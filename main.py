import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QVBoxLayout, QSlider, QComboBox, QPushButton, QStackedWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *
from classes.BeamViewer import BeamViewer
from classes.phasedArray import PhasedArray
from classes.controller import Controller
from classes.profileViewer import ProfileViewer
from copy import deepcopy
import numpy as np
from classes.transmetter import Transmitter
from classes.reciver import Reciver
import logging
compile_qrc()

logging.basicConfig(
    filename='app.log',
    filemode='a',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Beam Forming')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
        self.logger = logging.getLogger(self.__class__.__name__)

        logoPixmap = QPixmap('icons_setup\icons\logo2.png')

        self.logoLabel = self.findChild(QLabel, 'logoLabel')
        self.logoLabel.setPixmap(logoPixmap)
        self.logoLabel.setAlignment(Qt.AlignCenter) 

        self.modesStack = self.findChild(QStackedWidget, 'modesStack')
        self.modesStack.setCurrentIndex(1)
        
        self.transmitterRecieverModes = self.findChild(QComboBox, 'comboBox_2') 
        self.transmitterRecieverModes.currentIndexChanged.connect(self.change_mode)


        self.constructive_map_viewer_frame = self.findChild(QFrame,"constructiveMapFrame")
        self.constructive_map_viewer_frame_layout = QVBoxLayout()
        self.constructive_map_viewer_frame.setLayout(self.constructive_map_viewer_frame_layout)
        self.beam_Viewer = BeamViewer()
        self.constructive_map_viewer_frame_layout.addWidget(self.beam_Viewer)
        
        self.profile_viewer_frame = self.findChild(QFrame,"profileViewerFrame")
        self.profile_viewer_frame_layout = QVBoxLayout()
        self.profile_viewer_frame.setLayout(self.profile_viewer_frame_layout)
        self.profile_viewer = ProfileViewer()
        self.profile_viewer_frame_layout.addWidget(self.profile_viewer)
        
        self.phased_array = PhasedArray()
        self.phase_shift_slider = self.findChild(QSlider, "shiftSlider")
        self.phase_shift_values = [(i * np.pi * 2)/30 for i in range(-30//2, (30+1)//2)]
        self.phase_shift_slider.setMinimum(0)
        self.phase_shift_slider.setMaximum(30)
        self.phase_shift_slider.setValue(15)
        self.phase_shift_slider.valueChanged.connect(self.change_phase)
        
        self.reciver_phase_shift_slider = self.findChild(QSlider, "shiftRecievingSlider")
        self.reciver_phase_shift_slider.setMinimum(0)
        self.reciver_phase_shift_slider.setMaximum(30)
        self.reciver_phase_shift_slider.setValue(15)
        self.reciver_phase_shift_slider.valueChanged.connect(self.change_reciver_phase)
        
        
        self.frequency_slider = self.findChild(QSlider, "frequencySlider")
        self.frequency_slider.setMinimum(0)
        self.frequency_slider.setMaximum(20)
        self.frequency_slider.valueChanged.connect(self.change_frequency)
        
        self.frequency_receiving_mode_slider = self.findChild(QSlider, "transmitterFrequencySlider")
        self.frequency_receiving_mode_slider.setMinimum(0)
        self.frequency_receiving_mode_slider.setMaximum(19)
        self.frequency_receiving_mode_slider.valueChanged.connect(self.change_receivers_mode_frequency)
        
        self.frequency_receiving_mode_label  = self.findChild(QLabel, "label_23")
        
        self.distance_slider = self.findChild(QSlider, "distanceSlider")
        self.distance_slider.setMinimum(0)
        self.distance_slider.setMaximum(20)
        self.distance_slider.valueChanged.connect(self.set_distance_between_transmitters)
        self.number_of_transmetters_label = self.findChild(QLabel, "number_of_transmetters_label")
        self.number_of__recievers_label = self.findChild(QLabel, "recieversNumberLabel")
        
        self.add_transmitter_button = self.findChild(QPushButton , "plusButton")
        self.add_transmitter_button.clicked.connect(self.add_transmitter)
        
        self.add_reciever_button = self.findChild(QPushButton , "plusRecievingButton")
        self.add_reciever_button.clicked.connect(self.add_reciever)
        
        self.remove_transmitter_button = self.findChild(QPushButton , "minusButton")
        self.remove_transmitter_button.clicked.connect(self.remove_transmitter)
        
        self.remove_reciever_button = self.findChild(QPushButton , "minusRecievingButton")
        self.remove_reciever_button.clicked.connect(self.remove_reciever)
        
        # self.mode_combobox = self.findChild(QComboBox , "comboBox")
        # self.mode_combobox.currentIndexChanged.connect(self.set_mode)
        
        self.radius_slider = self.findChild(QSlider , "radiusSlider")
        self.radius_slider.setRange(1,10)
        self.radius_slider.sliderMoved.connect(self.set_radius)
        
        self.mode_combobox = self.findChild(QComboBox , "comboBox")
        self.mode_combobox.currentIndexChanged.connect(self.set_mode)
        # self.mode_combobox.currentText()

        self.radius_frame = self.findChild(QFrame, "radiusFrame")
        self.radius_frame.hide()
        
        self.radius_slider = self.findChild(QSlider , "radiusSlider")
        self.radius_slider.setRange(1,10)
        self.radius_slider.valueChanged.connect(self.set_radius)
        
        self.reciver_distance_slider = self.findChild(QSlider, "distanceRecievingSlider")
        self.reciver_distance_slider.setMinimum(0)
        self.reciver_distance_slider.setMaximum(20)
        self.reciver_distance_slider.valueChanged.connect(self.set_distance_between_transmitters)
        
        self.phase_shift_receiving_label = self.findChild(QLabel, "shiftRecievingLabel")
        self.distance_recievers_label = self.findChild(QLabel, "label_20")
        self.phase_shift_label = self.findChild(QLabel, "shiftLabel")
        self.distance_transmitters_label = self.findChild(QLabel, "distanceLabel")
        self.frequency_label = self.findChild(QLabel, "frequencyLabel")
        self.radius_label = self.findChild(QLabel, "radiusLabel")
        
        
        self.loadScenario = self.findChild(QPushButton, 'loadScenario')
        self.loadScenario.clicked.connect(self.load_scenario)

        self.scenarioComboBox = self.findChild(QComboBox, 'scenarioComboBox')
        self.scenarioComboBox.currentIndexChanged.connect(self.load_scenarios)
        
        self.controller = Controller(self.phased_array,self.beam_Viewer,self.profile_viewer)
        self.controller.phased_array = self.phased_array
        self.controller.beam_viewer = self.beam_Viewer
        self.controller.profile_viewer = self.profile_viewer
        self.controller.mode_box = self.transmitterRecieverModes
        self.beam_Viewer.current_phased_array = self.phased_array
        self.profile_viewer.current_phased_array = self.phased_array
        self.number_of_transmetters_label.setText('1')
        self.controller.set_current_beam()
        
    def change_frequency(self):
        new_frequency = self.get_frquency_slider_position()
        self.phased_array.current_frequency = deepcopy(new_frequency)
        self.controller.set_current_beam()
        self.frequency_label.setText(str(new_frequency))
        self.logger.info(f"Frequency changed to {new_frequency}")
        
    def change_receivers_mode_frequency(self):
        new_frequency = self.get_frquency_slider_position(2)
        self.phased_array.current_frequency = deepcopy(new_frequency)
        self.controller.set_current_beam()
        self.frequency_receiving_mode_label.setText(str(new_frequency))
        self.logger.info(f"frequency changed to {new_frequency}")
        
    def change_phase(self):
        new_phase = self.phase_shift_values[self.phase_shift_slider.value()]
        self.phased_array.phase_shift = deepcopy(new_phase)
        self.controller.set_current_beam()
        self.phase_shift_label.setText(f"{new_phase / np.pi:.1f}")
        self.logger.info(f"Transmitters phase shift changed to {new_phase}")
        
    def change_reciver_phase(self):
        new_phase = self.phase_shift_values[self.reciver_phase_shift_slider.value()]
        self.phased_array.reciver_phase_shift = deepcopy(new_phase)
        self.controller.set_current_beam()
        self.phase_shift_receiving_label.setText(f"{new_phase / np.pi:.1f}")
        self.logger.info(f"Receivers phase shift changed to {new_phase}")

    def set_mode(self , new_mode_index):
        if(new_mode_index == 0):
            self.controller.phased_array.geometry = "Linear"
            self.radius_frame.hide()
            self.logger.info("Changed the Transmitters' mode to Linear")
            
        elif(new_mode_index == 1):
            self.controller.phased_array.geometry = "Curvlinear"
            self.logger.info("Changed the Transmitters' mode to Curvlinear")
            self.radius_frame.show()
        self.add_transmitter()
        self.remove_transmitter()
        self.controller.set_current_beam()

    def set_distance_between_transmitters(self):
        distance_between_transmitters = self.get_distance_slider_position()
        circle_radius = self.radius_slider.sliderPosition()
        if self.transmitterRecieverModes.currentText() == "Transmitting Mode":
            if(self.controller.phased_array.geometry == "Linear"):
                self.controller.calculate_linear_distance(distance_between_transmitters)
            elif (self.controller.phased_array.geometry == "Curvlinear"):
                self.controller.calcualte_angles(distance_between_transmitters ,circle_radius )
            self.distance_transmitters_label.setText(f"{distance_between_transmitters}")
            self.logger.info(f"Changed the distance between transmitters to {distance_between_transmitters}")

        else:
            self.controller.calculate_linear_distance(distance_between_transmitters)
            self.distance_recievers_label.setText(str(distance_between_transmitters))
            self.logger.info(f"Changed the distance between recievers to {distance_between_transmitters}")
    
    def set_radius(self):
        circle_radius = self.radius_slider.sliderPosition()
        self.controller.phased_array.radius = circle_radius
        distance_between_transmitters = self.get_distance_slider_position()
        if(self.controller.phased_array.geometry == "Linear"):
            pass
        elif (self.controller.phased_array.geometry == "Curvlinear"):
            self.controller.phased_array.calcualte_angles(distance_between_transmitters , circle_radius)
        self.controller.set_current_beam()
        self.radius_label.setText(str(circle_radius))
        self.logger.info(f"Changed the radius of transmitters' circle to {circle_radius}")

    def add_transmitter(self):
        circle_radius = self.radius_slider.sliderPosition()
        distance_between_transmitters = self.get_distance_slider_position()
        self.number_of_transmetters_label.setText(f'{str(int(self.number_of_transmetters_label.text()) + 1)}')
        self.controller.add_transmitter(distance_between_transmitters , circle_radius)
        
    def add_reciever(self):
        # circle_radius = self.radius_slider.sliderPosition()
        distance_between_transmitters = self.get_distance_slider_position()
        self.number_of__recievers_label.setText(f'{str(int(self.number_of__recievers_label.text()) + 1)}')
        self.controller.add_transmitter(distance_between_transmitters , 0)
            
    def remove_transmitter(self):
        if int(self.number_of_transmetters_label.text()) > 0:
            circle_radius = self.radius_slider.sliderPosition()
            distance_between_transmitters = self.get_distance_slider_position()
            self.number_of_transmetters_label.setText(f'{str(int(self.number_of_transmetters_label.text()) - 1)}')
            self.controller.remove_transmitter(distance_between_transmitters ,circle_radius)
        
    def remove_reciever(self):
        # circle_radius = self.radius_slider.sliderPosition()
        if int(self.number_of__recievers_label.text()) > 0:
            distance_between_transmitters = self.get_distance_slider_position()
            self.number_of__recievers_label.setText(f'{str(int(self.number_of__recievers_label.text()) - 1)}')
            self.controller.remove_transmitter(distance_between_transmitters ,0)
        
    def get_distance_slider_position(self):
        list_of_lambda_ratios = [(i/8) for i in range(0,21)]
        # print(list_of_lambda_ratios[self.distance_slider.value()])
        if self.transmitterRecieverModes.currentText() == "Transmitting Mode":
            return list_of_lambda_ratios[self.distance_slider.value()]
        else:
            return list_of_lambda_ratios[self.reciver_distance_slider.value()]
    
    def get_frquency_slider_position(self, index = 1):
        list_of_frequencies = [i for i in range(1,21)]
        if index == 2:
            return list_of_frequencies[self.frequency_receiving_mode_slider.value()]
        return list_of_frequencies[self.frequency_slider.value()]

    def change_mode(self):
        if self.transmitterRecieverModes.currentText() == 'Transmitting Mode':
            self.modesStack.setCurrentIndex(1)
            self.logger.info("Changed the Program mode to Transmitting")
        if self.transmitterRecieverModes.currentText() == 'Recieving Mode':
            self.modesStack.setCurrentIndex(0)
            self.logger.info("Changed the Program mode to Receiving")
            
        self.controller.phased_array.transmitters_list.clear()
            
        if self.transmitterRecieverModes.currentText() == 'Transmitting Mode':
            self.phased_array.transmitters_list.append(Transmitter())
            self.number_of_transmetters_label.setText('1')
        else:
            self.phased_array.transmitters_list.append(Reciver())
            self.number_of__recievers_label.setText('1')
        self.controller.set_current_beam()


    def load_scenario(self):
        self.controller.phased_array.transmitters_list.clear()
        for _ in range(4):
            self.controller.add_transmitter(0.5, 0)
        
        self.reciver_distance_slider.setValue(2)
        self.number_of__recievers_label.setText('4')
        self.controller.set_current_beam()

    def load_scenarios(self):
        if self.scenarioComboBox.currentText() == 'Tumor Ablation':
            self.controller.phased_array.geometry = "Curvlinear"
            self.radius_frame.show()
            self.radius_slider.setValue(16)
            self.distance_slider.setValue(2)
            self.number_of_transmetters_label.setText('16')
            self.set_radius()
            self.controller.phased_array.current_frequency = 1
            self.frequency_slider.setValue(0)
            self.controller.phased_array.transmitters_list.clear()
            self.mode_combobox.setCurrentIndex(1)
            for _ in range(16):
                self.controller.add_transmitter(0.5, 10)
            self.controller.set_current_beam()

        if self.scenarioComboBox.currentText() == 'Ultrasound':
            self.controller.phased_array.geometry = "Linear"
            self.radius_frame.hide()
            self.controller.phased_array.current_frequency = 1
            self.frequency_slider.setValue(0)
            self.distance_slider.setValue(2)
            self.number_of_transmetters_label.setText('4')
            self.set_distance_between_transmitters()
            self.controller.phased_array.transmitters_list.clear()
            for _ in range(4):
                self.controller.add_transmitter(0.5, 0)
            self.controller.set_current_beam()

        if self.scenarioComboBox.currentText() == 'Custom':
            self.controller.phased_array.geometry = "Linear"
            self.radius_frame.hide()
            self.controller.phased_array.current_frequency = 1
            self.frequency_slider.setValue(0)
            self.distance_slider.setValue(0)
            self.number_of_transmetters_label.setText('1')
            self.set_distance_between_transmitters()
            self.controller.phased_array.transmitters_list.clear()
            self.controller.add_transmitter(0.5, 0)
            self.controller.set_current_beam()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())