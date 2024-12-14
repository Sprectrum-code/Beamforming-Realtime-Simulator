import numpy as np
from classes.transmetter import Transmitter
from classes.reciver import Reciver
import logging
class PhasedArray():
    def __init__(self):
        self.current_frequency = 1
        self.transmitters_list = [Transmitter()]
        self.phase_shift = 0
        self.reciver_phase_shift = 0
        self.geometry = "Linear"
        self.distance = 1
        self.radius = 1
        self.current_x_range = 20
        self.current_y_range = 20
        self.x_grid_size = 1000
        self.y_grid_size = 1000
        self.wave_map = np.zeros((1000, 1000))
        self.current_mode = "Transmitting Mode"
        self.logger = logging.getLogger(self.__class__.__name__)

        
    def add_transmitter(self , distance_between_transmitters ,radius):
<<<<<<< HEAD
        try: 
            if self.current_mode == "Transmitting Mode":
                self.transmitters_list.append(Transmitter())
                self.logger.info(f'New transmitter added successfully')

                if(self.geometry == "Linear"):
                    self.calcualte_linear_distance(distance_between_transmitters)
                
                if(self.geometry == "Curvlinear"):
                    self.calcualte_angles(distance_between_transmitters , radius)
            else:
                self.transmitters_list.append(Reciver())
                self.logger.info(f'New reciever added successfully')

                if(self.geometry == "Linear"):
                    self.calcualte_linear_distance(distance_between_transmitters)
                if(self.geometry == "Curvlinear"):
                    self.calcualte_angles(distance_between_transmitters , radius)
        except Exception as e:
            self.logger.error(f'adding new transmitter/reciver caused an error {e}')
                   
=======
        if self.current_mode == "Transmitting Mode":
            self.transmitters_list.append(Transmitter())
            if(self.geometry == "Linear"):
                self.calcualte_linear_distance(distance_between_transmitters)
            if(self.geometry == "Curvlinear"):
                self.calcualte_angles(distance_between_transmitters , radius)
        else:
            self.transmitters_list.append(Reciver())
            # if(self.geometry == "Linear"):
            self.calcualte_linear_distance(distance_between_transmitters)
            # if(self.geometry == "Curvlinear"):
            #     self.calcualte_angles(distance_between_transmitters , radius)
            
>>>>>>> 8154b9e8c3c9f71e9c197dcb8cf9a45031665679
    def remove_transmitter(self , distance_between_transmitters , radius):
        if len(self.transmitters_list) > 0 :
            self.transmitters_list.pop()
            self.logger.info(f'removing a transmitter, new number of tranmiters is{len(self.transmitters_list)}')
        else: self.logger.warning('There are no transmitters')
        
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
        self.logger.info(f'Transmitters linear distances updated starting from {start_x_position}')
    
    def calcualte_angles(self , arc_distance_between_transmitters , radius):
        transmitters_number = len(self.transmitters_list)
        delta_theta = arc_distance_between_transmitters / radius
        total_angle = delta_theta * (transmitters_number - 1)
        angles_between_transmitters = np.linspace(-total_angle/2, total_angle/2, transmitters_number)

        for trans_num , transmitter in enumerate(self.transmitters_list):
            transmitter.x_posision = radius * np.cos(angles_between_transmitters[trans_num])
            transmitter.y_posision = radius * np.sin(angles_between_transmitters[trans_num]) + radius
        self.logger.info(f'Transmitters angles distances updated with delta theta {delta_theta}')
