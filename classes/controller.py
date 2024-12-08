class Controller():
    def __init__(self, phased_array, beam_viewer):
        self.phased_array = phased_array
        self.beam_viewer = beam_viewer
        
        
    def set_current_beam(self):
        self.beam_viewer.update_map()