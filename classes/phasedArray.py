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
        
    def add_transmitter(self , distance_between_transmitters ,radius):
        self.transmitters_list.append(Transmitter())
        if(self.geometry == "Linear"):
            self.calcualte_linear_distance(distance_between_transmitters)
        if(self.geometry == "Curvlinear"):
            self.calcualte_angles(distance_between_transmitters , radius)
            
    def remove_transmitter(self , distance_between_transmitters , radius):
        self.transmitters_list.pop()
        if(self.geometry == "Linear"):
            self.calcualte_linear_distance(distance_between_transmitters)
        if(self.geometry == "Curvlinear"):
            self.calcualte_angles(distance_between_transmitters , radius)
            
    def calcualte_linear_distance(self , distance_between_transmitters):
        transmitters_number = len(self.transmitters_list)
        start_x_position = -(transmitters_number - 1) / 2 * distance_between_transmitters
        for trans_num , transmitter in enumerate(self.transmitters_list):
            transmitter.x_posision = start_x_position + trans_num * distance_between_transmitters
            transmitter.y_posision = 0
    
    def calcualte_angles(self , arc_distance_between_transmitters , radius):
        transmitters_number = len(self.transmitters_list)
        delta_theta = arc_distance_between_transmitters / radius
        total_angle = delta_theta * (transmitters_number - 1)
        angles_between_transmitters = np.linspace(-total_angle/2, total_angle/2, transmitters_number)

        for trans_num , transmitter in enumerate(self.transmitters_list):
            transmitter.x_posision = radius * np.cos(angles_between_transmitters[trans_num])
            transmitter.y_posision = radius * np.sin(angles_between_transmitters[trans_num]) + radius