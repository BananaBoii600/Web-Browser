#packages
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


#Creating the main browser class
class WebBrowser(QMainWindow):

    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Web Browser")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        #Creating the buttons
        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)

        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)

        #Adding the Buttons to the canvas
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)

        self.browser = QWebEngineView()

        #Creating Functions for the buttons
        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.toPlainText()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
                
        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        #Setting the browser's default url when opened to google.com
        self.browser.setUrl(QUrl("https://google.com"))

        self.window.setLayout(self.layout)
        self.window.show()

    #Function to add "http:// to the url if it is not typed already"
    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def home(self):
        self.url_bar.setText("google.com")
        self.navigate()

app = QApplication([])
window = WebBrowser()
app.exec_()
