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
        
    def add_transmitter(self , distance_between_transmitters):
        self.transmitters_list.append(Transmitter())
        self.calcualte_distance(distance_between_transmitters)
    
    def remove_transmitter(self , distance_between_transmitters):
        self.transmitters_list.pop()
        self.calcualte_distance(distance_between_transmitters)
        
    def calcualte_distance(self , distance_between_transmitters):
        transmitters_number = len(self.transmitters_list)
        start_x_position = -(transmitters_number - 1) / 2 * distance_between_transmitters
        for trans_num , transmitter in enumerate(self.transmitters_list):
            transmitter.x_posision = start_x_position + trans_num * distance_between_transmitters
        
