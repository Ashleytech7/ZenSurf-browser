import json
import os
import sys
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str)  # current_version, latest_version
    
    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version
        self.update_url = "https://raw.githubusercontent.com/yourusername/zensurf/main/version.json"
        
    def run(self):
        try:
            response = requests.get(self.update_url)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('version')
                if self._compare_versions(latest_version, self.current_version) > 0:
                    self.update_available.emit(self.current_version, latest_version)
        except Exception as e:
            print(f"Error checking for updates: {e}")
    
    def _compare_versions(self, v1, v2):
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))
        return (v1_parts > v2_parts) - (v1_parts < v2_parts)

def check_for_updates(parent, current_version):
    checker = UpdateChecker(current_version)
    
    def show_update_dialog(current, latest):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Update Available")
        msg.setText(f"A new version of ZenSurf is available!\n\n"
                   f"Current version: {current}\n"
                   f"Latest version: {latest}\n\n"
                   f"Would you like to download the update?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == QMessageBox.Yes:
            # Here you would implement the download and update process
            QMessageBox.information(parent, "Update", 
                                  "Please visit our website to download the latest version.")
    
    checker.update_available.connect(show_update_dialog)
    checker.start() 