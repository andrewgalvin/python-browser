import sys
from datetime import datetime
from urllib.parse import urlparse
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEnginePage,
    QWebEngineProfile,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QAction,
    QMenu,
    QApplication,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class Browser(QWidget):
    def __init__(self, proxy, link_file):
        """
        This is the constructor for the main window of the application.
        It sets the geometry, style, title and icon of the main window,
        creates the tab widget, navigation layout, URL bar and layout
        for the main window, and sets the proxy and opens the links
        specified in the link_file.

        Parameters:
            - proxy (str): The proxy to be used for the application.
            - link_file (str): The file containing the links to be opened.
        """
        super().__init__()
        self.setGeometry(100, 100, 1600, 1200)
        self.setStyleSheet(
            "QWidget { background-color: #2a2a3b;}"
            "QTabBar::scroller {width: 0px;}"
            "QTabBar::tab:hover {background-color: #5357a0;}"
            "QTabBar::selected:hover {background-color: #5357a0;}"
            "QTabBar::tab:selected {background-color: #898cc2;}"
            "QTabBar::tab { background-color: #444783; font-size: 15px;"
            "color: white; height: 50px; width: 150px; margin-right: 2px; border-top-left-radius: 5px;"
            "border-top-right-radius: 5px}"
            "QLabel {color: white; max-width: 400px}"
            "QPushButton {color: white; background-color: #444783; max-width: 200px; height: 2em; font-size:15px;}"
            "QPushButton:hover {background-color: #5357a0;} QMenu { background-color: white; }"
            "QLineEdit {background-color: #444783; color: white; height: 2.5em; border: none;"
            "border-radius: 5px; padding-left: 5px; font-size: 15px;}"
        )
        # Set application title as given proxy
        self.browser_proxy = proxy
        self.setWindowTitle(self.browser_proxy)

        # Removes the ugly default icon with a transparent icon
        icon = QPixmap(1, 1)
        icon.fill(Qt.transparent)
        self.setWindowIcon(QIcon(icon))

        # Create the first page
        self.page = QWidget()

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.current_tab_changed)

        # Create the browser navigation layout
        self.navigationLayout = QHBoxLayout()
        self.navigationBack = QPushButton("<")
        self.navigationBack.clicked.connect(self.go_back)

        self.navigationForward = QPushButton(">")
        self.navigationForward.clicked.connect(self.go_forward)

        self.labelButton = QPushButton("Copy URL")
        self.labelButton.clicked.connect(self.copy_current_url)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.navigationLayout.addWidget(self.navigationBack)
        self.navigationLayout.addWidget(self.navigationForward)
        self.navigationLayout.addWidget(self.labelButton)
        self.navigationLayout.addWidget(self.url_bar)

        # Create a vertical layout to hold the tab widget and navigation layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(self.navigationLayout)

        # Set the page layout
        self.page.setLayout(self.layout)

        # Process the proxy and open the given links

        browser_proxystring = proxy

        if browser_proxystring != "None":
            proxy = QNetworkProxy()
            hostname, port, username, password = browser_proxystring.split(":")
            proxy.setType(QNetworkProxy.HttpProxy)
            proxy.setHostName(hostname)
            proxy.setUser(username)
            proxy.setPassword(password)
            proxy.setPort(int(port))

            # THE BELOW CODE SETS THE PROXY FOR THE ENTIRE APPLICATION
            QNetworkProxy.setApplicationProxy(proxy)

            # Opens one tab for each link provided (if a proxy is provided)
            for link in open(link_file).readlines():
                self.open_new_tab(link.replace("\n", ""), hostname)
        else:
            # Opens one tab for each link provided (without a proxy)
            for link in open(link_file).readlines():
                self.open_new_tab(link.replace("\n", ""), "None")

        self.setLayout(self.layout)
        self.layout.addWidget(self.page)

    def copy_current_url(self):
        """
        This function copies the current URL displayed in the current browser to the clipboard.
        """
        browser = self.tab_widget.currentWidget()
        cb = QApplication.clipboard()
        cb.setText(browser.url().toString(), mode=cb.Clipboard)

    def open_new_tab(self, url=None, proxy=None, profile=None):
        """
        This function opens a new tab with the specified URL, proxy and profile.
        If no URL is specified, the default URL is set to 'https://www.google.com'.
        The function creates a new QWebEngineView object, sets the URL and proxy,
        adds the browser to the tab widget, sets the current tab to the newly created tab,
        connects the loadProgress signal to the current_tab_changed function,
        and creates a context menu with various actions such as 'Reload', 'New Tab',
        'Duplicate Tab', 'Copy', 'Paste', 'Forward' and 'Back'.

        Parameters:
            - url (str): The URL to open in the new tab.
            - proxy (str): The proxy to be used for the new tab.
            - profile (str): The profile to be used for the new tab.
        """
        if not url:
            url = "https://www.google.com"
        browser = QWebEngineView()

        if not profile:
            # On Windows, session storage can be found below:
            # C:/Users/YOUR USER NAME/AppData/Local/python/QtWebEngine/storage-PROXY.HOST.NAME
            profile = QWebEngineProfile(f"storage-{proxy}", browser)

        webpage = QWebEnginePage(profile, browser)
        browser.setPage(webpage)
        browser.setUrl(QUrl(url))

        self.tab_widget.addTab(browser, url.split(".")[1])
        self.tab_widget.setCurrentWidget(browser)

        browser.loadProgress.connect(
            lambda: self.current_tab_changed(self.tab_widget.currentIndex())
        )

        # Create a context menu and add actions to it
        # Context menu is the menu that pops up when
        # a user right clicks on the browser page
        context_menu = QMenu(browser)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(browser.reload)

        new_action = QAction("New Tab", self)
        new_action.triggered.connect(lambda: self.open_new_tab())

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(lambda: self.go_forward())

        back_action = QAction("Back", self)
        back_action.triggered.connect(lambda: self.go_back())

        duplicate_action = QAction("Duplicate Tab", self)
        duplicate_action.triggered.connect(
            lambda: self.duplicate_tab(url, proxy, profile)
        )

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(
            lambda: browser.page().triggerAction(QWebEnginePage.Copy)
        )

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(
            lambda: browser.page().triggerAction(QWebEnginePage.Paste)
        )

        # Add actions to the context menu
        context_menu.addAction(new_action)
        context_menu.addAction(reload_action)
        context_menu.addAction(duplicate_action)
        context_menu.addAction(paste_action)
        context_menu.addAction(back_action)
        context_menu.addAction(forward_action)
        context_menu.addAction(copy_action)

        # Assign the context menu to the web engine view
        browser.setContextMenuPolicy(Qt.CustomContextMenu)
        browser.customContextMenuRequested.connect(
            lambda point: context_menu.exec_(browser.mapToGlobal(point))
        )

    def duplicate_tab(self, url, proxy, profile):
        """
        This function creates a duplicate tab of the current tab with the same URL, proxy, and profile settings.

        Parameters:
            - url (str): The URL to be loaded in the duplicate tab.
            - proxy (str): The proxy to be used in the duplicate tab.
            - profile (str): The profile to be used in the duplicate tab.
        """
        self.open_new_tab(url, proxy, profile)

    def go_back(self):
        """
        This function navigates the current tab to the previous page in the browsing history.
        """
        self.tab_widget.currentWidget().back()

    def go_forward(self):
        """
        This function navigates the current tab to the next page in the browsing history.
        """
        self.tab_widget.currentWidget().forward()

    def close_tab(self, index):
        """
        This function closes the tab at the specified index.

        Parameters:
            - index (int): The index of the tab to be closed.
        """
        self.tab_widget.removeTab(index)

    def navigate_to_url(self):
        """
        This function navigates the current tab to the URL entered in the URL bar.
        If the entered URL is missing the scheme (e.g. 'https://'), the function will add the scheme
        before navigating to the URL.
        """
        url = self.url_bar.text()
        parsed_url = urlparse(url)

        if not parsed_url.scheme:
            url = "https://" + url

        self.tab_widget.currentWidget().setUrl(QUrl(url))

    def current_tab_changed(self, index):
        """
        This function is called when the current tab is changed.
        It updates:
            URL bar with the URL of the current tab
            Updates tab with page title
            Logs the URL of the current tab

        Parameters:
            - index (int): The index of the current tab
        """
        browser = self.tab_widget.currentWidget()
        self.url_bar.setText(browser.url().toString())
        self.tab_widget.setTabText(index, browser.page().title())
        self.tab_widget.setTabToolTip(index, browser.page().title())
        f = open(
            f"./logs/{self.browser_proxy.replace('.', '-').replace(':', '-')}.txt", "a+"
        )
        f.write(
            f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} - {browser.url().toString()}\n'
        )


if __name__ == "__main__":
    """
    This is the entry point of the application. It creates an instance of the
    QApplication, an instance of the Browser class with the specified proxy and links,
    shows the browser and starts the event loop.
    """
    app = QApplication(sys.argv)
    browser = Browser(proxy=sys.argv[1], link_file=sys.argv[2])
    browser.show()
    sys.exit(app.exec_())
