class Controller():
    def __init__(self, phased_array, beam_viewer):
        self.phased_array = phased_array
        self.beam_viewer = beam_viewer
        
        
    def set_current_beam(self):
        self.beam_viewer.update_map()
        
    def add_transmitter(self ,distance_between_transmitters , circle_radius):
        self.phased_array.add_transmitter(distance_between_transmitters , circle_radius)
        self.set_current_beam()
    
    def remove_transmitter(self ,distance_between_transmitters , circle_radius):
        self.phased_array.remove_transmitter(distance_between_transmitters , circle_radius)
        self.set_current_beam()
    
    def calculate_linear_distance(self , distance_between_transmitters):
        self.phased_array.calcualte_linear_distance(distance_between_transmitters)
        self.set_current_beam()
        
        
    def calcualte_angles(self ,distance_between_transmitters ,circle_radius ):
        self.phased_array.calcualte_angles(distance_between_transmitters , circle_radius)
        self.set_current_beam()
        
        
