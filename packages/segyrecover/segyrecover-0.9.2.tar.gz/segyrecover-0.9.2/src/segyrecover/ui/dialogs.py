"""Dialog windows for SEGYRecover."""
import os
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor, QPolygonF, QIntValidator
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import (QRadioButton, QButtonGroup, QFileDialog,
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QMessageBox, QScrollArea, QWidget, QDialog, QDialogButtonBox
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ParameterDialog(QDialog):
    """Dialog for inputting SEGY processing parameters."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Parameters")
        self.setGeometry(150, 120, 400, 600)
        self.layout = QVBoxLayout(self)

        # Define constants 
        self.POINT_CONFIGS = [
            ("P1", "Top Left", (7.5, 7.5), "Top left corner coordinates"),
            ("P2", "Top Right", (57.5, 7.5), "Top right corner coordinates"), 
            ("P3", "Bottom Left", (7.5, 37.5), "Bottom left corner coordinates")
        ]
        
        self.FREQUENCY_PARAMS = [
            ("F1", "Low cut-off"), ("F2", "Low pass"),
            ("F3", "High pass"), ("F4", "High cut-off")
        ]

        self.DETECTION_PARAMS = [
            ("TLT", "Traceline Thickness", "Thickness of vertical trace lines"),
            ("HLT", "Timeline Thickness", "Thickness of horizontal time lines"),
            ("HE", "Horizontal Erode", "Erosion size for horizontal features"),
            ("BDB", "Baseline Detection Begining", "Baseline Detection Begining"),
            ("BDE", "Baseline Detection End", "Baseline Detection End"),
            ("BFT", "Baseline Filter Threshold", "Baseline Filter Threshold")
        ]

        # Create and populate the dialog sections
        self._create_point_inputs()
        self._create_acquisition_params()
        self._create_detection_params()
        
        # Add accept button
        self.accept_button = QPushButton("Accept", self)
        self.accept_button.clicked.connect(self.accept)
        self.layout.addWidget(self.accept_button)

    def _create_point_inputs(self):
        """Create input fields for ROI point coordinates."""
        for point_id, label, dot_pos, tooltip in self.POINT_CONFIGS:
            # Create group box with tooltips
            group = QGroupBox(f"{point_id} - {label}", self)
            group.setFont(QFont("", -1, QFont.Bold))
            group.setToolTip(tooltip)
            layout = QFormLayout()
            
            # Create Trace and TWT inputs
            for param in ["Trace", "TWT"]:
                input_field = QLineEdit(self)
                input_field.setFixedWidth(50)
                input_field.setValidator(QIntValidator())
                layout.addRow(f"{param}_{point_id}:", input_field)
                setattr(self, f"{param}_{point_id}", input_field)
            
            group.setLayout(layout)
            
            # Create horizontal layout with icon
            h_layout = QHBoxLayout()
            h_layout.addWidget(group)
            
            # Create and add icon
            icon = QLabel(self)
            pixmap = QPixmap(70, 50)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setPen(Qt.red)
            painter.drawRect(10, 10, 50, 30)
            painter.drawEllipse(dot_pos[0], dot_pos[1], 5, 5)
            painter.end()
            icon.setPixmap(pixmap)
            h_layout.addWidget(icon)
            
            self.layout.addLayout(h_layout)

    def _create_acquisition_params(self):
        """Create acquisition parameter inputs."""
        group = QGroupBox("Acquisition Parameters", self)
        group.setFont(QFont("", -1, QFont.Bold))
        layout = QFormLayout()
        
        # Sample rate input
        self.DT = QLineEdit(self)
        self.DT.setFixedWidth(50)
        self.DT.setValidator(QIntValidator())
        self.DT.setToolTip("Sample rate in milliseconds")
        layout.addRow("Sample Rate (ms):", self.DT)
        
        # Frequency band inputs
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency band (Hz):"))
        
        for param_id, tooltip in self.FREQUENCY_PARAMS:
            input_field = QLineEdit(self)
            input_field.setFixedWidth(30)
            input_field.setValidator(QIntValidator())
            input_field.setToolTip(tooltip)
            freq_layout.addWidget(input_field)
            setattr(self, param_id, input_field)
        
        # Add frequency band diagram
        icon = self._create_freq_band_icon()
        freq_layout.addWidget(icon)
        layout.addRow(freq_layout)
        
        group.setLayout(layout)
        self.layout.addWidget(group)
    
    def _create_detection_params(self):
        """Create timeline/baseline detection parameter inputs."""
        group = QGroupBox("Timeline and Baseline Detection Parameters", self)
        group.setFont(QFont("", -1, QFont.Bold))
        layout = QFormLayout()
        
        # Basic parameters - first two parameters (TLT, HLT)
        basic_params = self.DETECTION_PARAMS[:2]
        for param_id, label, tooltip in basic_params:
            input_field = QLineEdit(self)
            input_field.setFixedWidth(50)
            input_field.setValidator(QIntValidator())
            input_field.setToolTip(tooltip)
            layout.addRow(f"{label}:", input_field)
            setattr(self, param_id, input_field)
        
        # Add Advanced Parameters label
        advanced_label = QLabel("Advanced Parameters")
        advanced_label.setFont(QFont("", -1, QFont.Bold))
        advanced_label.setStyleSheet("color: #444; margin-top: 10px;")
        layout.addRow(advanced_label, QLabel(""))
        
        # Advanced parameters - remaining parameters (HE, BDB, BDE, BFT)
        advanced_params = self.DETECTION_PARAMS[2:]
        for param_id, label, tooltip in advanced_params:
            input_field = QLineEdit(self)
            input_field.setFixedWidth(50)
            input_field.setValidator(QIntValidator())
            input_field.setToolTip(tooltip)
            layout.addRow(f"{label}:", input_field)
            setattr(self, param_id, input_field)
        
        group.setLayout(layout)
        self.layout.addWidget(group)

    def _create_freq_band_icon(self):
        """Create frequency band diagram icon."""
        icon = QLabel(self)
        pixmap = QPixmap(70, 50)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(Qt.red)
        
        # Draw trapezoid
        points = [
            QPointF(20, 10), QPointF(10, 40),
            QPointF(60, 40), QPointF(50, 10)
        ]
        painter.drawPolygon(QPolygonF(points))
        
        # Add frequency labels
        painter.setPen(QColor(0, 0, 0))
        labels = [("F2", 10, 10), ("F1", 5, 40),
                 ("F4", 55, 40), ("F3", 50, 10)]
        for text, x, y in labels:
            painter.drawText(x, y, text)
        
        painter.end()
        icon.setPixmap(pixmap)
        return icon

    def get_parameters(self):
        """Return all parameters as a dictionary."""
        params = {}
        
        # Get point parameters
        for point in ["P1", "P2", "P3"]:
            for param in ["Trace", "TWT"]:
                key = f"{param}_{point}"
                params[key] = int(getattr(self, key).text())
        
        # Get acquisition parameters
        params["DT"] = int(self.DT.text())
        for param_id, _ in self.FREQUENCY_PARAMS:
            params[param_id] = int(getattr(self, param_id).text())
            
        # Get detection parameters
        for param_id, _, _ in self.DETECTION_PARAMS:
            params[param_id] = int(getattr(self, param_id).text())
            
        return params


class TimelineBaselineWindow(QDialog):
    """Dialog for displaying and verifying timeline/baseline detection results."""
    
    def __init__(self, image_a, image_f, image_g, image_m, 
                 raw_baselines, clean_baselines, final_baselines, BDB, BDE):
        super().__init__()  
        self.setWindowTitle("Timeline and Baseline Detection")
        self.setGeometry(200, 150, 1100, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        fig, ((ax1, ax4), (ax2, ax3)) = plt.subplots(2, 2)
        self.canvas = FigureCanvas(fig)
        self.canvas.setFocusPolicy(Qt.StrongFocus) 
        
        layout.addWidget(self.canvas)
        
        toolbar_segyrec = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar_segyrec)

        # Plot the images and lines
        ax1.imshow(image_g, cmap='gray')        
        ax1.set_title('Image with Timelines Removed')

        ax2.imshow(image_a, cmap='gray')
        ax2.axhline(y=BDB, color='blue', linewidth=2, linestyle='--')
        ax2.axhline(y=BDE, color='blue', linewidth=2, linestyle='--')
        ax2.set_title('Image with Baselines')

        ax3.imshow(image_m, cmap='gray')
        ax3.set_title('Debug Baseline Detection')
        ax3.axhline(y=BDB, color='blue', linewidth=2, linestyle='--')
        ax3.axhline(y=BDE, color='blue', linewidth=2, linestyle='--')

        ax4.imshow(image_f, cmap='gray')
        ax4.set_title('Timelines')

        # Draw baselines
        for baseline in final_baselines:
            ax2.axvline(x=baseline, color='lime', linewidth=1)
        
        for baseline in raw_baselines:
            ax3.axvline(x=baseline, color='red', linewidth=1)

        for baseline in final_baselines:
            if baseline not in raw_baselines:
                ax3.axvline(x=baseline, color='cyan', linewidth=1, linestyle='--')

        # Add buttons at the bottom
        button_layout = QHBoxLayout()
        
        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.accept)
        button_layout.addWidget(continue_button)
        
        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(self.reject)
        button_layout.addWidget(restart_button)
        
        layout.addLayout(button_layout)


class ROISelectionDialog(QDialog):
    """Dialog for selecting region of interest on an image."""
    
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Select Region of Interest")
        self.setGeometry(100, 100, 800, 600)
        
        # Store points and create layout
        self.points = []
        layout = QVBoxLayout()
        
        # Create canvas for image display
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFocusPolicy(Qt.StrongFocus) 
        self.ax = self.figure.add_subplot(111)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar)
        
        # Display image and connect mouse event
        self.ax.imshow(image, cmap='gray')
        self.canvas.mpl_connect('button_press_event', self.on_click)
        layout.addWidget(self.canvas)
        
        # Instructions label
        self.instruction_label = QLabel(
        "Right-click to select points in this order:\n"
        "1. Top-left corner\n"
        "2. Top-right corner\n"
        "3. Bottom-left corner\n"
        "The fourth corner will be calculated automatically."
        )
        layout.addWidget(self.instruction_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Accept button (initially disabled)
        self.accept_button = QPushButton("Accept")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.accept)
        
        # Retry button
        self.retry_button = QPushButton("Retry")
        self.retry_button.clicked.connect(self.retry)
        
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.retry_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.binary_rectified_image = image  # Store for retry

    def on_click(self, event):
        """Handle mouse clicks for point selection."""
        if event.button == 3 and len(self.points) < 3:  # Right click
            # Create confirmation dialog
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Confirm Point")
            msg_box.setText(f"Confirm point {len(self.points) + 1} at coordinates:\nX: {event.xdata:.2f}\nY: {event.ydata:.2f}")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            
            if msg_box.exec() == QMessageBox.Yes:
                self.points.append((event.xdata, event.ydata))
            
                # Draw point
                self.ax.plot(event.xdata, event.ydata, 'ro')
                
                # Draw number next to point
                self.ax.annotate(str(len(self.points)), 
                        (event.xdata, event.ydata),
                        xytext=(10, 10),
                        textcoords='offset points')
                
                if len(self.points) == 3:
                    # Calculate fourth point
                    p1, p2, p3 = self.points
                    p4 = (p2[0] + (p3[0] - p1[0]), p3[1] + (p2[1] - p1[1]))
                    self.points.append(p4)
                    
                    # Draw fourth point
                    self.ax.plot(p4[0], p4[1], 'ro')
                    self.ax.annotate('4', (p4[0], p4[1]), 
                       xytext=(10, 10),
                       textcoords='offset points')
                    
                    # Draw lines connecting points to form quadrilateral
                    self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')  # Line 1-2
                    self.ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-')  # Line 1-3
                    self.ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-')  # Line 2-4
                    self.ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-')  # Line 3-4
                    
                    # Enable accept button
                    self.accept_button.setEnabled(True)
        
            self.canvas.draw()

    def retry(self):
        """Clear all points and restart selection."""
        self.points = []
        self.ax.clear()
        self.ax.imshow(self.binary_rectified_image, cmap='gray')
        self.accept_button.setEnabled(False)
        self.canvas.draw()


class HelpDialog(QDialog):
    """Help dialog with information about the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("How to Use SEGYRECOVER")    
        self.setGeometry(510, 100, 500, 820)
        
        # Create scroll area
        scroll = QWidget()
        scroll_layout = QVBoxLayout(scroll)
        
        # Add content
        msg = """
        <h2>SEGYRECOVER Tutorial</h2>
        
        <p><b>SEGYRECOVER</b> is a comprehensive tool designed to digitize seismic images into SEGY format.</p>

        <h2> Visualization controls </h2>
        <p> The application provides a set of tools to navigate and interact with the seismic image:</p>
        <h3>Navigation Toolbar</h3>
        <ul>
            <li>🏠 <b>Home:</b> Reset view to original display</li>
            <li>⬅️ <b>Back:</b> Previous view</li>
            <li>➡️ <b>Forward:</b> Next view</li>
            <li>✋ <b>Pan:</b> Left click and drag to move around</li>
            <li>🔍 <b>Zoom:</b> Left click and drag to zoom into a rectangular region</li>
            <li>⚙️ <b>Configure:</b> Configure plot settings</li>
            <li>💾 <b>Save:</b> Save the figure</li>
        </ul>
        
        <h2>SEGYRECOVER Workflow</h2>
        <p>The application follows a step-by-step process to digitize and rectify seismic images:</p>

        <h3>Step 1: Load Image</h3>
        <ul>
            <li>Click "Load Image" to select an image (TIF, JPEG, PNG)</li>
            <li>Images should be in binary format (black and white pixels only)</li>
            <li>The corresponding geometry file  in the GEOMETRY folder will be automatically loaded and displayed</li>
        </ul>

        <h3>Step 2: Set Parameters</h3>
        <ul>
            <li><b>ROI Points</b>: Set trace number and TWT values for the 3 corner points</li>
            <li><b>Acquisition Parameters</b>:
            <ul>
                <li>Sample Rate (DT): Time interval in milliseconds</li> 
                <li>Frequency Band (F1-F4): Filter corners in Hz</li>
            </ul>
            </li>
            <li><b>Detection Parameters</b>:
            <ul>
                <li>TLT: Thickness in pixels of vertical trace lines</li>
                <li>HLT: Thickness in pixels of horizontal time lines</li>
                <li>HE: Erosion size for horizontal features</li>
                <li><b>Advanced parameters:</b></li>
                <li>BDB: Begining of baseline detection range in pixels from the top</li>
                <li>BDE: End of bÝaseline detection range in pixels from the top</li>
                <li>BFT: Baseline filter threshold</li>
            </ul>
            </li>
        </ul>

        <h3>Step 3: Region Selection</h3>
        <ul>
            <li>Click "Begin Digitization" and select 3 points on the image using <b>right-click</b>:</li>
            <ol>
                <li>Top-left corner (P1)</li>
                <li>Top-right corner (P2)</li>
                <li>Bottom-left corner (P3)</li>
            </ol>
            </li>
            <li>Zoom using the navigation toolbar to select points accurately</li>
            <li>The fourth corner will be calculated automatically</li>
            <li>The selected region will be rectified and displayed</li>
        </ul>

        <h3>Step 4: Processing</h3>
        <ul>
            <li>Process will continue with the following steps:</li>
            <li>Timeline detection and removal</li>
            <li>Baseline detection: a window will appear for quality control</li>
            <li>Amplitude extraction</li>
            <li>Data resampling and filtering</li>
            <li>Coordinate assignment</li>
            <li>SEGY file creation</li>
        </ul>

        <h3>Step 5: Results</h3>
        <ul>
            <li>Displays the digitized SEGY section</li>
            <li>Shows the average amplitude spectrum</li>
            <li>Creates SEGY file in the SEGY folder</li>
        </ul>

        <h3>File Structure</h3>
        <ul>
            <li><b>IMAGES/</b>: Store input seismic images</li>
            <li><b>GEOMETRY/</b>: Store .geometry files with trace coordinates</li>
            <li><b>ROI/</b>: Store region of interest points</li>
            <li><b>PARAMETERS/</b>: Store processing parameters</li>
            <li><b>SEGY/</b>: Store output SEGY files</li>
        </ul>
        """
        
        # Create text label with HTML content
        text = QLabel(msg)
        text.setWordWrap(True)
        text.setTextFormat(Qt.RichText)
        scroll_layout.addWidget(text)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll)
        scroll_area.setWidgetResizable(True)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

