import pyqtgraph as pg

class ProfileViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.current_phased_array = []
        self.setBackground("#1E293B")
        