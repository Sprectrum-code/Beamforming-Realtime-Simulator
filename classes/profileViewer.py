import pyqtgraph as pg
import numpy as np
from classes.phasedArray import PhasedArray

class ProfileViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.current_phased_array = PhasedArray()
        self.setBackground("#1E293B")
        
        
    def update_plot(self):
        self.clear()
        angles_list = np.linspace(-90, 90, 500)
        angles_radian = np.radians(angles_list)
        wave_lengh = 3e8 / self.current_phased_array.current_frequency
        k = 2 * np.pi/wave_lengh
        number_of_transmitters = len(self.current_phased_array.transmitters_list)
        distance = self.current_phased_array.distance
        transmitters_positions = np.array([[transmitter.x_posision, transmitter.y_posision] for transmitter in self.current_phased_array.transmitters_list]) 
        beam_profile = []
        for theta in angles_radian:
            phase_shifts = k*(transmitters_positions[:,0] * np.cos(theta) + transmitters_positions[:, 1]*np.sin(theta))
            combined_field = np.sum(np.exp(1j * phase_shifts))
            beam_profile.append(np.abs(combined_field)**2)
        beam_profile = np.array(beam_profile)/np.max(beam_profile)
        self.plot(angles_list, beam_profile)
            
            ##idea for the new year , apply the modulation effect
                
