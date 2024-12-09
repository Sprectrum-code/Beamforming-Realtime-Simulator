class Controller():
    def __init__(self, phased_array, beam_viewer, profile_viewer):
        self.phased_array = phased_array
        self.beam_viewer = beam_viewer
        self.profile_viewer = profile_viewer
        
        
    def set_current_beam(self):
        self.beam_viewer.update_map()
        self.profile_viewer.update_plot()