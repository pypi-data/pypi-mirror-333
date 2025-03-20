"""Entry point for the SEGYRecover application."""

import sys
import os
from PySide6.QtWidgets import QApplication

# Use relative imports when running as an installed package
from .ui.main_window import SegyRecover

def main():
    """Run the SEGYRecover application."""
    app = QApplication(sys.argv)
    
    # Get the path to the QSS file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "ui", "theme.qss")
    
    # Load and apply the stylesheet from file
    try:
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error loading stylesheet: {str(e)}")

    # Create and show main window directly using SegyRecover
    window = SegyRecover()
    window.setWindowTitle('SEGYRecover')
    window.setGeometry(100, 100, 400, 870)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    # When run directly as a script, we need to adjust imports
    try:
        # Try to run using the installed package context
        from segyrecover.ui.main_window import SegyRecover
    except ImportError:
        # Fallback to direct imports when running from source
        try:
            from src.segyrecover.ui.main_window import SegyRecover
        except ImportError:
            # Last resort when running from the current directory
            from ui.main_window import SegyRecover
            
    # For direct execution, locate the QSS file relative to this script
    main()
