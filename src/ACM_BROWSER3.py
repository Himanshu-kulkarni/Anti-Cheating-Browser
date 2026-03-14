import sys
import os

# ---- SYSTEM COMPATIBILITY FIXES ----
# Prevent GPU crashes on some Windows laptops
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"

# Fix sandbox crashes on some systems
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from urllib.parse import urlparse


# Allowed domains
ALLOWED_DOMAINS = [
    "hackerrank.com",
    "hrcdn.net",
    "api.hackerrank.com",
    "cdn.hackerrank.com",
    "assets.hackerrank.com",
    "accounts.google.com",
    "google.com",
    "gstatic.com",
    "login.microsoftonline.com",
    "microsoft.com",
    "linkedin.com",
    "licdn.com"
]


class WebEnginePage(QWebEnginePage):

    

    def acceptNavigationRequest(self, url, _type, isMainFrame):

        hostname = urlparse(url.toString()).hostname

        if hostname:
            for domain in ALLOWED_DOMAINS:
                if hostname.endswith(domain):
                    return True

        if isMainFrame:
            self.view().setUrl(QUrl("https://www.hackerrank.com"))

        return False


    def createWindow(self, _type):

        # Handle popup windows (OAuth login etc.)
        view = QWebEngineView()
        page = WebEnginePage(view)

        view.setPage(page)
        view.resize(1000, 700)
        view.show()

        return page


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("ACM Contest Browser")

        # Correct window flags (fixed override issue)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )

        self.browser = QWebEngineView()

        page = WebEnginePage(self.browser)
        self.browser.setPage(page)

        self.browser.setUrl(QUrl("https://www.hackerrank.com"))

        # Disable right click
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)

        self.setCentralWidget(self.browser)

        self.showMaximized()
        self.showFullScreen()

        # ----- NAVBAR -----
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # ---- CLIPBOARD WIPE TIMER ----
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

        # Block paste
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            return

        # Block Alt shortcuts
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


# ---- APPLICATION START ----
from PyQt5.QtWebEngine import QtWebEngine
QtWebEngine.initialize()

app = QApplication(sys.argv)

QApplication.setApplicationName("ACM BROWSER")

window = MainWindow()

sys.exit(app.exec())