import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication
from classes.phasedArray import PhasedArray
from classes.transmetter import Transmitter
import logging
class BeamViewer(pg.ImageView):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.current_phased_array = PhasedArray()
        self.transmitter_positions= []
        self.getView().setBackgroundColor("#1E293B")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.getView().invertY(False)
        self.getView().setAspectLocked(False)
        self.current_mode = "Transmitting Mode"
        
    def update_map(self):
        self.clear()
        x_line = np.linspace(-self.current_phased_array.current_x_range, self.current_phased_array.current_x_range, self.current_phased_array.x_grid_size)
        y_line = np.linspace(0, self.current_phased_array.current_y_range, self.current_phased_array.y_grid_size)
        x_mesh, y_mesh = np.meshgrid(x_line,y_line)
        amplitude = np.zeros_like(x_mesh)
        self.clear_red_dots()
        print(self.current_mode)
        self.logger.info(f'updating the map with current mode {self.current_mode}')
        
        if self.current_mode == "Transmitting Mode":
            for i, transmitter in enumerate(self.current_phased_array.transmitters_list):
                distance = np.sqrt((x_mesh - transmitter.x_posision)**2 + (y_mesh - transmitter.y_posision)**2)
                amplitude += np.sin(self.current_phased_array.current_frequency *2*np.pi + i*self.current_phased_array.phase_shift + 2*np.pi*self.current_phased_array.current_frequency*distance)
                # if(self.current_phased_array.geometry == "Linear"):
                scaled_x = (transmitter.x_posision * (self.current_phased_array.x_grid_size/2)/self.current_phased_array.current_x_range) + self.current_phased_array.x_grid_size/2
                scaled_y = transmitter.y_posision * (self.current_phased_array.y_grid_size)/self.current_phased_array.current_y_range
                self.add_red_dot(scaled_x, scaled_y)
        else:# this can be not static 
            temp_transmitter = Transmitter()
            temp_transmitter.x_posision = 50
            temp_transmitter.y_posision = 50
            distance = np.sqrt((x_mesh - temp_transmitter.x_posision)**2 + (y_mesh - temp_transmitter.y_posision)**2)
            amplitude += np.sin(2 *2*np.pi + 2*np.pi*2*distance)
            for reciever in self.current_phased_array.transmitters_list:
                scaled_x = (reciever.x_posision * (self.current_phased_array.x_grid_size/2)/self.current_phased_array.current_x_range) + self.current_phased_array.x_grid_size/2
                scaled_y = reciever.y_posision * (self.current_phased_array.y_grid_size)/self.current_phased_array.current_y_range
                self.add_red_dot(scaled_x, scaled_y)
            
        colormap = pg.ColorMap([0 ,0.5 , 1], [(255, 0, 0), (0, 0, 255), (255, 0, 0)])
            
            
        self.current_phased_array.wave_map = amplitude
        amplitude_normalized = (amplitude - np.min(amplitude)) / (np.max(amplitude) - np.min(amplitude))
        image  = pg.ImageItem(amplitude_normalized.T)
        image.setLookupTable(colormap.getLookupTable())

        self.getView().addItem(image)

        colorbar = pg.ColorBarItem(
            values=(-1, 1),  # Range of the color scale
            colorMap=colormap,  # The colormap to use
            width=20  # Width of the color bar
        )
        
        # Add the color bar to the layout
        colorbar.axis.setScale(-1)
        colorbar.setMinimumHeight(800)
        self.getView().addItem(colorbar)
        # self.image.setLookupTable(colormap.getLookupTable())
        self.getView().autoRange()
            
    def add_red_dot(self , x,y):
        scatter = pg.ScatterPlotItem(
            pos=np.array([[x, y]]),  
            size=15,               
            brush=pg.mkBrush('g'), 
            pen=None               
        )
        scatter.setZValue(100)
        self.getView().addItem(scatter)
        self.transmitter_positions.append(scatter)
        
    def clear_red_dots(self):
        for red_dot in self.transmitter_positions:
            self.getView().removeItem(red_dot)
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
        
        
        
        # Not USED Piece of Codes
        # (transmitter.x_posision * (self.current_phased_array.x_grid_size/2)/self.current_phased_array.current_x_range) + self.current_phased_array.x_grid_size/2 ,
        #                      transmitter.y_posision * (self.current_phased_array.y_grid_size/2)/self.current_phased_array.current_y_range