import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QFrame
import numpy as np
from classes.phasedArray import PhasedArray
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class ProfileViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.current_phased_array = PhasedArray()
        # self.setBackground("#1E293B")
        self.current_mode = "Transmitting Mode"
        self.num_of_antennas = 1
        self.frequency = 2
        self.distance_between_recievers = 1
        self.transmitter_position = (50,50)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        
        self.wavelength = 1 / self.frequency
        self.theta = np.linspace(-np.pi, np.pi, 1000) 
        self.phase_shift = 2 * np.pi * self.distance_between_recievers / self.wavelength
        self.k = 2 * np.pi / self.wavelength

    
        self.ax = self.figure.add_subplot(111, polar=True)  
        # self.ax.set_title("Polar Beam Profile", va='bottom')
        self.ax.set_rticks([]) 
        self.ax.set_ylim(0, 1)

        self.animation = FuncAnimation(self.figure, self.update_plot, frames=np.arange(0, 2*np.pi, 0.01), 
                                        init_func=self.init_plot, blit=True, interval=50)

    def init_plot(self):
        self.line, = self.ax.plot([], [], color="b", linewidth=2, label="Beam Profile")
        return self.line,

    def calculate_phase_shift(self, antenna, angle):
        dx = antenna.x_posision - self.transmitter_position[0]
        dy = antenna.y_posision - self.transmitter_position[1]
        distance = np.sqrt(dx**2 + dy**2)

        additional_distance = distance * np.cos(angle)

        return self.k * additional_distance

    def update_plot(self, frame):
        if (self.current_mode == "Recieving Mode"):
            self.frequency = 2
            self.wavelength = 1 / self.frequency
            self.phase_shift = 2 * np.pi * self.distance_between_recievers / self.wavelength
            self.k = 2 * np.pi / self.wavelength
            amplitude = np.zeros_like(self.theta, dtype=np.complex128)
            for antenna in self.current_phased_array.transmitters_list:
                phase_shift = self.calculate_phase_shift(antenna, self.theta)
                amplitude += np.exp(1j * (2 * np.pi * self.frequency * frame - phase_shift))

            intensity = np.abs(amplitude) ** 2  
            normalized_intensity = intensity / np.max(intensity) 
            self.line.set_data(self.theta, normalized_intensity)
            return self.line,
        
        elif(self.current_mode == "Transmitting Mode"):
            self.frequency = 2
            self.wavelength = 1 / self.frequency
            self.phase_shift = 2 * np.pi * self.distance_between_recievers / self.wavelength
            self.k = 2 * np.pi / self.wavelength
            amplitude = np.zeros_like(self.theta, dtype=np.complex128)
            for antenna in self.current_phased_array.transmitters_list:
                phase_shift = self.calculate_phase_shift(antenna, self.theta)
                amplitude += np.exp(1j * (2 * np.pi * self.frequency * frame - phase_shift))

            intensity = np.abs(amplitude) ** 2  
            normalized_intensity = intensity / np.max(intensity) 
            self.line.set_data(self.theta, normalized_intensity)
            return self.line,


    # def update_plot(self):
    #     self.clear()
    #     angles_list = np.linspace(-90, 90, 500)
    #     angles_radian = np.radians(angles_list)
    #     wave_lengh = 3e8 / self.current_phased_array.current_frequency
    #     k = 2 * np.pi/wave_lengh
    #     number_of_transmitters = len(self.current_phased_array.transmitters_list)
    #     distance = self.current_phased_array.distance
    #     transmitters_positions = np.array([[transmitter.x_posision, transmitter.y_posision] for transmitter in self.current_phased_array.transmitters_list]) 
    #     beam_profile = []
    #     for theta in angles_radian:
    #         phase_shifts = k*(transmitters_positions[:,0] * np.cos(theta) + transmitters_positions[:, 1]*np.sin(theta))
    #         combined_field = np.sum(np.exp(1j * phase_shifts))
    #         beam_profile.append(np.abs(combined_field)**2)
    #     beam_profile = np.array(beam_profile)/np.max(beam_profile)
    #     self.plot(angles_list, beam_profile)
            
            ##idea for the new year , apply the modulation effect
                
