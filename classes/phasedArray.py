import numpy as np
from classes.transmetter import Transmitter
class PhasedArray():
    def __init__(self):
        self.current_frequency = 1
        self.transmitters_list = [Transmitter()]
        self.phase_shift = 0
        self.geometry = "Linear"
        self.distance = 1
        self.radius = 1
        self.current_x_range = 20
        self.current_y_range = 20
        self.x_grid_size = 1000
        self.y_grid_size = 1000
        self.wave_map = np.zeros((1000, 1000))
        
    
            
        