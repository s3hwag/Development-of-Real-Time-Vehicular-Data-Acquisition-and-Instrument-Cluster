import sys
import io
import PyQt5
import socket
import threading
import time
import random
import struct

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5 import QtCore, QtGui, QtWidgets
from gauge import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSocketNotifier, Qt

ui=None
def handle_socket_events(socket_descriptor):
    notifier = QSocketNotifier(socket_descriptor, QSocketNotifier.Read)
    notifier.setEnabled(True)

    def read_socket():
        data= socket.recvfrom(bufferSize)
        # Process the received data and update your UI elements here
        # Emit signals to update UI elements like RPM and speed
        ui.rpm_update_signal.emit(RPM1)
        ui.speed_update_signal.emit(speed1)
        ui.door_update_signal.emit(DS)
        ui.charge_update_signal.emit(charge)
        ui.indicator_update_signal.emit(Indicators)
        ui.temp_update_signal.emit(temp)
        ui.bodyversion_update_signal.emit(bodyversion)
        ui.connectivityversion_update_signal.emit(connectivityversion)







    notifier.activated.connect(read_socket)

    while not exit_event.is_set():
        app.processEvents()

    notifier.setEnabled(False)


class DataUpdater(QObject):
    rpm_update_signal = pyqtSignal(int)
    speed_update_signal = pyqtSignal(int) 
    door_update_signal= pyqtSignal(int)   
    charge_update_signal= pyqtSignal(int)   
    indicator_update_signal= pyqtSignal(int)  
    temp_update_signal= pyqtSignal(int)   
    bodyversion_update_signal= pyqtSignal(int)
    connectivityversion_update_signal= pyqtSignal(int)
 





