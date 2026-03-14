import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        view = QWebEngineView()
        view.setPage(page)
        view.show()
        return page

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setUrl(QUrl('https://google.com'))

        # disable right click menu
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.showFullScreen()

        # NAVBAR
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # CLIPBOARD WIPE TIMER (blocks paste)
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.clear_clipboard)
        self.clipboard_timer.start(100)

    def navigate_to_url(self):
        url = self.url_bar.text()

        if not url.startswith("http"):
            url = "https://" + url

        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    # clear clipboard repeatedly
    def clear_clipboard(self):
        QApplication.clipboard().clear()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.showFullScreen()

    
    def restore_fullscreen(self):
        self.showFullScreen()
        self.activateWindow()

    def keyPressEvent(self, event):

        # block paste
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            return

        # block Alt+Tab / Alt+F4 attempts
        if event.modifiers() == Qt.AltModifier:
            return

        super().keyPressEvent(event)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit Browser",
            "Are you sure you want to exit the contest browser?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )   

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
QApplication.setApplicationName('ACM BROWSER')

window = MainWindow()
app.exec()