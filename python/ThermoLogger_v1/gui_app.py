### Thermo Couple Logger Device
## MakingDevices - 2022/23
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
        #print("thermocouple is open circuit")
        temperature = -1000
        return temperature
    elif(binary&0b00000010 == 0b10):
        #print("thermocouple is short-circuit to GND")
        temperature = -1001
        return temperature
    elif(binary&0b00000100 == 0b100):
        #print("thermocouple is short-circuit to Vcc")
        temperature = -1002
        return temperature
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
        #print("Thermocouple error")
        temperature = -10003
        return temperature
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
#   TASK CONTROL   --   GLOBAL VARIABLES
# -------------------------
event = '_IDLE_'
Loop_number = 0
tc1_internal = 0
tc1_external = 0
tc2_internal = 0
tc2_external = 0
comport = 0
x_axis = 100
interrupt_data = 0
tic = 0
toc = 0
tic_sample = 0
toc_sample = 0
connection_avail = 0
remove_line = [1,1,1,1]
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
        self.tc1_graph.stateChanged.connect(self.graph1_activation_checkbox) # CheckBox for the graph tc1 Internal
        self.tc2_graph.stateChanged.connect(self.graph2_activation_checkbox) # CheckBox for the graph tc1 External
        self.tc1_graph_2.stateChanged.connect(self.graph3_activation_checkbox) # CheckBox for the graph tc2 Internal
        self.tc2_graph_2.stateChanged.connect(self.graph4_activation_checkbox) # CheckBox for the graph tc2 External

        self.com_port_bt.clicked.connect(self.fn_com_port_bt)

        self.graph1_activation = 0  #Var to know if the graph is activated

        n_data = 1      #Number of samples to graph

        self.xdata_1 = [1]  #Get the X data. (x=0 at the beggining)
        self.ydata_1 = [0]  #internal T1
        self.ydata_2 = [0] #External T1
        self.ydata_3 = [0] #Internal T2
        self.ydata_4 = [0] #External T2

        self.timer1_start()   #Start the timer
        self.update_gui()     #Update the GUI

    def fn_com_port_bt(self):
        global connection_avail, device,comport
        if(connection_avail == 0):
            self.com_port_bt.setText("Disconnect!")
            comport = self.com_port_usb.currentText()
            device = serial.Serial(port=comport, baudrate=115200, timeout=0.001, write_timeout=0.001)
            connection_avail = 1
            self.tc1_graph.setEnabled(True)
            self.tc2_graph.setEnabled(True)
            self.tc1_graph_2.setEnabled(True)
            self.tc2_graph_2.setEnabled(True)
            return

        if(connection_avail == 1):
            connection_avail = 0
            self.tc1_graph.setEnabled(False)
            self.tc2_graph.setEnabled(False)
            self.tc1_graph_2.setEnabled(False)
            self.tc2_graph_2.setEnabled(False)
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
        global x_axis,remove_line
        ###
        ## If the checkbox change of the state, the following code execute:
        #
        if state == QtCore.Qt.Checked:  #If checked
            remove_line[0] = 0
            if(self.graph1_activation==0):
                # make a new figure
                self.fig, self.ax = plt.subplots()            #New graph
                self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                self.ax.set_xlim(0, x_axis)                #Axis X fro 0 to 1000
                #self.ax.get_xaxis().set_animated(True)
                self.ax.set_title("Temperature Plot")   #Title
                self.graph1_activation = 1  #We change the variable to activated

            (self.ln,) = self.ax.plot(self.xdata_1, self.ydata_1, animated=True, label="Internal T1")   #We create the lines with the data 
            plot_list = [self.ln]
            if(remove_line[1]==0):
                plot_list.append(self.ln_2)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)  
            #(self.ln_2,) = self.ax.plot(self.xdata_1, self.ydata_2, animated=True, label="External T1")        
            #(self.ln_3,) = self.ax.plot(self.xdata_1, self.ydata_3, animated=True, label="Internal T2")   
            #(self.ln_4,) = self.ax.plot(self.xdata_1, self.ydata_4, animated=True, label="External T2")  
            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.show(block=False)    #We show to the user the plot
            plt.pause(.1)            
        else:
            remove_line[0] = 1
            self.ln.remove()
            plot_list = []
            if(remove_line[1]==0):
                plot_list.append(self.ln_2)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)  
            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.show(block=False)    #We show to the user the plot
            plt.pause(.1)   
            self.bm.update()   
            self.fig.canvas.resize_event()
            #if(remove_line[0]==1 and remove_line[1] ==1 and remove_line[2]==1 and remove_line[3]==1):
                #self.graph1_activation = 0  #We change the variable to desactivated

    def graph2_activation_checkbox(self, state):
        global remove_line
        if state == QtCore.Qt.Checked:  #If checked
            remove_line[1] = 0
            if(self.graph1_activation==0):
                # make a new figure
                self.fig, self.ax = plt.subplots()            #New graph
                self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                self.ax.set_xlim(0, x_axis)                #Axis X fro 0 to 1000
                #self.ax.get_xaxis().set_animated(True)
                self.ax.set_title("Temperature Plot")   #Title
                self.graph1_activation = 1

            (self.ln_2,) = self.ax.plot(self.xdata_1, self.ydata_2, animated=True, label="External T1")
            plot_list = [self.ln_2]
            if(remove_line[0]==0):
                plot_list.append(self.ln)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)  

            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.show(block=False)    #We show to the user the plot
            plt.pause(.1)   
            self.bm.update()   
            self.fig.canvas.resize_event()
        else:
            remove_line[1] = 1
            self.ln_2.remove()
            plot_list = []
            if(remove_line[0]==0):
                plot_list.append(self.ln)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)  
            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.show(block=False)    #We show to the user the plot
            plt.pause(.1)   
            self.bm.update()   
            self.fig.canvas.resize_event()
            #if(remove_line[0]==1 and remove_line[1] ==1 and remove_line[2]==1 and remove_line[3]==1):
                #self.graph1_activation = 0  #We change the variable to desactivated
            
    def graph3_activation_checkbox(self, state):
            global remove_line
            if state == QtCore.Qt.Checked:  #If checked
                remove_line[2] = 0
                if(self.graph1_activation==0):
                    # make a new figure
                    self.fig, self.ax = plt.subplots()            #New graph
                    self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                    self.ax.set_xlim(0, x_axis)                #Axis X fro 0 to 1000
                    self.ax.set_title("Temperature Plot")   #Title
                    self.graph1_activation = 1

                (self.ln_3,) = self.ax.plot(self.xdata_1, self.ydata_3, animated=True, label="Internal T2")
                plot_list = [self.ln_3]
                if(remove_line[0]==0):
                    plot_list.append(self.ln)
                if(remove_line[1]==0):
                    plot_list.append(self.ln_2)
                if(remove_line[3]==0):
                    plot_list.append(self.ln_4)  

                self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
                plt.legend()
                plt.show(block=False)    #We show to the user the plot
                plt.pause(.1)   
                self.bm.update()   
                self.fig.canvas.resize_event()
            else:
                remove_line[2] = 1
                self.ln_3.remove()
                plot_list = []
                if(remove_line[0]==0):
                    plot_list.append(self.ln)
                if(remove_line[1]==0):
                    plot_list.append(self.ln_2)
                if(remove_line[3]==0):
                    plot_list.append(self.ln_4)  
                self.bm = BlitManager(self.fig.canvas, plot_list)   #Execute the class BlitManager to take control over the lines
                plt.legend()
                plt.show(block=False)   #We show to the user the plot
                plt.pause(.1)   
                self.bm.update()   
                self.fig.canvas.resize_event()
                #if(remove_line[0]==1 and remove_line[1] ==1 and remove_line[2]==1 and remove_line[3]==1):
                    #self.graph1_activation = 0  #We change the variable to desactivated

    def graph4_activation_checkbox(self, state):
                global remove_line
                if state == QtCore.Qt.Checked:  #If checked
                    remove_line[3] = 0
                    if(self.graph1_activation==0):
                        # make a new figure
                        self.fig, self.ax = plt.subplots()            #New graph
                        self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                        self.ax.set_xlim(0, x_axis)                #Axis X fro 0 to 1000
                        self.ax.set_title("Temperature Plot")   #Title
                        self.graph1_activation = 1

                    (self.ln_4,) = self.ax.plot(self.xdata_1, self.ydata_4, animated=True, label="External T2")  
                    plot_list = [self.ln_4]
                    if(remove_line[0]==0):
                        plot_list.append(self.ln)
                    if(remove_line[1]==0):
                        plot_list.append(self.ln_2)
                    if(remove_line[2]==0):
                        plot_list.append(self.ln_3)  

                    self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
                    plt.legend()
                    plt.show(block=False)    #We show to the user the plot
                    plt.pause(.1)   
                    self.bm.update()   
                    self.fig.canvas.resize_event()
                else:
                    remove_line[3] = 1
                    self.ln_4.remove()
                    plot_list = []
                    if(remove_line[0]==0):
                        plot_list.append(self.ln)
                    if(remove_line[1]==0):
                        plot_list.append(self.ln_2)
                    if(remove_line[2]==0):
                        plot_list.append(self.ln_3)  
                    self.bm = BlitManager(self.fig.canvas, plot_list)   #Execute the class BlitManager to take control over the lines
                    plt.legend()
                    plt.show(block=False)   #We show to the user the plot
                    plt.pause(.1)   
                    self.bm.update()   
                    self.fig.canvas.resize_event()
                    #if(remove_line[0]==1 and remove_line[1] ==1 and remove_line[2]==1 and remove_line[3]==1):
                        #self.graph1_activation = 0  #We change the variable to desactivated

    def update_gui(self):  #Update GUI (Without human interaction)
        global COMS, tc1_internal,tc1_external, x_axis, interrupt_data,tc2_internal,tc2_external,tic_sample,toc_sample,connection_avail,remove_line
        if (connection_avail==0):
            self.update_COM()

        tic_sample = time.perf_counter()
        if(interrupt_data == 1):
            self.xdata_1.append(self.xdata_1[-1] + 1)  #We load the new data
            if(tc1_internal > -100):
                self.ydata_1.append(tc1_internal)         
                self.ydata_2.append(tc1_external)
                self.tc1_int_temperature.setEnabled(True)
                self.tc1_ext_temperature.setEnabled(True)
                self.tc1_graph.setEnabled(True)
                self.tc2_graph.setEnabled(True)
            else:
                self.ydata_1.append(0) 
                self.ydata_2.append(0) 
                self.tc1_int_temperature.setEnabled(False)
                self.tc1_ext_temperature.setEnabled(False)
                self.tc1_graph.setEnabled(False)
                self.tc2_graph.setEnabled(False)
            
            if(tc2_internal > -100):
                self.ydata_3.append(tc2_internal)
                self.ydata_4.append(tc2_external)
                self.tc2_int_temperature.setEnabled(True)
                self.tc2_ext_temperature.setEnabled(True)
                self.tc1_graph.setEnabled(True)
                self.tc2_graph.setEnabled(True)
            else:
                self.ydata_3.append(0)
                self.ydata_4.append(0)
                self.tc2_int_temperature.setEnabled(False)
                self.tc2_ext_temperature.setEnabled(False)
                self.tc1_graph_2.setEnabled(False)
                self.tc2_graph_2.setEnabled(False)
            interrupt_data = 0

            print(f"Sampling time {tic_sample - toc_sample:0.4f} seconds")

            toc_sample = time.perf_counter()
            if(tc1_internal == -1000):
                self.tc1_status.setText("Not connected")
            elif(tc1_internal == -1001):
                self.tc1_status.setText("Short to GND")
            elif(tc1_internal == -1002):
                self.tc1_status.setText("Short to Vcc")
            else:
                self.tc1_status.setText("Working")

            self.tc1_int_temperature.setText(str(tc1_internal))           #print internal Temp
            self.tc1_ext_temperature.setText(str(tc1_external))           #print external Temp

            if(tc2_internal == -1000):
                self.tc2_status.setText("Not connected")
            elif(tc2_internal == -1001):
                self.tc2_status.setText("Short to GND")
            elif(tc2_internal == -1002):
                self.tc2_status.setText("Short to Vcc")
            else:
                self.tc2_status.setText("Working")
            self.tc2_int_temperature.setText(str(tc2_internal))           #print internal Temp
            self.tc2_ext_temperature.setText(str(tc2_external))           #print external Temp

        if (self.graph1_activation == 1):                  #If the graph is activated...
            if(remove_line[0]==0):
                self.ln.set_xdata(self.xdata_1)
                self.ln.set_ydata(self.ydata_1)                #Load the new values of Y...
            if(remove_line[1]==0):
                self.ln_2.set_xdata(self.xdata_1)
                self.ln_2.set_ydata(self.ydata_2)
            if(remove_line[2]==0):                
                self.ln_3.set_xdata(self.xdata_1)
                self.ln_3.set_ydata(self.ydata_3)
            if(remove_line[3]==0):
                self.ln_4.set_xdata(self.xdata_1)
                self.ln_4.set_ydata(self.ydata_4)                
            if(self.xdata_1[-1] + 20 > x_axis):
                x_axis = x_axis + 100
                self.ax.set_xlim(0, x_axis)
                self.fig.canvas.resize_event()
                    # tell the blitting manager to do its thing
            self.bm.update()                               #BlitManager class prints everything
            self.fig.canvas.mpl_connect('close_event', self.handle_close)

    def handle_close(self, evt):
        global remove_line
        self.tc1_graph.setChecked(False)
        self.tc2_graph.setChecked(False)
        self.tc1_graph_2.setChecked(False)
        self.tc2_graph_2.setChecked(False)
        remove_line[0] = 1
        remove_line[1] = 1
        remove_line[2] = 1
        remove_line[3] = 1
        print('Closed Figure')
        self.graph1_activation = 0  #We change the variable to desactivated
    def timer1_start(self):  #TIMER
        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.timer1_timeout) #The function is call when the time is over
        self.timer1.start(25) #ms

    def timer1_timeout(self): #When the time is over...
        self.update_gui() #Watch out! it is "self" so it can access the GUI

