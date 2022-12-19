### Thermo Couple Device
## Ruben Garcia Segovia - 2022
#

import sys, time
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QThread
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QApplication
import serial.tools.list_ports

import serial, time

COMS = []

def bin2tempint(binary, binary2):
    temperature = 0
    if(binary&0b00000001 == 1):
        print("thermocouple is open circuit")
    elif(binary&0b00000010 == 0b10):
        print("thermocouple is short-circuit to GND")
    elif(binary&0b00000100 == 0b100):
        print("thermocouple is short-circuit to Vcc")
    if(binary&0b00010000 == 0b10000):
        temperature += 0.0625
    if(binary&0b00100000 == 0b100000):
        temperature += 0.125
    if(binary&0b01000000 == 0b1000000):
        temperature += 0.25
    if(binary&0b10000000 == 0b10000000):
        temperature += 0.5
    if(binary2&0b0000001 == 0b1):
        temperature += 1
    if(binary2&0b0000010 == 0b10):
        temperature += 2
    if(binary2&0b00000100 == 0b100):
        temperature += 4
    if(binary2&0b00001000 == 0b1000):
        temperature += 8
    if(binary2&0b00010000 == 0b10000):
        temperature += 16
    if(binary2&0b00100000 == 0b100000):
        temperature += 32
    if(binary2&0b01000000 == 0b1000000):
        temperature += 64
    if(binary2&0b10000000 == 0b10000000):
        temperature = temperature*(-1)
    return temperature

def bin2tempext(binary, binary2):
    temperature = 0
    if(binary&0b00000001 == 1):
        print("Thermocouple error")
    if(binary&0b00000100 == 0b100):
        temperature += 0.25
    if(binary&0b00001000 == 0b1000):
        temperature += 0.5
    if(binary&0b00010000 == 0b10000):
        temperature += 1
    if(binary&0b00100000 == 0b100000):
        temperature += 2
    if(binary&0b01000000 == 0b1000000):
        temperature += 4
    if(binary&0b10000000 == 0b10000000):
        temperature += 8
    if(binary2&0b0000001 == 0b1):
        temperature += 16
    if(binary2&0b0000010 == 0b10):
        temperature += 32
    if(binary2&0b00000100 == 0b100):
        temperature += 64
    if(binary2&0b00001000 == 0b1000):
        temperature += 128
    if(binary2&0b00010000 == 0b10000):
        temperature += 256
    if(binary2&0b00100000 == 0b100000):
        temperature += 512
    if(binary2&0b01000000 == 0b1000000):
        temperature += 1024
    if(binary2&0b10000000 == 0b10000000):
        temperature = temperature*(-1)
    return temperature

# -------------------------
#   TASK CONTROL   --   VARIABLES GLOBALES
# -------------------------
event = '_IDLE_'
Loop_number = 0
tc1_internal = 0
tc1_external = 0
tc2_internal = 0
tc2_external = 0
x_axis = 100
interrupt_data = 0
tic = 0
toc = 0
tic_sample = 0
toc_sample = 0
com_port = "COM9"
connection_avail = 0
device = serial.Serial()

## ---------------------------
##  GRAPH CLASS & RELATED DEFINITIONS
## ---------------------------

class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()

# ----------------------------------
#   USB Serial Check
# ----------------------------------

def serial_ports():
    """ Lists serial port names, descriptions and HW IDs
    """
    ports_avail = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if(hwid[12:16] == "04D8" and hwid[17:21] == "00AA"):
            ports_avail.append(port)
    return ports_avail

# ----------------------------------
#   GUI CLASS & RELATED DEFINITIONS
# ----------------------------------

