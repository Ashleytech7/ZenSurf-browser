from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class TabWidget(QTabWidget):
    newTabRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        
        # Set fixed tab width and styling
        self.setStyleSheet("""
            QTabBar::tab {
                min-width: 150px;
                max-width: 150px;
                padding: 8px;
                text-overflow: ellipsis;
                overflow: hidden;
            }
            QTabBar::tab:selected {
                background-color: #f8f9fa;
                border-bottom: 2px solid #007bff;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Create a container widget for the tab bar
        self.tab_bar = self.tabBar()
        
        # Add new tab button
        self.new_tab_button = QToolButton(self.tab_bar)
        self.new_tab_button.setText('+')
        self.new_tab_button.setStyleSheet("""
            QToolButton {
                border: none;
                padding: 5px;
                background-color: transparent;
                font-size: 16px;
                min-width: 30px;
                min-height: 30px;
                margin-right: 5px;
            }
            QToolButton:hover {
                background-color: #e9ecef;
                border-radius: 4px;
            }
        """)
        self.new_tab_button.clicked.connect(self.newTabRequested.emit)
        self.new_tab_button.show()
        
        # Connect signals to update button position
        self.currentChanged.connect(self.update_new_tab_button_position)
        self.tabCloseRequested.connect(self.update_new_tab_button_position)
        
        # Initial button position update
        self.update_new_tab_button_position()
        
    def update_new_tab_button_position(self):
        # Get the last tab's rectangle
        last_tab_index = self.tab_bar.count() - 1
        if last_tab_index >= 0:
            tab_rect = self.tab_bar.tabRect(last_tab_index)
            # Position the button with more space from the tab's right edge
            self.new_tab_button.move(tab_rect.right() + 15, tab_rect.top() + (tab_rect.height() - 30) // 2)
            self.new_tab_button.show()
        
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        else:
            # Instead of closing the window, just reload the home page
            self.widget(0).setUrl(QUrl('http://google.com')) 