### Thermo Couple Logger Device
## MakingDevices - 2022/23
#

import sys, time, datetime, csv
from PyQt5 import uic, QtCore,QtWidgets
from PyQt5.QtCore import QThread
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from PyQt5.QtWidgets import * 
import serial.tools.list_ports
import pyvisa

COMS = []

import pyvisa, time

rm = pyvisa.ResourceManager()

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

# -------------------------
#   TASK CONTROL   --   GLOBAL VARIABLES
# -------------------------
event = '_IDLE_'
Loop_number = 0
tc1_internal = 0
tc1_external = 0
tc2_internal = 0
tc2_external = 0
tc1_internal_buffer = 0
tc1_external_buffer = 0
tc2_internal_buffer = 0
tc2_external_buffer = 0
count_packages = 0
comport = 0
x_axis = 100
interrupt_data = 0
tic = 0
toc = 0
tic_sample = 0
toc_sample = 0
TC_LOGGER = None
connection_avail = 0
remove_line = [1,1,1,1]
comm_time = 0.25
sampling_rate = 1
sampling_number = 0
csv_mark = 0
sampling_choice = 0
last_sample = 0
xdata_1 = 0
origin_xdata_1 = 0
graph_choice = 6 
com_description = 0
board_info_bool = 0
board_HW = 0
board_SW = 0

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
    global com_description
    ports_avail = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if(hwid[12:16] == "04D8" and hwid[17:21] == "00AA"):
            com_description = desc
            ports_avail.append(port)
    return ports_avail

