"""Core workflow functions for SEGYRecover application."""

import os
import cv2
import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox


from .dialogs import ParameterDialog, TimelineBaselineWindow
from .image_viewer import display_segy_results, display_amplitude_spectrum, ROIManager
from ..core.image_processor import ImageProcessor
from ..core.amplitude_extractor import AmplitudeExtractor
from ..core.data_processor import DataProcessor
from ..core.segy_writer import SegyFileWriter

# Module-level variables to store processor instances
image_processor = None
amplitude_extractor = None
data_processor = None
segy_writer = None
roi_manager = None

def initialize(progress_bar, console, script_dir, image_canvas):
    """Initialize the workflow module with required components."""
    global image_processor, amplitude_extractor, data_processor, segy_writer, roi_manager
    
    # Initialize processors
    image_processor = ImageProcessor(progress_bar, console, script_dir)
    amplitude_extractor = AmplitudeExtractor(progress_bar, console, script_dir)
    data_processor = DataProcessor(progress_bar, console, script_dir)
    segy_writer = SegyFileWriter(progress_bar, console, script_dir)
    
    
    # Initialize ROI manager with default values
    roi_manager = ROIManager(
        parent=progress_bar.parent().parent(),
        console=console,
        image_canvas=image_canvas,
        script_dir=script_dir,
        trace_p1=0, trace_p2=0, trace_p3=0,
        twt_p1=0, twt_p2=0, twt_p3=0
    )
    
    return roi_manager

def load_image(main_window):
    """Handle image loading through ImageLoader."""
    if main_window.image_loader.load_image():
        main_window.image_path = main_window.image_loader.image_path
        main_window.img_array = main_window.image_loader.img_array
        main_window.image_canvas = main_window.image_loader.image_canvas
        
        # Update the ROI manager with the new canvas
        global roi_manager
        roi_manager.image_canvas = main_window.image_canvas
        
        main_window.plot_location_canvas = main_window.image_loader.plot_location_canvas
        main_window.param_button.setEnabled(True)


