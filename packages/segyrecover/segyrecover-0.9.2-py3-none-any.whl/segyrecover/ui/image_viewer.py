"""Image loading and ROI handling for SEGYRecover."""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from .dialogs import ROISelectionDialog

def display_segy_results(segy_path, parent=None):
    """Display SEGY section and amplitude spectrum."""
    try:
        import seisio
        import seisplot

        # Get base name
        base_name = os.path.splitext(os.path.basename(segy_path))[0]

        # 1. Display SEGY Section
        seis_window = QDialog(parent)
        seis_window.setWindowTitle('Digitized SEGY')        
        seis_window.setGeometry(510, 550, 600, 400)

        # Create layout and canvas
        layout = QVBoxLayout(seis_window)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        seis_canvas = FigureCanvas(fig)

        # Load and plot SEGY data
        sio = seisio.input(segy_path)
        dataset = sio.read_all_traces()
        seis = dataset["data"]
        seisplot.plot(seis, 
                    perc=99, 
                    haxis="tracf", 
                    hlabel="Trace no.", 
                    vlabel="Time (ms)",
                    ax=ax)  

        layout.addWidget(seis_canvas)
        layout.addWidget(NavigationToolbar(seis_canvas, seis_window))
        seis_window.show()
        seis_canvas.draw()

        return seis_window
    except Exception as e:
        print(f"Error displaying SEGY results: {str(e)}")
        return None

def display_amplitude_spectrum(filtered_data, dt, parent=None):
    """Display amplitude spectrum window."""
    try:
        # Display Amplitude Spectrum
        spectrum_window = QDialog(parent)
        spectrum_window.setWindowTitle('Average Amplitude Spectrum')    
        spectrum_window.setGeometry(1120, 550, 500, 400)

        # Create layout and canvas
        spectrum_layout = QVBoxLayout(spectrum_window)
        spectrum_canvas = FigureCanvas(plt.figure())
        spectrum_ax = spectrum_canvas.figure.add_subplot(111)

        # Calculate and plot spectrum
        fs = 1 / (dt / 1000)
        fs_filtered = np.zeros(filtered_data.shape, dtype=complex)
        for i in range(filtered_data.shape[1]):
            fs_filtered[:,i] = np.fft.fft(filtered_data[:,i])

        freqs = np.fft.fftfreq(filtered_data.shape[0], 1/fs)
        fsa_filtered = np.mean(np.abs(fs_filtered), axis=1)
        fsa_filtered = fsa_filtered/np.max(fsa_filtered)

        pos_freq_mask = freqs >= 1
        spectrum_ax.plot(freqs[pos_freq_mask], fsa_filtered[pos_freq_mask], 'r')
        spectrum_ax.set_xlim(0, 100)  
        spectrum_ax.set_xlabel('Frequency (Hz)')
        spectrum_ax.set_ylabel('Normalized Amplitude')
        spectrum_ax.set_title('Averaged Amplitude Spectrum') 
        spectrum_ax.grid(True)

        spectrum_layout.addWidget(spectrum_canvas)
        spectrum_layout.addWidget(NavigationToolbar(spectrum_canvas, spectrum_window))
        spectrum_window.show()
        spectrum_canvas.draw()

        return spectrum_window
    except Exception as e:
        print(f"Error displaying amplitude spectrum: {str(e)}")
        return None