class AThread(QThread):  #Thread in parallel
    def run(self):
        while True:
            time.sleep(0.001) # Seconds
            Event_Task()  #We launch Event_Task every 10ms in parallel

def Event_Task():
    global COMS,Loop_number,comport, interrupt_data, tc1_external, tc1_internal, tc2_external, tc2_internal, tic, toc, connection_avail, device
    if(Loop_number > 3 and connection_avail==0):
        COMS = serial_ports()
        Loop_number = 0
    toc = time.perf_counter()
    if((toc-tic)>=0.15):
        Loop_number += 0.15
        tic = time.perf_counter()
        if(connection_avail == 1):
            try:
                if(device == None):
                    device = serial.Serial(port=comport, baudrate=115200, timeout=0.0001, write_timeout=0.0001)
                
                device.write(':MEAS:TC1:EXT?'.encode('utf-8'))

                raw_string_b = device.readline()
                print(str(raw_string_b))

                tc1_internal= bin2tempint(raw_string_b[4],raw_string_b[3])
                tc1_external = bin2tempext(raw_string_b[2],raw_string_b[1])
                tc2_internal = bin2tempint(raw_string_b[8],raw_string_b[7])
                tc2_external = bin2tempext(raw_string_b[6],raw_string_b[5])
                
                if(device!= None):device.close()
                device = None

                interrupt_data = 1
            except:
                if(device!= None):device.close()
                device = None
                print("Trying to reconnect...")
            
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
    