def input_parameters(main_window):
    """Open a dialog to input, validate and save processing parameters."""
    if not main_window.image_path:
        QMessageBox.warning(main_window, "Warning", "Please load an image first.")
        return

    # Setup paths
    base_name = os.path.splitext(os.path.basename(main_window.image_path))[0]
    parameters_dir = os.path.join(main_window.script_dir, "PARAMETERS")
    parameters_path = os.path.join(parameters_dir, f"{base_name}.par")

    # Create parameter dialog
    dialog = ParameterDialog(main_window)

    try:
        # Load existing parameters with defaults
        default_params = {
            "Trace_P1": "0", "TWT_P1": "0",
            "Trace_P2": "0", "TWT_P2": "0",
            "Trace_P3": "0", "TWT_P3": "0",
            "DT": "1", 
            "F1": "10", "F2": "12", "F3": "70", "F4": "80",
            "TLT": "1", "HLT": "1", "HE": "50", "BDB": "5", "BDE": "100", "BFT": "80"
        }

        params = default_params.copy()
        if os.path.exists(parameters_path):
            with open(parameters_path, "r") as f:
                file_params = dict(line.split('\t') for line in f if '\t' in line)
                params.update({k: v.strip() for k,v in file_params.items()})

        # Set dialog values
        for param, value in params.items():
            if hasattr(dialog, param):
                getattr(dialog, param).setText(value)

        if dialog.exec():
            # Validate parameters
            try:
                param_values = {
                    "Trace_P1": int(dialog.Trace_P1.text()),
                    "TWT_P1": int(dialog.TWT_P1.text()),
                    "Trace_P2": int(dialog.Trace_P2.text()), 
                    "TWT_P2": int(dialog.TWT_P2.text()),
                    "Trace_P3": int(dialog.Trace_P3.text()),
                    "TWT_P3": int(dialog.TWT_P3.text()),
                    "DT": int(dialog.DT.text()),
                    "F1": int(dialog.F1.text()),
                    "F2": int(dialog.F2.text()),
                    "F3": int(dialog.F3.text()),
                    "F4": int(dialog.F4.text()),
                    "TLT": int(dialog.TLT.text()),
                    "HLT": int(dialog.HLT.text()),
                    "HE": int(dialog.HE.text()),
                    "BDB": int(dialog.BDB.text()),
                    "BDE": int(dialog.BDE.text()),
                    "BFT": int(dialog.BFT.text())                
                }

                # Validate parameter relationships
                validations = [
                    (param_values["DT"] > 0, "Sample rate must be > 0"),
                    (param_values["F4"] > param_values["F3"], "F4 must be > F3"),
                    (param_values["F3"] > param_values["F2"], "F3 must be > F2"), 
                    (param_values["F2"] > param_values["F1"], "F2 must be > F1"),
                    (param_values["F1"] > 0, "F1 must be > 0"),
                    (param_values["TWT_P3"] > param_values["TWT_P1"], "TWT_P3 must be > TWT_P1"),
                    (param_values["BDB"] < param_values["BDE"], "BDB must be < BDE"),
                    (param_values["BDB"] >= 0, "BDB must be >= 0"),
                    (param_values["BFT"] >= 0 and param_values["BFT"] <= 100, "BFT must be between 0 and 100"),
                    (param_values["TLT"] > 0, "Timeline thickness must be > 0"),
                    (param_values["HLT"] > 0, "Horizontal line thickness must be > 0"),
                    (param_values["HE"] > 0, "Horizontal erosion must be > 0"),
                    (param_values["Trace_P1"] >= 0, "Trace_P1 must be >= 0"),
                    (param_values["Trace_P2"] >= 0, "Trace_P2 must be >= 0"),
                    (param_values["Trace_P3"] >= 0, "Trace_P3 must be >= 0")
                ]

                for condition, message in validations:
                    if not condition:
                        raise ValueError(message)

                # Save parameters
                os.makedirs(parameters_dir, exist_ok=True)
                with open(parameters_path, "w") as f:
                    for param, value in param_values.items():
                        f.write(f"{param}\t{value}\n")

                # Update main window attributes for reference
                for param, value in param_values.items():
                    setattr(main_window, param, value)

                main_window.console.append(f"\nPARAMETERS FOR {base_name}:")
                for param, value in param_values.items():
                    main_window.console.append(f"{param}: {value}")
                main_window.console.append(f"\nParameters saved: {parameters_path}\n")

                # Show next steps
                QMessageBox.information(main_window, "Parameters Set",
                    "<p><b>Parameters saved successfully.</b></p>")

                main_window.begin_digitization_button.setEnabled(True)
                
                # Update our module ROI manager with new parameters
                global roi_manager
                roi_manager = ROIManager(
                    main_window,
                    main_window.console, 
                    main_window.image_canvas,
                    main_window.script_dir,
                    param_values["Trace_P1"], param_values["Trace_P2"], param_values["Trace_P3"],
                    param_values["TWT_P1"], param_values["TWT_P2"], param_values["TWT_P3"]
                )

            except ValueError as e:
                QMessageBox.critical(main_window, "Invalid Parameters", str(e))
                return

    except Exception as e:
        main_window.console.append(f"Error processing parameters: {str(e)}\n")
        QMessageBox.critical(main_window, "Error", 
            f"Failed to process parameters: {str(e)}")


def select_area(main_window):
    """Handle ROI selection process."""
    if not main_window.image_path:
        QMessageBox.warning(main_window, "Warning", "Please load an image first.")
        return

    # Start ROI selection process using our module ROI manager
    global roi_manager
    selected = roi_manager.select_roi(main_window.image_path, main_window.img_array)
    if selected:
        main_window.points = roi_manager.get_points()
        crop_seismic_section(main_window)


def crop_seismic_section(main_window):
    """Crop the seismic section based on the selected points."""
    if len(main_window.points) == 4 and main_window.img_array is not None:
        pts1 = np.float32(main_window.points)
        width = int(np.linalg.norm(np.array(main_window.points[0]) - np.array(main_window.points[1])))
        height = int(np.linalg.norm(np.array(main_window.points[0]) - np.array(main_window.points[2])))
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        main_window.rectified_image = cv2.warpPerspective(main_window.img_array, matrix, (width, height))

        # Convert the rectified image to binary (0 or 255)
        _, main_window.binary_rectified_image = cv2.threshold(main_window.rectified_image, 128, 255, cv2.THRESH_BINARY)

        ax = main_window.image_canvas.figure.axes[0]
        ax.clear()
        ax.imshow(main_window.binary_rectified_image, cmap='gray')
        main_window.image_canvas.draw()

        main_window.console.append("Seismic section cropped and rectified\n")            

        main_window.load_button.setEnabled(False)
        main_window.param_button.setEnabled(False)

        digitize_segy(main_window)


