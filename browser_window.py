from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon, QCursor
from tab_widget import TabWidget
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs = TabWidget(self)
        self.tabs.newTabRequested.connect(self.add_new_tab)
        self.setCentralWidget(self.tabs)
        
        # Set window size and position
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.showMaximized()

        # Set window title and icon
        self.setWindowTitle('ZenSurf')
        # Set the window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browser_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("Warning: Browser icon not found at", icon_path)

        # Create and style the navbar
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setIconSize(QSize(24, 24))
        navbar.setStyleSheet("""
            QToolBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #e9ecef;
            }
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
                background: white;
                selection-background-color: #007bff;
                min-width: 300px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: 0;
                box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
            }
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #e9ecef;
            }
        """)
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction(QIcon('back.png'), 'Back', self)
        back_btn.setStatusTip('Go back to previous page')
        back_btn.triggered.connect(self.navigate_back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction(QIcon('forward.png'), 'Forward', self)
        forward_btn.setStatusTip('Go forward to next page')
        forward_btn.triggered.connect(self.navigate_forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction(QIcon('reload.png'), 'Reload', self)
        reload_btn.setStatusTip('Reload current page')
        reload_btn.triggered.connect(self.reload_page)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(QIcon('home.png'), 'Home', self)
        home_btn.setStatusTip('Go to home page')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Adding a separator
        navbar.addSeparator()

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL or search term...')
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Search button
        search_btn = QAction(QIcon('search.png'), 'Search', self)
        search_btn.setStatusTip('Search the web')
        search_btn.triggered.connect(self.navigate_to_url)
        navbar.addAction(search_btn)

        # New tab button in navbar
        new_tab_btn = QAction(QIcon('new_tab.png'), 'New Tab', self)
        new_tab_btn.setStatusTip('Open a new tab')
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)

        # Hamburger menu
        self.menu_btn = QAction(QIcon('menu.png'), 'Menu', self)
        self.menu_btn.setStatusTip('Open menu')
        self.menu_btn.triggered.connect(self.show_menu)
        navbar.addAction(self.menu_btn)

        # Enable status bar
        self.setStatusBar(QStatusBar(self))

        # Add first tab
        self.add_new_tab(QUrl('http://google.com'), 'Homepage')

        # Connect signals
        self.tabs.currentChanged.connect(self.tab_changed)

    def add_new_tab(self, qurl=None, label="New Tab"):
        try:
            if qurl is None:
                qurl = QUrl('http://google.com')
            elif isinstance(qurl, str):
                qurl = QUrl(qurl)
            elif not isinstance(qurl, QUrl):
                qurl = QUrl('http://google.com')
            
            browser = QWebEngineView()
            browser.setUrl(qurl)
            # Set default zoom to 120%
            browser.setZoomFactor(1.2)
            
            i = self.tabs.addTab(browser, label)
            self.tabs.setCurrentIndex(i)
            
            # Connect signals for favicon and title updates
            browser.iconChanged.connect(lambda icon, i=i: self.update_tab_icon(icon, i))
            browser.titleChanged.connect(lambda title, i=i: self.update_tab_title(title, i))
            browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        except Exception as e:
            print(f"Error creating new tab: {e}")
            # If there's an error, try to create a tab with the default URL
            try:
                browser = QWebEngineView()
                browser.setUrl(QUrl('http://google.com'))
                browser.setZoomFactor(1.2)
                i = self.tabs.addTab(browser, label)
                self.tabs.setCurrentIndex(i)
                browser.iconChanged.connect(lambda icon, i=i: self.update_tab_icon(icon, i))
                browser.titleChanged.connect(lambda title, i=i: self.update_tab_title(title, i))
            except:
                pass

    def update_tab_icon(self, icon, index):
        try:
            if icon and not icon.isNull():
                self.tabs.setTabIcon(index, icon)
        except Exception as e:
            print(f"Error updating tab icon: {e}")

    def update_tab_title(self, title, index):
        try:
            if title:
                # Limit title to 15 characters and add ellipsis
                short_title = title[:15] + '...' if len(title) > 15 else title
                self.tabs.setTabText(index, short_title)
        except Exception as e:
            print(f"Error updating tab title: {e}")

    def tab_changed(self, i):
        try:
            if i >= 0 and self.tabs.currentWidget():
                qurl = self.tabs.currentWidget().url()
                self.update_url(qurl, self.tabs.currentWidget())
        except Exception as e:
            print(f"Error changing tab: {e}")

    def navigate_back(self):
        try:
            if self.tabs.currentWidget():
                self.tabs.currentWidget().back()
        except Exception as e:
            print(f"Error navigating back: {e}")

    def navigate_forward(self):
        try:
            if self.tabs.currentWidget():
                self.tabs.currentWidget().forward()
        except Exception as e:
            print(f"Error navigating forward: {e}")

    def reload_page(self):
        try:
            if self.tabs.currentWidget():
                self.tabs.currentWidget().reload()
        except Exception as e:
            print(f"Error reloading page: {e}")

    def navigate_home(self):
        try:
            if self.tabs.currentWidget():
                self.tabs.currentWidget().setUrl(QUrl('http://google.com'))
        except Exception as e:
            print(f"Error navigating home: {e}")

    def navigate_to_url(self):
        try:
            if not self.tabs.currentWidget():
                return
                
            url = self.url_bar.text()
            if '.' not in url and ' ' not in url:
                url = 'https://www.google.com/search?q=' + url
            elif ' ' in url:
                url = 'https://www.google.com/search?q=' + url.replace(' ', '+')
            elif not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self.tabs.currentWidget().setUrl(QUrl(url))
        except Exception as e:
            print(f"Error navigating to URL: {e}")
    
    def update_url(self, q, browser=None):
        try:
            if browser != self.tabs.currentWidget():
                return
            self.url_bar.setText(q.toString())
        except Exception as e:
            print(f"Error updating URL: {e}")

    def show_menu(self):
        try:
            menu = QMenu(self)
            
            # Zoom controls
            zoom_menu = menu.addMenu("Zoom")
            zoom_in_action = zoom_menu.addAction("Zoom In")
            zoom_out_action = zoom_menu.addAction("Zoom Out")
            reset_zoom_action = zoom_menu.addAction("Reset Zoom")
            
            zoom_in_action.triggered.connect(self.zoom_in)
            zoom_out_action.triggered.connect(self.zoom_out)
            reset_zoom_action.triggered.connect(self.reset_zoom)
            
            menu.addSeparator()
            
            # History
            history_action = menu.addAction("History")
            history_action.triggered.connect(self.show_history)
            
            # Bookmarks
            bookmarks_action = menu.addAction("Bookmarks")
            bookmarks_action.triggered.connect(self.show_bookmarks)
            
            # Downloads
            downloads_action = menu.addAction("Downloads")
            downloads_action.triggered.connect(self.show_downloads)
            
            menu.addSeparator()
            
            # Private Browsing
            private_action = menu.addAction("New Private Window")
            private_action.triggered.connect(self.open_private_window)
            
            menu.addSeparator()
            
            # Settings
            settings_action = menu.addAction("Settings")
            settings_action.triggered.connect(self.show_settings)
            
            # About
            about_action = menu.addAction("About")
            about_action.triggered.connect(self.show_about)
            
            # Get the toolbar and find the menu button's position
            toolbar = self.findChild(QToolBar)
            if toolbar:
                # Find the menu button widget
                for action in toolbar.actions():
                    if action == self.menu_btn:
                        # Get the widget associated with the action
                        widget = toolbar.widgetForAction(action)
                        if widget:
                            # Show menu at the widget's position
                            menu.exec_(widget.mapToGlobal(QPoint(0, widget.height())))
                            return
                
            # Fallback: show menu at cursor position
            menu.exec_(QCursor.pos())
        except Exception as e:
            print(f"Error showing menu: {e}")

    def zoom_in(self):
        try:
            if self.tabs.currentWidget():
                current_zoom = self.tabs.currentWidget().zoomFactor()
                self.tabs.currentWidget().setZoomFactor(current_zoom + 0.1)
        except Exception as e:
            print(f"Error zooming in: {e}")

    def zoom_out(self):
        try:
            if self.tabs.currentWidget():
                current_zoom = self.tabs.currentWidget().zoomFactor()
                self.tabs.currentWidget().setZoomFactor(max(0.25, current_zoom - 0.1))
        except Exception as e:
            print(f"Error zooming out: {e}")

    def reset_zoom(self):
        try:
            if self.tabs.currentWidget():
                self.tabs.currentWidget().setZoomFactor(1.2)  # Reset to 120% zoom
        except Exception as e:
            print(f"Error resetting zoom: {e}")

    def show_history(self):
        QMessageBox.information(self, "History", "History feature will be implemented soon!")

    def show_bookmarks(self):
        QMessageBox.information(self, "Bookmarks", "Bookmarks feature will be implemented soon!")

    def show_downloads(self):
        QMessageBox.information(self, "Downloads", "Downloads feature will be implemented soon!")

    def open_private_window(self):
        QMessageBox.information(self, "Private Browsing", "Private browsing will be implemented soon!")

    def show_settings(self):
        QMessageBox.information(self, "Settings", "Settings will be implemented soon!")

    def show_about(self):
        QMessageBox.about(self, "About My Browser", 
            "My Browser v1.0\n\n"
            "A simple web browser built with PyQt5\n"
            "© 2024") 