# Add this class to your existing dialogs.py file

class AboutDialog(QDialog):
    """Dialog displaying information about the application."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SEGYRecover")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # App icon or logo would go here if available
        title = QLabel("SEGYRecover")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Version and copyright info
        version = QLabel("Version 0.9.2")
        version.setAlignment(Qt.AlignCenter)
        
        copyright = QLabel("© 2025 Alejandro Pertuz")
        copyright.setAlignment(Qt.AlignCenter)
        
        # Description text
        description = QLabel(
            "A Python tool for digitizing scanned seismic sections\n"
            "and converting them to standard SEGY format."
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        
        # License info
        license_info = QLabel("Released under the GPL-3.0 License")
        license_info.setAlignment(Qt.AlignCenter)
        
        # Add all widgets to layout
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(copyright)
        layout.addSpacing(10)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(license_info)
        
        # Add OK button at bottom
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

class FirstRunDialog(QDialog):
    """Dialog shown on first run to configure application settings."""
    
    def __init__(self, parent=None, default_location=None):
        super().__init__(parent)
        self.selected_location = default_location
        self.custom_location = None
        
        self.setWindowTitle("Welcome to SEGYRecover")
        self.resize(600, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Welcome heading
        welcome_label = QLabel("Welcome to SEGYRecover!", self)
        welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Description
        description = QLabel(
            "Choose where you'd like to store your data files.\n"
            "You can change this later in the application settings.\n", 
            self
        )
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        layout.addSpacing(20)
        
        # Location options group
        location_group = QGroupBox("Data Storage Location", self)
        location_layout = QVBoxLayout()
        
        # Radio button group
        self.location_btn_group = QButtonGroup(self)
        
        # Default location option (from appdirs)
        self.default_radio = QRadioButton("Default location (system-managed)", self)
        self.default_radio.setToolTip(f"Store in: {self.selected_location}")
        self.location_btn_group.addButton(self.default_radio, 1)
        location_layout.addWidget(self.default_radio)
        
        # Documents folder option
        documents_path = os.path.join(os.path.expanduser("~"), "Documents", "SEGYRecover")
        self.documents_radio = QRadioButton(f"Documents folder: {documents_path}", self)
        self.location_btn_group.addButton(self.documents_radio, 2)
        location_layout.addWidget(self.documents_radio)
        
        # Custom location option
        custom_layout = QHBoxLayout()
        self.custom_radio = QRadioButton("Custom location:" , self)
        self.location_btn_group.addButton(self.custom_radio, 3)
        custom_layout.addWidget(self.custom_radio)
        
        self.browse_btn = QPushButton("Browse...", self)
        self.browse_btn.clicked.connect(self.browse_location)
        custom_layout.addWidget(self.browse_btn)
        
        location_layout.addLayout(custom_layout)
        
        # Selected path display
        self.path_label = QLabel("", self)
        location_layout.addWidget(self.path_label)
        
        location_group.setLayout(location_layout)
        layout.addWidget(location_group)
        
        layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.continue_btn = QPushButton("Continue", self)
        self.continue_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.continue_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set default selection
        self.default_radio.setChecked(True)
        self.location_btn_group.buttonClicked.connect(self.update_selection)
    
    def browse_location(self):
        """Open file dialog to select custom location."""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory for SEGYRecover Data",
            os.path.expanduser("~")
        )
        
        if directory:
            self.custom_location = os.path.join(directory, "SEGYRecover")
            self.path_label.setText(f"Selected: {self.custom_location}")
            self.custom_radio.setChecked(True)
            self.update_selection(self.custom_radio)
    
    def update_selection(self, button):
        """Update the selected location based on radio button choice."""
        if button == self.default_radio:
            self.selected_location = self.selected_location
        elif button == self.documents_radio:
            self.selected_location = os.path.join(os.path.expanduser("~"), "Documents", "SEGYRecover")
        elif button == self.custom_radio and self.custom_location:
            self.selected_location = self.custom_location
    
    def get_selected_location(self):
        """Return the user's selected location."""
        return self.selected_location
