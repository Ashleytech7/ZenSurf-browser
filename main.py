import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import os
from browser_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('ZenSurf')
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browser_icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print("Warning: Browser icon not found at", icon_path)
        
    window = MainWindow()
    app.exec_()