class MyMainWindow(QMainWindow):
       
    def __init__(self):
        super().__init__()

        uic.loadUi("gui_app.ui", self)
        self.tc1_graph.stateChanged.connect(self.graph1_activation_checkbox) # CheckBox para la grafica. Excepción cuando cambia de estado.
        self.com_port_bt.clicked.connect(self.fn_com_port_bt)

        self.graph1_activation = 0  #Variable para saber si la grafica está activada o no.

        n_data = 1      #Numero de samples para graficar

        self.xdata_1 = [1]  #Cogemos samples para el valor de X. (x=0 para todas las muestras)
        self.ydata_1 = [0]  #internal T1
        self.ydata_2 = [0] #External T1
        self.ydata_3 = [0] #Internal T2
        self.ydata_4 = [0] #External T2

        self.timer1_start()   #Inicio el timer
        self.update_gui()     #Actualizo la GUI

    def fn_com_port_bt(self):
        global connection_avail, device
        if(connection_avail == 0):
            self.com_port_bt.setText("Disconnect!")
            com_port = self.com_port_usb.currentText()
            print(com_port)
            device = serial.Serial(port=com_port, baudrate=115200, timeout=0.001, write_timeout=0.001)
            connection_avail = 1
            return

        if(connection_avail == 1):
            connection_avail = 0
            self.com_port_bt.setText("Connect!")


    def update_COM(self):
        global COMS
        if(len(COMS) > 0):
            if(len(COMS) != self.com_port_usb.count()):
                self.com_port_usb.clear()

            for i in range(len(COMS)):
                if(self.com_port_usb.itemText(i) != COMS[i]):
                    self.com_port_usb.addItem(COMS[i])

    def graph1_activation_checkbox(self, state):
        global x_axis
        ###
        ## En cualquier momento que el checkbox cambia de estado, este codigo se ejecuta:
        #
        if state == QtCore.Qt.Checked:  #Si está check
            # make a new figure
            self.fig, self.ax = plt.subplots()            #Creamos nueva ventana de gráfica
            self.ax.set_ylim(0,100)                  #Eje Y de 0 a 200
            self.ax.set_xlim(0, x_axis)                #Eje X de 0 a 1000
            #self.ax.get_xaxis().set_animated(True)
            self.ax.set_title("Temperature Plot")   #Titulo grafica

            (self.ln,) = self.ax.plot(self.xdata_1, self.ydata_1, animated=True, label="Internal T1")   #We create the lines with the data
            (self.ln_2,) = self.ax.plot(self.xdata_1, self.ydata_2, animated=True, label="External T1")             
            (self.ln_3,) = self.ax.plot(self.xdata_1, self.ydata_3, animated=True, label="Internal T2")   
            (self.ln_4,) = self.ax.plot(self.xdata_1, self.ydata_4, animated=True, label="External T2")  
            self.bm = BlitManager(self.fig.canvas, [self.ln,self.ln_2,self.ln_3,self.ln_4 ])      #Ejecutamos la clase BlitManager para que tome el control de la linea y la imprima en la ventada de grafica
            plt.legend()
            plt.show(block=False)    #Enseñamos al usuario la ventana de grafica
            plt.pause(.1)            #Una pequeña pausa para arrancar
            self.graph1_activation = 1  #Cambiamos la variable de la grafica a activa
        else:
            self.graph1_activation = 0  #Cambiamos la variable de la grafica a desactivada

    def update_gui(self):  #Funcion que actualiza la GUI de forma automatica (SIN NECESIDAD DE INTERACTUAR CON EL HUMANO)
        global COMS, tc1_internal,tc1_external, x_axis, interrupt_data,tc2_internal,tc2_external,tic_sample,toc_sample
        self.update_COM()
        tic_sample = time.perf_counter()
        if(interrupt_data == 1):
            self.xdata_1.append(self.xdata_1[-1] + 1)  #We load the new data
            self.ydata_1.append(tc1_internal)         
            self.ydata_2.append(tc1_external)
            self.ydata_3.append(tc2_internal)
            self.ydata_4.append(tc2_external)
            interrupt_data = 0
            print(f"Sampling time {tic_sample - toc_sample:0.4f} seconds")
            toc_sample = time.perf_counter()
            self.tc1_status.setText("Working")
            self.tc1_int_temperature.setText(str(tc1_internal))           #print internal Temp
            self.tc1_ext_temperature.setText(str(tc1_external))           #print external Temp
            self.tc2_status.setText("Working")
            self.tc2_int_temperature.setText(str(tc2_internal))           #print internal Temp
            self.tc2_ext_temperature.setText(str(tc2_external))           #print external Temp

        if (self.graph1_activation == 1):                  #Si la grafica está activada...
            self.ln.set_xdata(self.xdata_1)
            self.ln.set_ydata(self.ydata_1)                #Cargamos los nuevos valores de Y a la linea.
            self.ln_2.set_xdata(self.xdata_1)
            self.ln_2.set_ydata(self.ydata_2)                #Cargamos los nuevos valores de Y a la linea.
            self.ln_3.set_xdata(self.xdata_1)
            self.ln_3.set_ydata(self.ydata_3)
            self.ln_4.set_xdata(self.xdata_1)
            self.ln_4.set_ydata(self.ydata_4)                #Cargamos los nuevos valores de Y a la linea.
            if(self.xdata_1[-1] + 20 > x_axis):
                x_axis = x_axis + 100
                self.ax.set_xlim(0, x_axis)
                self.fig.canvas.resize_event()
                    # tell the blitting manager to do its thing
            self.bm.update()                               #Y que la clase BlitManager se encargue de graficar.
            self.fig.canvas.mpl_connect('close_event', self.handle_close)

    def handle_close(self, evt):
        self.tc1_graph.setChecked(False)
        print('Closed Figure')
    def timer1_start(self):  #TIMER
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.timer1_timeout) #Se ejecuta esta funcion cuando el tiempo se agota
        self.timer1.start(25) #50ms

    def timer1_timeout(self): #Cuando el tiempo se agota, ejecuto update_gui.
        self.update_gui() #OJO!, es "self" por que si no, no podria acceder a la GUI

class AThread(QThread):  #Thread en paralelo a la actualizacion del GUI
    def run(self):
        while True:
            time.sleep(0.01)
            Event_Task()  #Lanzamos funcion Event_Task cada 10ms EN PARALELO.

def Event_Task():
    global COMS,Loop_number, interrupt_data, tc1_external, tc1_internal, tc2_external, tc2_internal, tic, toc, connection_avail 
    if(Loop_number > 3):
        COMS = serial_ports()
        Loop_number = 0
    toc = time.perf_counter()
    if((toc-tic)>=0.15):
        Loop_number += 0.15
        tic = time.perf_counter()
        if(connection_avail == 1):
            try:
                device.write('getValue'.encode('utf-8'))
                raw_string_b = device.readline()
                tc1_internal= bin2tempint(raw_string_b[4],raw_string_b[3])
                tc1_external = bin2tempext(raw_string_b[2],raw_string_b[1])
                tc2_internal = bin2tempint(raw_string_b[8],raw_string_b[7])
                tc2_external = bin2tempext(raw_string_b[6],raw_string_b[5])
                interrupt_data = 1
            except:
                print("Exception occurred, somthing wrong...")
                connection_avail = 0
            

        


# -----------------
#   MAIN PROGRAM
# -----------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = MyMainWindow()
    GUI.show()
    thread = AThread()
    thread.finished.connect(app.exit)
    thread.start()

    sys.exit(app.exec())

# DRAFT & NOTES

"""

    
"""    
    