class ImageLoader:
    """Handles image loading and display functionality"""
    def __init__(self, parent, console, work_dir):
        self.parent = parent
        self.console = console
        self.work_dir = work_dir
        self.image_path = None
        self.img_array = None
        self.image_window = None
        self.location_window = None
        self.image_canvas = None
        self.plot_location_canvas = None

    def load_image(self):
        """Load and display image with geometry"""
        # Start in the IMAGES folder of the script directory
        images_dir = os.path.join(self.work_dir, "IMAGES")
        
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select Seismic Image File",
            images_dir,  # Now starting in IMAGES folder
            "Image Files (*.tif *.jpg *.png);;All Files (*.*)"
        )
        
        if not file_path:
            return False

        img_array = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img_array is None:
            QMessageBox.warning(self.parent, "Error", "Could not load image.")
            return False

        self.image_path = file_path
        self.img_array = img_array

        self.image_window = self._create_image_window()  
        self.location_window = self._create_location_window()
        
        # Load and display geometry data
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        self._load_geometry_data(base_name)
            
        self.console.append(f"Image loaded: {self.image_path}\n")
        return True

    def _create_image_window(self):
        """Create window to display seismic image"""
        image_window = QDialog(self.parent)
        image_window.setWindowTitle('Seismic Section Image')          
        image_window.setGeometry(510, 100, 600, 400)

        layout = QVBoxLayout(image_window)

        self.image_canvas = FigureCanvas(plt.figure())
        self.image_canvas.setFocusPolicy(Qt.StrongFocus)
        self.image_canvas.figure.add_subplot(111).imshow(self.img_array, cmap='gray')     

        layout.addWidget(self.image_canvas)
        layout.addWidget(NavigationToolbar(self.image_canvas, image_window))
        
        image_window.show()
        self.image_canvas.draw()

        return image_window

    def _create_location_window(self):
        """Create window to display geometry plot"""
        window = QDialog(self.parent)
        window.setWindowTitle('Seismic Line Location')      
        window.setGeometry(1120, 100, 500, 400)

        layout = QVBoxLayout(window)

        fig = plt.figure()
        self.plot_location_canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.set_xlabel('UTM X')
        ax.set_ylabel('UTM Y')
        ax.grid(True)

        layout.addWidget(self.plot_location_canvas)
        layout.addWidget(NavigationToolbar(self.plot_location_canvas, window))

        window.show()
        return window

    def _load_geometry_data(self, base_name):
        """Load and display geometry data"""
        geometry_file = os.path.join(self.work_dir, 'GEOMETRY', f'{base_name}.geometry')

        if not os.path.exists(geometry_file):
            self.console.append("Geometry file not found.\n")
            return False

        try:
            cdp, x, y = [], [], []
            with open(geometry_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    cdp.append(parts[0])
                    x.append(float(parts[1]))
                    y.append(float(parts[2]))

            ax = self.plot_location_canvas.figure.get_axes()[0]        
            ax.plot(x, y, marker='o', markersize=2, color='red', linestyle='-')

            # Add labels with threshold to avoid overcrowding
            threshold = 1000
            annotated_positions = []
            for i, txt in enumerate(cdp):
                position = (x[i], y[i])
                if all(np.linalg.norm(np.array(position) - np.array(p)) > threshold 
                      for p in annotated_positions):
                    ax.annotate(txt, position)
                    annotated_positions.append(position)

            ax.set_title(f"COORDINATES \"{base_name}\"")
            ax.set_aspect('equal', adjustable='box')
            self.plot_location_canvas.draw()
            return True

        except Exception as e:
            self.console.append(f"Error loading geometry: {str(e)}\n")
            return False


class ROIManager:
    """Handles ROI selection and management"""
    def __init__(self, parent, console, image_canvas, work_dir,
                 trace_p1, trace_p2, trace_p3, 
                 twt_p1, twt_p2, twt_p3):
        self.parent = parent
        self.console = console
        self.image_canvas = image_canvas
        self.work_dir = work_dir
        self.points = []
        
        # Store trace and time parameters
        self.trace_values = [trace_p1, trace_p2, trace_p3, trace_p2]
        self.twt_values = [twt_p1, twt_p2, twt_p3, twt_p3]

    def select_roi(self, image_path, img_array):
        """Main ROI selection workflow"""
        # Get ROI file path
        roi_path = os.path.join(
            self.work_dir, 
            "ROI", 
            f"{os.path.splitext(os.path.basename(image_path))[0]}.roi"
        )
        
        if os.path.exists(roi_path):
            if self._prompt_use_existing_roi():
                self.points = self._load_roi_points(roi_path)
                self._draw_roi()
            else:
                if not self._get_new_roi(img_array):
                    return False
        else:
            if not self._get_new_roi(img_array):
                return False

        self._save_roi_points(roi_path)
        return self._confirm_roi()

    def _load_roi_points(self, roi_path):
        """Load ROI points from file"""
        with open(roi_path, "r") as f:
            return [tuple(map(float, line.split())) for line in f]

    def _save_roi_points(self, roi_path):
        """Save ROI points to file"""
        os.makedirs(os.path.dirname(roi_path), exist_ok=True)
        with open(roi_path, "w") as f:
            for point in self.points:
                f.write(f"{point[0]} {point[1]}\n")
        self.console.append(f"ROI points saved to: {roi_path}\n")

    def _get_new_roi(self, img_array):
        """Get new ROI through selection dialog"""
        dialog = ROISelectionDialog(img_array)
        if dialog.exec() == QDialog.Accepted:
            self.points = dialog.points
            self._draw_roi()
            return True
        return False

    def _draw_roi(self):
        """Draw ROI with labels"""
        if len(self.points) != 4:
            return

        ax = self.image_canvas.figure.axes[0]
        p1, p2, p3, p4 = self.points
        
        # Draw quadrilateral
        lines = [
            (p1, p2), (p2, p4), (p4, p3), (p3, p1)
        ]
        for start, end in lines:
            ax.plot([start[0], end[0]], [start[1], end[1]], 'b-')

        # Add labels
        for i, (p, cdp, twt) in enumerate(zip(
            self.points, self.trace_values, self.twt_values
        )):
            ax.text(p[0], p[1], 
                   f"CDP: {cdp}\nTWT: {twt}", 
                   color='red', 
                   fontsize=10, 
                   ha='right' if i % 2 == 0 else 'left')

        self.image_canvas.draw()

    def _prompt_use_existing_roi(self):
        """Ask user about using existing ROI"""
        return QMessageBox.question(
            self.parent,
            "Existing ROI",
            "Existing ROI found. Use it?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes

    def _confirm_roi(self):
        """Ask user to confirm ROI"""
        return QMessageBox.question(
            self.parent,
            "Confirm ROI",
            "Use this ROI?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes

    def get_points(self):
        """Return selected points"""
        return self.points