class Ui_MainWindow(object): 
    global RPM1, speed1, DS
 
    def __init__(self):
        #meow=UDPServer(localIP, localPort)
        #meow.receive_and_respond(self.RPM1)

        self.RPM1 = 0  # Initialize RPM1 with a default value
        self.speed1 = 0 # Initialize speed1 with a default value
        self.DS = 0
        self.charge=0
        self.Indicators=0
        self.temp = 0
        self.bodyversion=0
        self.connectivityversion= 0
        self.data_updater = DataUpdater()
        self.data_updater.rpm_update_signal.connect(self.update)
        self.data_updater.speed_update_signal.connect(self.update)
        self.data_updater.door_update_signal.connect(self.Doorstatus)
        self.data_updater.charge_update_signal.connect(self.chargestatus)
        self.data_updater.indicator_update_signal.connect(self.Indicatorstatus)
        self.data_updater.temp_update_signal.connect(self.Temperaturestatus)
        self.data_updater.bodyversion_update_signal.connect(self.body_version)
        self.data_updater.connectivityversion_update_signal.connect(self.connectivity)

        self.blink_count = 0



    def connectivity(self):
           self.label_101.setStyleSheet("color:#fff;\n"
"font: 9pt \"Calibiri\";\n"
"background:None;")
           self.label_101.setText(self.connectivityversion)  

    def body_version(self):
           self.label_100.setStyleSheet("color:#fff;\n"
"font: 9pt \"Calibiri\";\n"
"background:None;")
           self.label_100.setText(self.bodyversion)  

    def update(self):
        #global RPM1,speed1
        
        self.rpm.update_value(self.RPM1)
        self.speed.update_value(self.speed1)   


    def chargestatus(self):
           print("charge status:", self.charge)
           charges = self.charge
           self.progressBar_2.setProperty("value", charges)


    def Temperaturestatus(self):
           print("temppp :",self.temp)     
           temperature=self.temp
           self.label_44.setStyleSheet("color:#fff;\n"
"font: 14pt \"MS UI Gothic\";\n"
"background:None;")
           self.label_44.setText(str(temperature)+"°C")  

    def startBlinking(self):
        # Start a timer to call Indicatorstatus every, for example, 500 milliseconds.
        self.timer = QTimer()
        self.timer.timeout.connect(self.Indicatorstatus)
        self.timer.start(100)
        print("blibking")

    def stopBlinking(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            print("stopepeed")

    def Indicatorstatus(self):
        print("Updated Indicators  :", self.Indicators)
        indicator=self.Indicators
        #if self.blink_state:
        if (indicator[6] == '1'):
                print('Right Indicator On')
                self.right_indicator.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 8px;")
                self.right_indicator1.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 7px;")
                self.right_indicator2.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 5px;")
        else:
                print('Right Indicator Off') 

        if (indicator[7] == '1'):
                print('Left Indicator On')
                self.left_indicator.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 8px;")
                self.left_indicator1.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 7px;")
                self.left_indicator2.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 5px;") 
        else:
                print('Left Indicator Off')  


        if indicator[6] == '1' or indicator[7] == '1':
            # Increment the blink count.
            self.blink_count += 1

            # If the blink count reaches 5, stop blinking.
            if self.blink_count >= 5:
                self.stopBlinking()




    def Doorstatus(self):
        Doors=str(self.DS)
        if len(Doors) >= 8:

                if (Doors[7] == '1'):
                        print('Front Right Door Open')
                        self.label_5.setStyleSheet("color:green;")
                        self.label_5.setText("Unlocked")
                else:
                        print('Front Right Door Close')
                        self.label_5.setStyleSheet("color:red;")
                        self.label_5.setText("Locked")

                if (Doors[6] == '1'):
                        print('Front Left Door Open')
                        self.label_6.setStyleSheet("color:green;")
                        self.label_6.setText("Unlocked")
                else:
                        print('Front Left Door Close')
                        self.label_6.setStyleSheet("color:red;")
                        self.label_6.setText("Locked")
                if (Doors[5] == '1'):
                        print('Rear Right Door Open')
                        self.label_9.setStyleSheet("color:green;")
                        self.label_9.setText("Unlocked")
                else:
                        print('Rear Right Door Close')
                        self.label_9.setStyleSheet("color:red;")
                        self.label_9.setText("Locked")

                if (Doors[4] == '1'):
                        print('Rear Left Door Open')
                        self.label_4.setStyleSheet("color:green;")
                        self.label_4.setText("Unlocked")
                else:
                        print('Rear Left Door Close')
                        self.label_4.setStyleSheet("color:red;")
                        self.label_4.setText("Locked")

                if (Doors[3] == '1'):
                        print('Trunk Open')
                        self.label_7.setStyleSheet("color:green;")
                        self.label_7.setText("Unlocked")

                else:
                        print('Trunk Close')
                        self.label_7.setStyleSheet("color:red;")
                        self.label_7.setText("Locked")
                if (Doors[2] == '1'):
                        print('Boot Open')
                        self.label_8.setStyleSheet("color:green;")
                        self.label_8.setText("Unlocked")
                else:
                        print('Boot Close')
                        self.label_8.setStyleSheet("color:red;")
                        self.label_8.setText("Locked") 


                if (Doors[2] and Doors[3] and Doors[4] and Doors[5] and Doors[6] and Doors[7] == '0'):
                      self.label_15.setText("Locked")
                else:
                      self.label_15.setText("Unlocked")      
                      


        else:
                print("Invalid input: The string should have at least 8 characters.")    

    def setupUi(self, MainWindow):
        
        #background color
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1117, 636)
        MainWindow.setStyleSheet("background-color: rgb(0, 0,39 )")
        #MainWindow.installEventFilter(self)

        #Background/Border image
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1111, 651))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")


        #Instrument Cluster Framework
        self.frame_dashboard = QtWidgets.QFrame(self.centralwidget)
        self.frame_dashboard.setEnabled(True)
        self.frame_dashboard.setGeometry(QtCore.QRect(70, 120, 971, 411))
        self.frame_dashboard.setStyleSheet("QFrame{\n"
"background-color: rgb(30, 30,80);\n"
"\n"
"border-radius:200px;\n"
"\n"
"}")
        self.frame_dashboard.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dashboard.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dashboard.setObjectName("frame_dashboard")

        #Backend of speedometer
        self.speed = AnalogGaugeWidget(self.frame_dashboard)
        self.speed.setGeometry(QtCore.QRect(30, 50, 311, 281))
        self.speed.setStyleSheet("background-color: rgb(85, 85, 127);\nborder-radius: 0px;")
        self.speed.setObjectName("speed")
        #self.speed1=speed1

        #Backend of RPM gauge
        self.rpm = AnalogGaugeWidget(self.frame_dashboard)
        self.rpm.setGeometry(QtCore.QRect(630, 50, 311, 281))
        self.rpm.setStyleSheet("background-color: rgb(85, 85, 127);\n"
"border-radius:o px;")
        self.rpm.setObjectName("rpm")
        #self.RPM1=RPM1


        #Framework of the car 
        self.car_state = QtWidgets.QFrame(self.frame_dashboard)
        self.car_state.setGeometry(QtCore.QRect(350, 80, 771,750))
        self.car_state.setStyleSheet("background:None;\n"
"color:#ee1111;")
        self.car_state.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.car_state.setFrameShadow(QtWidgets.QFrame.Raised)
        self.car_state.setObjectName("car_state")
        self.label_3 = QtWidgets.QLabel(self.car_state)
        self.label_3.setGeometry(QtCore.QRect(45, 60, 200, 200))
        self.label_3.setStyleSheet("background:None")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./car3.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.car_state)
        self.label_7.setGeometry(QtCore.QRect(118, 260, 90, 16))
        self.label_7.setObjectName("label_7")
        self.label_5 = QtWidgets.QLabel(self.car_state)
        self.label_5.setGeometry(QtCore.QRect(187, 145, 90, 16))
        self.label_5.setObjectName("label_5")

        self.label_4 = QtWidgets.QLabel(self.car_state)
        self.label_4.setGeometry(QtCore.QRect(40, 202, 90, 16))
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.car_state)
        self.label_8.setGeometry(QtCore.QRect(119, 100, 90, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.car_state)
        self.label_9.setGeometry(QtCore.QRect(187, 200, 90, 16))
        self.label_9.setStyleSheet("")
        self.label_9.setObjectName("label_9")
        self.label_6 = QtWidgets.QLabel(self.car_state)
        self.label_6.setGeometry(QtCore.QRect(40, 150, 90, 16))
        self.label_6.setObjectName("label_6")
        self.label_100 = QtWidgets.QLabel(self.frame_dashboard)
        self.label_100.setGeometry(QtCore.QRect(265, 380, 200, 26))
        self.label_100.setStyleSheet("color: white; background: None;")
        font=QFont("Calibiri", 8)
        font.setBold(True)
        self.label_100.setFont(font)
        self.label_100.setObjectName("label_100")

        self.label_101 = QtWidgets.QLabel(self.frame_dashboard)
        self.label_101.setGeometry(QtCore.QRect(525, 380, 200, 26))
        self.label_101.setStyleSheet("color: white; background: None;")

        font=QFont("Calibiri", 8)
        font.setBold(True)
        self.label_101.setFont(font)
        self.label_101.setObjectName("label_101")

        #CHARGE FRAMEWORK

        self.frame_4 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_4.setGeometry(QtCore.QRect(730, 340, 141, 42))
        self.frame_4.setStyleSheet("background-color: rgb(0, 85, 127,130);\n"
"border-radius:15px;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_14 = QtWidgets.QLabel(self.frame_4)
        self.label_14.setStyleSheet("color:#fff;\n"
"font: 12pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_3.addWidget(self.label_14)

        #CHARGE STATUS BAR
        self.progressBar_2 = QtWidgets.QProgressBar(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_2.sizePolicy().hasHeightForWidth())
        self.progressBar_2.setSizePolicy(sizePolicy)
        self.progressBar_2.setMinimumSize(QtCore.QSize(50, 0))
        self.progressBar_2.setStyleSheet("QProgressBar{\n"
"    background-color : rgb(141, 144, 147);\n"
"    \n"
"    color: rgb(0, 0, 0);\n"
"    border-style: none;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"    border-radius: 5px;\n"
"    \n"
"    background-color: rgb(227,162,26,150);\n"
"}")
        self.progressBar_2.setProperty("value", 56)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setInvertedAppearance(False)
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setFormat("")
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout_3.addWidget(self.progressBar_2)

        #SIDEBAR DOOR STATUS FRAMEWORK
        self.frame_5 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_5.setGeometry(QtCore.QRect(100, 340, 141, 42))
        self.frame_5.setStyleSheet("background-color: rgb(152, 57, 38,100);\n"
"border-radius:15px;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_15 = QtWidgets.QLabel(self.frame_5)
        self.label_15.setStyleSheet("color:#fff;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15") 
        self.horizontalLayout_4.addWidget(self.label_15)


        # CAR DOOR STATUS FRAMEWORK

        self.frame_6 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_6.setGeometry(QtCore.QRect(370, 265, 90, 30))
        self.frame_6.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_6)
        self.label_4.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_7 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_7.setGeometry(QtCore.QRect(503, 222, 90, 30))
        self.frame_7.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6= QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.frame_7)
        self.label_5.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_8 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_8.setGeometry(QtCore.QRect(503, 270, 90, 30))
        self.frame_8.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_7")
        self.horizontalLayout_7= QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(self.frame_8)
        self.label_9.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_9 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_9.setGeometry(QtCore.QRect(370, 220, 90, 30))
        self.frame_9.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_7")
        self.horizontalLayout_8= QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.frame_9)
        self.label_6.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_12 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_12.setGeometry(QtCore.QRect(440, 335, 90, 30))
        self.frame_12.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_6")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.frame_12)
        self.label_7.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_13 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_13.setGeometry(QtCore.QRect(440, 120, 90, 30))
        self.frame_13.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_6")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_10.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.frame_13)
        self.label_8.setStyleSheet("color:red;\n"
"font: 10pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)



        #Temperature Framework

        self.frame_15 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_15.setGeometry(QtCore.QRect(455, 60, 60, 60))
        self.frame_15.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.label_44 = QtWidgets.QLabel(self.frame_15)
        self.label_44.setStyleSheet("color:#fff;\n"
"font: 14pt \"MS UI Gothic\";\n"
"background:None;")
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName("label_15") 
        self.horizontalLayout_44.addWidget(self.label_44)


        #INDICATOR

        self.left_indicator = QtWidgets.QLabel(self.car_state)
        self.left_indicator.setGeometry(QtCore.QRect(74, 0, 18, 18))
        self.left_indicator.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 8px;")

        self.left_indicator1 = QtWidgets.QLabel(self.car_state)
        self.left_indicator1.setGeometry(QtCore.QRect(44, 0, 15, 15))
        self.left_indicator1.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 7px;")

        self.left_indicator2 = QtWidgets.QLabel(self.car_state)
        self.left_indicator2.setGeometry(QtCore.QRect(14, 0, 11, 11))
        self.left_indicator2.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 5px;")

        self.right_indicator = QtWidgets.QLabel(self.car_state)
        self.right_indicator.setGeometry(QtCore.QRect(180, 0, 18, 18))
        self.right_indicator.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 8px;")

        self.right_indicator1 = QtWidgets.QLabel(self.car_state)
        self.right_indicator1.setGeometry(QtCore.QRect(210, 0, 15, 15))
        self.right_indicator1.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 7px;")

        self.right_indicator2 = QtWidgets.QLabel(self.car_state)
        self.right_indicator2.setGeometry(QtCore.QRect(240, 0, 11, 11))
        self.right_indicator2.setStyleSheet("background-color: rgb(80, 80, 80); border-radius: 5px;")

        #BODY VERSION
        self.frame_22 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_22.setGeometry(QtCore.QRect(423, 373, 40, 40))
        self.frame_22.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout(self.frame_22)
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.label_43 = QtWidgets.QLabel(self.frame_22)
        self.label_43.setStyleSheet("color:#fff;\n"
"font: 9pt \"Calibiri\";\n"
"background:None;")
        self.label_43.setAlignment(QtCore.Qt.AlignCenter)
        self.label_43.setObjectName("label_15") 
        self.horizontalLayout_43.addWidget(self.label_43)

        #CONNECTIVITY VERSION
        self.frame_23 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_23.setGeometry(QtCore.QRect(655, 373, 40, 40))
        self.frame_23.setStyleSheet("background-color: transparent;\n"
"border-radius:15px;")
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_42 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_42.setObjectName("horizontalLayout_42")
        self.label_42 = QtWidgets.QLabel(self.frame_23)
        self.label_42.setStyleSheet("color:#fff;\n"
"font: 9pt \"Calibiri\";\n"
"background:None;")
        self.label_42.setAlignment(QtCore.Qt.AlignCenter)
        self.label_42.setObjectName("label_15") 
        self.horizontalLayout_42.addWidget(self.label_42)


        MainWindow.setCentralWidget(self.centralwidget)
        self.progress()
        self.update()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.label_km = QLabel(self.speed)
        self.label_km.setText("Km/h")
        self.label_km.setGeometry(QRect(130, 190, 57, 16))
        self.label_km.setStyleSheet(u"\n"
"color:#fff;\n"
"    font: 15pt;\n"
"background:None;\n"
"\n"
)
        self.label_km.setAlignment(Qt.AlignCenter)

    

    def retranslateUi(self, MainWindow):
            translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(translate("CAR DASHBOARD", "MainWindow"))
            self.label_7.setText(translate("MainWindow", "Locked"))
            self.label_5.setText(translate("MainWindow", "Locked"))
            self.label_4.setText(translate("MainWindow", "Locked"))
            self.label_8.setText(translate("MainWindow", "Locked"))
            self.label_9.setText(translate("MainWindow", "Locked"))
            self.label_6.setText(translate("MainWindow", "Locked"))
            self.label_14.setText(translate("MainWindow", "Charge:"))
            self.label_15.setText(translate("MainWindow", "Locked"))
            self.label_44.setText(translate("MainWindow", "25°C"))
            self.label_100.setText(translate("MainWindow", "Body Application Version :"))
            self.label_101.setText(translate("MainWindow", "Connectivity Version :"))
            self.label_43.setText(translate("MainWindow", ""))
            self.label_42.setText(translate("MainWindow", ""))


   

    def progress(self):
            self.speed.set_MaxValue(100)
            self.speed.set_DisplayValueColor(200,200,200)
            self.speed.set_CenterPointColor(255,255,255)
            self.speed.set_NeedleColor(255,255,200)
            self.speed.set_NeedleColorDrag(255,255,255)
            self.speed.set_ScaleValueColor(255,200,255)
            self.speed.set_enable_big_scaled_grid(True)
            self.speed.set_enable_barGraph(False)
            self.speed.set_enable_filled_Polygon(False)


            self.rpm.set_scala_main_count(8)
            self.rpm.set_MaxValue(8)
            self.rpm.set_MinValue(0)

            self.rpm.set_DisplayValueColor(200,200,200)
            self.rpm.set_enable_big_scaled_grid(True)
            self.rpm.set_ScaleValueColor(255,255,255)
            self.rpm.set_NeedleColor(155,155,100)
            self.rpm.set_NeedleColorDrag(255,255,255)
            self.rpm.set_CenterPointColor(255,255,255)
    


class UDPServer:
    def __init__(self, local_ip, local_port, local_ip_version, local_port_version,ui_instance):
        self.local_ip = local_ip
        self.local_port = local_port
        self.local_ip_version = local_ip_version
        self.local_port_version = local_port_version
        self.buffer_size = 1024
        self.exit_event = threading.Event()
        self.RPM1 = 0
        self.speed1 = 0
        self.DS = 0
        self.charge=0
        self.Indicators=0
        self.temp = 0
        self.bodyversion = '0.0'
        self.connectivityversion ='0.0'
        self.ui_instance = ui_instance  # Reference to the Ui_MainWindow instance

    def receive_and_respond(self):
        #global RPM22
        UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPServerSocket.bind((self.local_ip, self.local_port))
        print("UDP server up and listening")

        while not self.exit_event.is_set():
            bytes_address_pair = UDPServerSocket.recvfrom(self.buffer_size)
            message = bytes_address_pair[0]
            address = bytes_address_pair[1]
            message = message.decode()
            client_msg = "Message from client: {}".format(message)
            client_ip = "Client IP Address: {}".format(address)
            print(client_msg)
            print(client_ip)

            if message.startswith('00000101'):  # Reading the RPM header
                RPM_hex = message[-2:]  # checking the LSB of RPM
                print('RPM:', int(RPM_hex, 16))  # converting hex into integer
                self.ui_instance.RPM1=int(RPM_hex, 16)
                self.ui_instance.data_updater.rpm_update_signal.emit(self.ui_instance.RPM1)

                self.RPM1 = int(RPM_hex, 16)
                print("RPM_Updated :",self.RPM1)

            if message.startswith('00000102'): #Reading the speed header
                Speed_hex = message[-2:] #Checking LSB of speed
                print('Speed', int(Speed_hex,16))
                self.ui_instance.speed1=int(Speed_hex, 16)
                self.ui_instance.data_updater.speed_update_signal.emit(self.ui_instance.speed1)
                self.speed1 = int(Speed_hex, 16)
                print("Speed_Upadted :",self.speed1)

            if message.startswith('00000105'): # Reading the Door status
                Door_status = message[-2:]
                Door_status = int(Door_status,16)
                Door_status = bin(Door_status)[2:].zfill(8)
                #DS= Door_status
                self.DS = Door_status
                print("Updated door :",self.DS)
                self.ui_instance.DS=self.DS
                self.ui_instance.data_updater.door_update_signal.emit(self.ui_instance.DS)    


            if (message[:8] == '00000103'):#Reading the charge 
                Charge_hex = message[-2:]
                print('charge', int(Charge_hex,16))
                self.charge=int(Charge_hex,16)
                print("Updated charge :", self.charge)
                self.ui_instance.charge=self.charge
                self.ui_instance.data_updater.charge_update_signal.emit(self.ui_instance.charge) 


            if (message[:8] == '00000106'): # Reading the Indicator status 
                Indicator_status = message[-2:]
                Indicator_status = int(Indicator_status,16)
                Indicator_status = bin(Indicator_status)[2:].zfill(8)
                print (Indicator_status) 
                self.Indicators= Indicator_status
                self.ui_instance.Indicators=self.Indicators
                self.ui_instance.data_updater.indicator_update_signal.emit(self.ui_instance.Indicators)      


            if (message[:8] == '00000104'):
                HVAC_hex = message[-2:] #Checking LSB of speed
                print('HVAC', int(HVAC_hex,16))      
                self.ui_instance.temp=int(HVAC_hex, 16)
                self.ui_instance.data_updater.temp_update_signal.emit(self.ui_instance.temp)
                self.temp = int(HVAC_hex, 16)
                print("HVAC_Upadted :",self.temp)    


            # Rest of your message processing logic...

            if not self.exit_event.is_set():
                UDPServerSocket.sendto(bytesToSend, address)

            #self.RPM1 = int(RPM_hex, 16)
            #self.RPM22=RPM22
        UDPServerSocket.close()


    def version_update(self):
        
        versionServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        versionServerSocket.bind((self.local_ip_version, self.local_port_version))
        print("version server up and listening")
        while not self.exit_event.is_set():
            bytes_address_pair1 = versionServerSocket.recvfrom(self.buffer_size)
            message1 = bytes_address_pair1[0]
            address1 = bytes_address_pair1[1]
            message1 = message1.decode()
            client_msg1 = "Message from client: {}".format(message1)
            client_ip1 = "Client IP Address: {}".format(address1)
            #print(client_msg1)
            #print(client_ip1)
            message_parts = message1.split()
            #print('Container name:', message_parts[0])
            #print('Conatiner Version:', message_parts[1])
            
            if (message_parts[0]=='sender1'):
                self.bodyversion = message_parts[1]
                print("Updated body app version :",self.bodyversion)
                print('Container name:', message_parts[0])
                self.ui_instance.bodyversion=self.bodyversion
                self.ui_instance.data_updater.bodyversion_update_signal.emit(self.ui_instance.bodyversion)            

            if (message_parts[0]=='receiver1'):
                self.connectivityversion = message_parts[1]
                print("Updated connectivity app version :",self.connectivityversion)
                print('Container name:', message_parts[0])
                self.ui_instance.connectivityversion=self.connectivityversion
                self.ui_instance.data_updater.connectivityversion_update_signal.emit(self.ui_instance.connectivityversion)
                
            if not self.exit_event.is_set():
                versionServerSocket.sendto(bytesToSend2, address1)
                
        versionServerSocket.close()
    def start_server(self):
        receiver_thread = threading.Thread(target=self.receive_and_respond)
        version_thread =threading.Thread(target=self.version_update)
        receiver_thread.start()
        version_thread.start()

    def stop_server(self):
        self.exit_event.set()

localIP = "0.0.0.0"
localPort = 5000
msgFromServer = "Hello VM Client\n"
bytesToSend = str.encode(msgFromServer)

localIP_version ="localhost"
localPort_version = 5006
msgFromServer2 = "Hello OTA client\n"
bytesToSend2 = str.encode(msgFromServer2)

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        udp_server = UDPServer(localIP, localPort, localIP_version, localPort_version, ui)
        udp_server.start_server()     
        sys.exit(app.exec_())
