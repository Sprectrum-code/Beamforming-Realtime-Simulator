import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication
from classes.phasedArray import PhasedArray

class BeamViewer(pg.ImageView):
    def __init__(self):
        super().__init__()
        self.current_phased_array = PhasedArray()
        self.getView().setBackgroundColor("#1E293B")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.getView().invertY(False)
        self.getView().setAspectLocked(False)
        
    def update_map(self):
        self.clear()
        x_line = np.linspace(-self.current_phased_array.current_x_range, self.current_phased_array.current_x_range, self.current_phased_array.x_grid_size)
        y_line = np.linspace(0, self.current_phased_array.current_y_range, self.current_phased_array.y_grid_size)
        x_mesh, y_mesh = np.meshgrid(x_line,y_line)
        amplitude = np.zeros_like(x_mesh)
        for i, transmitter in enumerate(self.current_phased_array.transmitters_list):
            distance = np.sqrt((x_mesh - transmitter.x_posision)**2 + (y_mesh - transmitter.y_posision)**2)
            amplitude += np.sin(self.current_phased_array.current_frequency *2*np.pi *distance + (i+1)*self.current_phased_array.phase_shift)
        self.current_phased_array.wave_map = amplitude
        self.setImage(amplitude.T)
        self.getView().autoRange()
            

        # # Transmitter position and grid setup
        # x_t, y_t = 0, 0  # Transmitter at the origin
        # grid_size = 1000  # Size of the grid (nxn)
        # n = grid_size

        # # Create a fine-grained grid for X and Y coordinates
        # x = np.linspace(0, 1000, 2000)
        # y = np.linspace(0, 50, 1000)
        # X, Y = np.meshgrid(x, y)

        # self.getView().autoRange()  # Automatically fit the view to the image

        # # Sine wave parameters
        # k = 1  # Transmitter strength
        # omega = 2 * np.pi * 50  # Frequency of the sine wave (50 Hz)
        # t = 1  # Time (can animate this for oscillations)
        # phi = 0  # Phase offset

        # # Initialize a blank image (n x n array) with zeros
        # amplitude = np.zeros((n, n))

        # # Loop through each pixel and compute its value
        # for i in range(n):
        #     for j in range(n):
        #         distance = np.sqrt((X[i, j] - x_t)**2 + (Y[i, j] - y_t)**2 + 1e-6)  # Avoid division by zero
        #         amplitude[i, j] = np.sin(omega * t + phi + distance)  # Calculate the sine wave amplitude for the pixel

        # # Normalize the amplitude to [-1, 1] range
        # amplitude = k * amplitude / np.max(np.abs(amplitude))

        # # Set the computed image as the displayed image
        # self.setImage(amplitude)

        # # Adjust view to fit the image (automatic scaling)
        # self.getView().autoRange()

        # # Show the image in the window
        # self.show()