# ----------------------------------
#   INFO CLASS & RELATED DEFINITIONS
# ----------------------------------

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        global comport, com_description, board_HW, board_SW
        uic.loadUi("gui_app_2.ui", self)
        self.COM_board.setText(str(comport))
        self.vendor_USB.setText("04D8")
        self.product_USB.setText("00AA")
        self.label_14.setText(str(com_description))
        self.HW_board.setText(str(board_HW))
        self.SW_board.setText(str(board_SW))

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

        self.com_port_info.clicked.connect(self.fn_com_port_info) #Info page

        self.com_port_bt.clicked.connect(self.fn_com_port_bt) #Connect/disconnect button
        self.bt_recording_data.clicked.connect(self.fn_bt_recording_data) #Recording data
        self.bt_recording_data_mark.clicked.connect(self.fn_bt_recording_data_mark) #Recording data

        self.tc1_sampling_rate_2.currentIndexChanged.connect(self.fn_graph_sampling_changed)

        self.graph1_activation = 0  #Var to know if the graph is activated

        self.recording_data = 0 #Var to know if the data is being saved

        n_data = 1      #Number of samples to graph
        now = datetime.datetime.now()
        self.xdata_1_time = [now]
        self.ydata_1 = [0]  #internal T1
        self.ydata_2 = [0] #External T1
        self.ydata_3 = [0] #Internal T2
        self.ydata_4 = [0] #External T2

        self.timer1_start()   #Start the timer
        self.update_gui()     #Update the GUI

    def graph_resize_event(self):
        global xdata_1,origin_xdata_1
        if((self.graph1_activation == 1)):
            if(self.tc1_sampling_rate_2.currentIndex()==5):  #Complete graph
                now = datetime.datetime.now()     
                xdata_1 = dates.date2num(now) + (1/1440)*10  
                self.ax.set_xlim(origin_xdata_1, xdata_1)
            
            if(self.tc1_sampling_rate_2.currentIndex()==5):  #30 mins graph
                now = datetime.datetime.now()     
                if(dates.date2num(now) - origin_xdata_1 > (1/1440)*30):  #If we have more than 30 minutes of data... 
                    xdata_1 = dates.date2num(now) + (1/1440)*8  
                    self.ax.set_xlim(xdata_1 - (1/1440)*30 , xdata_1)
                else:
                    self.ax.set_xlim(origin_xdata_1, dates.date2num(now) + (1/1440)*10)

            if(self.tc1_sampling_rate_2.currentIndex()==4):  #24 hours graph
                now = datetime.datetime.now()     
                if(dates.date2num(now) - origin_xdata_1 > 1):  #If we have more than 1 day of data... 
                    xdata_1 = dates.date2num(now) + (1/1440)*30  
                    self.ax.set_xlim(xdata_1 - 1 , xdata_1)
                else:
                    self.ax.set_xlim(origin_xdata_1, dates.date2num(now) + (1/1440)*30)

            if(self.tc1_sampling_rate_2.currentIndex()==3):  #8 hours graph
                now = datetime.datetime.now()     
                if(dates.date2num(now) - origin_xdata_1 > (1/1440)*60*8):  #If we have more than 8 hours of data... 
                    xdata_1 = dates.date2num(now) + (1/1440)*30  
                    self.ax.set_xlim(xdata_1 - (1/1440)*60*8 , xdata_1)
                else:
                    self.ax.set_xlim(origin_xdata_1, dates.date2num(now) + (1/1440)*15)

            if(self.tc1_sampling_rate_2.currentIndex()==2):  #1 hour graph
                now = datetime.datetime.now()     
                if(dates.date2num(now) - origin_xdata_1 > (1/1440)*60):  #If we have more than 1 hour of data... 
                    xdata_1 = dates.date2num(now) + (1/1440)*15 
                    self.ax.set_xlim(xdata_1 - (1/1440)*60 , xdata_1)
                else:
                    self.ax.set_xlim(origin_xdata_1, dates.date2num(now) + (1/1440)*10)


            if(self.tc1_sampling_rate_2.currentIndex()==1):  #30 mins graph
                now = datetime.datetime.now()     
                if(dates.date2num(now) - origin_xdata_1 > (1/1440)*30):  #If we have more than 30 minutes of data... 
                    xdata_1 = dates.date2num(now) + (1/1440)*8  
                    self.ax.set_xlim(xdata_1 - (1/1440)*30 , xdata_1)
                else:
                    self.ax.set_xlim(origin_xdata_1, dates.date2num(now) + (1/1440)*5)

            if(self.tc1_sampling_rate_2.currentIndex()==0):  # 5 mins graph
                now = datetime.datetime.now()     
                xdata_1 = dates.date2num(now) + (1/1440)*4  
                self.ax.set_xlim(dates.date2num(now)-(1/1440)*1, xdata_1)

            self.fig.canvas.resize_event()
            self.bm.update()                               #BlitManager class prints everything
            self.fig.canvas.mpl_connect('close_event', self.handle_close)
    
    def fn_graph_sampling_changed(self):    
        self.graph_resize_event()
    
    def fn_com_port_info(self):
        self.info_window = AnotherWindow()
        self.info_window.show()

    def fn_bt_recording_data_mark(self):
        global csv_mark
        csv_mark = 1 #We print the mark

    def fn_bt_recording_data(self):
        if self.recording_data == 0:
            choice = QMessageBox.question(self, 'Recording data!',
                                          "Do you want to start recording the data?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                now = datetime.datetime.now()
                self.file_name = now.strftime("%d%m%Y_%H%M%S")
                # 2D list of variables (tabular data with rows and columns)
                file_index = [
                    ['Time', 'Status TC1', 'Internal T TC1', 'External T TC1', 'Status TC2', 'Internal T TC2','External T TC2','Mark']
                ]
                self.recording_data = 1
                # Example.csv gets created in the current working directory
                try:
                    with open('./data/log_' + self.file_name + '.csv', 'a', newline='') as csvfile:
                        my_writer = csv.writer(csvfile, delimiter=';')
                        my_writer.writerows(file_index)
                except:
                    print("Unable to open .csv file")
                self.bt_recording_data.setText("Stop Recording Data")
                self.record_data_label.setText("Recording: log_"+self.file_name+".csv")
            else:
                pass
        elif self.recording_data == 1:
            choice = QMessageBox.question(self, 'Stop recording data!',
                                          "Do you want to stop recording the data?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                print("Stop recording on data folder")
                self.recording_data = 0
                self.record_data_label.setText("")
                self.bt_recording_data.setText("Record Data")
            else:
                pass

    def fn_com_port_bt(self):
        global connection_avail, device,comport,origin_xdata_1,xdata_1, board_info_bool,remove_line
        if(connection_avail == 0):
            global TC_LOGGER
            self.com_port_bt.setText("Disconnect!")
            comport = self.com_port_usb.currentText()
            TC_LOGGER = rm.open_resource(comport)
            TC_LOGGER.baudrate=115200
            TC_LOGGER.timeout = 1
            TC_LOGGER.write_termination = '\n'
            TC_LOGGER.read_termination = '\n'
            connection_avail = 1
            self.tc1_graph.setEnabled(True)
            self.tc2_graph.setEnabled(True)
            self.tc1_graph_2.setEnabled(True)
            self.tc2_graph_2.setEnabled(True)
            self.com_port_info.setEnabled(True)
            self.bt_recording_data.setEnabled(True)
            self.bt_recording_data_mark.setEnabled(True)
            self.tc1_sampling_rate.setEnabled(True)
            self.tc1_sampling_rate_2.setEnabled(True)


            now = datetime.datetime.now()
            origin_xdata_1 = (dates.date2num(now))  #Get the X data. (x=0 at the beggining)
            xdata_1 = origin_xdata_1 + (1/1440)*10
            return

        if(connection_avail == 1):
            connection_avail = 0
            self.tc1_graph.setEnabled(False)
            self.tc2_graph.setEnabled(False)
            self.tc1_graph_2.setEnabled(False)
            self.tc2_graph_2.setEnabled(False)
            self.com_port_info.setEnabled(False)
            self.bt_recording_data.setEnabled(False)
            self.bt_recording_data_mark.setEnabled(False)
            self.tc1_sampling_rate.setEnabled(False)
            self.tc1_sampling_rate_2.setEnabled(False)
            self.tc1_graph.setChecked(False)
            self.tc2_graph.setChecked(False)
            self.tc1_graph_2.setChecked(False)
            self.tc2_graph_2.setChecked(False)
            remove_line[0] = 1
            remove_line[1] = 1
            remove_line[2] = 1
            remove_line[3] = 1
            self.graph1_activation = 0  #We change the variable to desactivated
            board_info_bool = 0
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
        global x_axis,remove_line,origin_xdata_1,xdata_1
        ###
        ## If the checkbox change of the state, the following code execute:
        #
        if state == QtCore.Qt.Checked:  #If checked
            remove_line[0] = 0
            if(self.graph1_activation==0):
                # make a new figure
                self.fig, self.ax = plt.subplots()            #New graph
                self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                self.ax.set_xlim(origin_xdata_1 , xdata_1)                #Axis X in matplotlib DATE FORMAT
                #self.ax.get_xaxis().set_animated(True)                                   #1/1440 * (TIME IN MINUTES)
                self.ax.set_title("Temperature Plot")   #Title
                self.graph1_activation = 1  #We change the variable to activated
            #Yself.ax.xaxis.axis_date
            (self.ln,) = self.ax.plot(self.xdata_1_time, self.ydata_1, animated=True, label="Internal T1")   #We create the lines with the data 
            plot_list = [self.ln]
            if(remove_line[1]==0):
                plot_list.append(self.ln_2)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)    
            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.xticks(rotation=45, ha='right')
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


    def graph2_activation_checkbox(self, state):
        global remove_line,origin_xdata_1,xdata_1
        if state == QtCore.Qt.Checked:  #If checked
            remove_line[1] = 0
            if(self.graph1_activation==0):
                # make a new figure
                self.fig, self.ax = plt.subplots()            #New graph
                self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                self.ax.set_xlim(origin_xdata_1 , xdata_1)   
                self.ax.set_title("Temperature Plot")   #Title
                self.graph1_activation = 1

            (self.ln_2,) = self.ax.plot(self.xdata_1_time, self.ydata_2, animated=True, label="External T1")
            plot_list = [self.ln_2]
            if(remove_line[0]==0):
                plot_list.append(self.ln)
            if(remove_line[2]==0):
                plot_list.append(self.ln_3)
            if(remove_line[3]==0):
                plot_list.append(self.ln_4)  

            self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
            plt.legend()
            plt.xticks(rotation=45, ha='right')
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
            
    def graph3_activation_checkbox(self, state):
            global remove_line,origin_xdata_1,xdata_1
            if state == QtCore.Qt.Checked:  #If checked
                remove_line[2] = 0
                if(self.graph1_activation==0):
                    # make a new figure
                    self.fig, self.ax = plt.subplots()            #New graph
                    self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                    self.ax.set_xlim(origin_xdata_1 , xdata_1)   
                    self.ax.set_title("Temperature Plot")   #Title
                    self.graph1_activation = 1

                (self.ln_3,) = self.ax.plot(self.xdata_1_time, self.ydata_3, animated=True, label="Internal T2")
                plot_list = [self.ln_3]
                if(remove_line[0]==0):
                    plot_list.append(self.ln)
                if(remove_line[1]==0):
                    plot_list.append(self.ln_2)
                if(remove_line[3]==0):
                    plot_list.append(self.ln_4)  

                self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
                plt.legend()
                plt.xticks(rotation=45, ha='right')
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

    def graph4_activation_checkbox(self, state):
                global remove_line,origin_xdata_1,xdata_1
                if state == QtCore.Qt.Checked:  #If checked
                    remove_line[3] = 0
                    if(self.graph1_activation==0):
                        # make a new figure
                        self.fig, self.ax = plt.subplots()            #New graph
                        self.ax.set_ylim(0,100)                  #Axis Y from 0 to 200
                        self.ax.set_xlim(origin_xdata_1 , xdata_1)   
                        self.ax.set_title("Temperature Plot")   #Title
                        self.graph1_activation = 1

                    (self.ln_4,) = self.ax.plot(self.xdata_1_time, self.ydata_4, animated=True, label="External T2")  
                    plot_list = [self.ln_4]
                    if(remove_line[0]==0):
                        plot_list.append(self.ln)
                    if(remove_line[1]==0):
                        plot_list.append(self.ln_2)
                    if(remove_line[2]==0):
                        plot_list.append(self.ln_3)  

                    self.bm = BlitManager(self.fig.canvas, plot_list)      #Execute the class BlitManager to take control over the lines
                    plt.legend()
                    plt.xticks(rotation=45, ha='right')
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

    def update_gui(self):  #Update GUI (Without human interaction)
        global origin_xdata_1,xdata_1,graph_choice,COMS, tc1_internal,tc1_external, x_axis, interrupt_data,tc2_internal,tc2_external,last_sample,tic_sample,toc_sample,connection_avail,remove_line,csv_mark,sampling_choice, count_packages,sampling_choice,sampling_number,sampling_rate
        if (connection_avail==0):
            self.update_COM()
        tic_sample = time.perf_counter()
        if (count_packages<1000):
            self.dl_debug.setText(f"Packages: {count_packages}" + f" Sampling: {last_sample:0.2f}s // "+"SN: "+str(sampling_number)+" SR: "+str(sampling_rate)+" SC: "+str(sampling_choice))
        else:
            self.dl_debug.setText(f"Packages: {count_packages/1000:0.2f}k" + f" Sampling: {last_sample:0.2f}s // "+"SN: "+str(sampling_number)+" SR: "+str(sampling_rate)+" SC: "+str(sampling_choice))

        sampling_choice = self.tc1_sampling_rate.currentIndex()
        graph_choice = self.tc1_sampling_rate_2.currentIndex()
        if(interrupt_data == 1):
            now = datetime.datetime.now()
            self.xdata_1_time.append(now)  #We load the new data
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

            last_sample = tic_sample - toc_sample
            toc_sample = time.perf_counter()
            if(tc1_internal == -300):
                self.tc1_status.setText("Not connected")
            elif(tc1_internal == -301):
                self.tc1_status.setText("Short to GND")
            elif(tc1_internal == -302):
                self.tc1_status.setText("Short to Vcc")
            else:
                self.tc1_status.setText("Working")

            self.tc1_int_temperature.setText(str(tc1_internal))           #print internal Temp
            self.tc1_ext_temperature.setText(str(tc1_external))           #print external Temp

            if(tc2_internal == -300):
                self.tc2_status.setText("Not connected")
            elif(tc2_internal == -301):
                self.tc2_status.setText("Short to GND")
            elif(tc2_internal == -302):
                self.tc2_status.setText("Short to Vcc")
            else:
                self.tc2_status.setText("Working")
            self.tc2_int_temperature.setText(str(tc2_internal))           #print internal Temp
            self.tc2_ext_temperature.setText(str(tc2_external))           #print external Temp
            if(self.recording_data==1):
                now = datetime.datetime.now()
                self.file_name_updated = now.strftime("%d%m%Y_%H%M%S")
                file_index = [
                    [self.file_name_updated, self.tc1_status.text(), str(tc1_external), str(tc1_internal),  self.tc2_status.text(), str(tc2_internal),str(tc2_external),csv_mark]
                ]
                if(csv_mark==1): csv_mark = 0
                # Example.csv gets created in the current working directory
                try:
                    with open('./data/log_' + self.file_name + '.csv', 'a', newline='') as csvfile:
                        my_writer = csv.writer(csvfile, delimiter=';')
                        my_writer.writerows(file_index)
                except:
                    print("Unable to open .csv file")

        if (self.graph1_activation == 1):                  #If the graph is activated...
            if(remove_line[0]==0):
                self.ln.set_xdata(self.xdata_1_time)
                self.ln.set_ydata(self.ydata_1)                #Load the new values of Y...
            if(remove_line[1]==0):
                self.ln_2.set_xdata(self.xdata_1_time)
                self.ln_2.set_ydata(self.ydata_2)
            if(remove_line[2]==0):                
                self.ln_3.set_xdata(self.xdata_1_time)
                self.ln_3.set_ydata(self.ydata_3)
            if(remove_line[3]==0):
                self.ln_4.set_xdata(self.xdata_1_time)
                self.ln_4.set_ydata(self.ydata_4)        
            
            now = datetime.datetime.now()        
            if(dates.date2num(now) + ((1/1440)*2) > xdata_1): 
                self.graph_resize_event()
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
    global COMS,Loop_number,board_HW, board_SW, board_info_bool,comport, last_sample,interrupt_data, tc1_external, tc1_internal, tc2_external, tc2_internal,tc1_external_buffer, tc1_internal_buffer, tc2_external_buffer, count_packages,tc2_internal_buffer,tic, toc, connection_avail, comport,TC_LOGGER, rm, csv_mark,sampling_rate, sampling_number,sampling_choice
    if(Loop_number > 3 and connection_avail==0):
        COMS = serial_ports()
        Loop_number = 0
    if(sampling_choice == 0): comm_time = 0.15
    else: comm_time = 0.25
    sampling_rate = 1
    if(sampling_choice==1): sampling_rate = 1
    elif(sampling_choice==2): sampling_rate = 2
    elif(sampling_choice==3): sampling_rate = 4
    elif(sampling_choice==4): sampling_rate = 20
    elif(sampling_choice==5): sampling_rate = 40
    elif(sampling_choice==6): sampling_rate = 240
    elif(sampling_choice==7): sampling_rate = 480
    elif(sampling_choice==8): sampling_rate = 720
    elif(sampling_choice==9): sampling_rate = 1200
    elif(sampling_choice==10): sampling_rate = 2400
    toc = time.perf_counter()
    if((toc-tic)>comm_time): #Communication time with USB. Recommended: 250ms. Experimental: 150ms
        Loop_number += toc-tic
        tic = time.perf_counter()
        if(connection_avail == 1):
            try:
                if(board_info_bool==0):
                    board_HW = TC_LOGGER.query(':CONFIG:HW?')
                    board_SW =  TC_LOGGER.query(':CONFIG:APP?')
                    board_info_bool = 1

                if(sampling_number == 0):
                    tc1_external_buffer = 0
                    tc1_internal_buffer = 0
                    tc2_external_buffer = 0
                    tc2_internal_buffer = 0

                tc1_external_buffer  += float(TC_LOGGER.query(':MEAS:TC1:EXT?'))
                tc1_internal_buffer  += float(TC_LOGGER.query(':MEAS:TC1:INT?'))
                tc2_external_buffer  += float(TC_LOGGER.query(':MEAS:TC2:EXT?'))
                tc2_internal_buffer  += float(TC_LOGGER.query(':MEAS:TC2:INT?'))

                sampling_number += 1
                count_packages +=1

                if(sampling_number >= sampling_rate):
                    tc1_external = round(tc1_external_buffer / sampling_number, 2)
                    tc1_internal = round(tc1_internal_buffer / sampling_number, 2)
                    tc2_external = round(tc2_external_buffer / sampling_number, 2)
                    tc2_internal = round(tc2_internal_buffer / sampling_number, 2)
                    sampling_number = 0
                    interrupt_data = 1

            except:
                TC_LOGGER = None
                print("Trying to reconnect...")
                COMS = serial_ports()
                if(len(COMS) > 0):
                    if COMS[0] == comport: 
                        print("USB Ready")
                        TC_LOGGER = rm.open_resource(comport)
                        TC_LOGGER.baudrate=115200
                        TC_LOGGER.timeout = 1
                        TC_LOGGER.write_termination = '\n'
                        TC_LOGGER.read_termination = '\n'
                        print("Connected!")
            
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
    