def digitize_segy(main_window):
    """Process seismic data through all steps to create SEGY file."""
    try:
        # Use our module-level processors instead of main_window's ones
        global image_processor, amplitude_extractor, data_processor, segy_writer
        
        # 1. Remove timelines
        image_g, image_f = image_processor.remove_timelines(
            main_window.binary_rectified_image,
            main_window.HE,
            main_window.HLT
        )
        if image_g is None:
            return
        
        # 2. Detect baselines
        image_m, raw_baselines, clean_baselines, final_baselines = image_processor.detect_baselines(
            image_g,
            main_window.TLT,
            main_window.BDB,
            main_window.BDE,
            main_window.BFT
        )
        if image_m is None:
            return
        
        timeline_baseline_window = TimelineBaselineWindow(
            main_window.binary_rectified_image, 
            image_f, 
            image_g, 
            image_m, 
            raw_baselines, 
            clean_baselines,
            final_baselines,
            main_window.BDB, 
            main_window.BDE)
            
        result = timeline_baseline_window.exec()

        if result != QMessageBox.Accepted:
            main_window.restart_process()
            main_window.console.append("Process cancelled. Try setting new parameters.\n")            
            return

        # 3. Extract amplitudes
        raw_amplitude = amplitude_extractor.extract_amplitude(
            image_g, 
            final_baselines
        )
        if raw_amplitude is None:
            main_window.console.append("Failed to extract amplitude\n")
            return
        
        processed_amplitude = amplitude_extractor.process_amplitudes(
            raw_amplitude
        )
        if processed_amplitude is None:
            main_window.console.append("Failed to process amplitude\n")
            return
        
        # 4. Resample and filter
        old_times = np.linspace(main_window.TWT_P1, main_window.TWT_P3, processed_amplitude.shape[0])
        new_times = np.arange(main_window.TWT_P1, main_window.TWT_P3 + main_window.DT, main_window.DT)
        
        resampled = data_processor.resample_data(
            processed_amplitude,
            old_times,
            new_times
        )
        if resampled is None:
            main_window.console.append("Failed to resample data\n")
            return

        filtered = data_processor.filter_data(
            resampled,
            main_window.DT,
            main_window.F1,
            main_window.F2,
            main_window.F3,
            main_window.F4
        )
        if filtered is None:
            main_window.console.append("Failed to filter data\n")
            return
        
        # 5. Create SEGY
        base_name = os.path.splitext(os.path.basename(main_window.image_path))[0]
        segy_path = os.path.join(main_window.script_dir, "SEGY", f"{base_name}.segy")
        
        if not segy_writer.write_segy(
            filtered,
            final_baselines,
            main_window.image_path,
            main_window.DT,
            main_window.F1,
            main_window.F2,
            main_window.F3,
            main_window.F4
        ):
            main_window.console.append("Failed to create SEGY file\n")
            return

        # 6. Display results
        display_results(main_window, filtered, segy_path)
        
    except Exception as e:
        main_window.console.append(f"Digitization failed: {str(e)}\n")
        main_window.restart_process()


def display_results(main_window, filtered_data, segy_path):
    """Display SEGY section and amplitude spectrum."""
    try:
        # Display SEGY section
        seis_window = display_segy_results(segy_path, main_window)
        
        # Display amplitude spectrum
        spectrum_window = display_amplitude_spectrum(filtered_data, main_window.DT, main_window)
        
        if seis_window and spectrum_window:
            main_window.console.append("Results displayed successfully\n")
        else:
            main_window.console.append("Some results could not be displayed\n")
            
    except Exception as e:
        main_window.console.append(f"Error displaying results: {str(e)}\n")
