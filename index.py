from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFrame, QHBoxLayout, QAbstractItemView,QDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFontMetrics
from qasync import QEventLoop
from sys import argv
from string import ascii_letters
from random import choice
from sqlite3 import connect
from dataManager import loaderDatabase
import asyncio
import ctypes, sys


""" from faker import Faker

fake = Faker()
db.addSession(str(fake.ipv4()), str(fake.mac_address()), str(fake.windows_platform_token())) """


with loaderDatabase() as db:
    print(db.sessions())


class addDevice(QDialog):
    def __init__(self):
        super().__init__()
        self.configure()
    
    def configure(self):
        def settingsConfigure():
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            self.setFixedSize(600, 200)
            self.setWindowTitle("Add Device...")
        
        def widgetsConfigure():
            self.__container = QWidget()
            self.__containerLayout = QVBoxLayout()
            self.__container.setLayout(self.__containerLayout)

            self.__frameButtons = QFrame()
            self.__frameButtonsLayout = QHBoxLayout()
            self.__frameButtons.setLayout(self.__frameButtonsLayout)
            self.confirm = QPushButton("Confirm")
            self.cancel = QPushButton("Cancel")


            self.__frameButtonsLayout.addWidget(self.confirm)
            self.__frameButtonsLayout.addWidget(self.cancel)

        widgetsConfigure()
        settingsConfigure()

class Application(QMainWindow):

    def __init__(self):
        super().__init__()
        self.configure()
    
    def configure(self):
        def geometryConfigure():
            self.setFixedSize(880, 550)
            #self.setWindowFlag(Qt.FramelessWindowHint)
            #self.setAttribute(Qt.WA_TranslucentBackground)
            
        
        def timerConfigure():
            self.timerTitleChanger = QTimer()
            self.timerTitleChanger.setInterval(25)
            self.timerTitleChanger.timeout.connect(self.changeTitle)
            self.timerTitleChanger.start()
        
        def widgetsConfigure():
            def selectClient(logicalIndex):
                self.__container.setSelectionMode(QAbstractItemView.SingleSelection)
                self.__container.selectRow(logicalIndex)
                self.__container.setSelectionMode(QAbstractItemView.NoSelection)
            
            self.__central = QWidget()
            self.__layout = QVBoxLayout()
            self.__layout.setContentsMargins(1, 0, 1, 0)
            self.__layout.setSpacing(0)
            
            self.__central.setLayout(self.__layout)
            self.setCentralWidget(self.__central)

            self.__container = QTableWidget()
            self.__container.setCornerButtonEnabled(False)
            self.__container.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.__container.horizontalHeader().setSectionsClickable(False)
            self.__container.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.__container.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
            self.__container.setSelectionMode(QAbstractItemView.NoSelection)
            self.__container.verticalHeader().sectionClicked.connect(selectClient)
            self.__container.verticalHeader().setDefaultSectionSize(25)
            self.__container.verticalHeader().setSectionsClickable(True)
            self.__container.setColumnCount(4)
            self.__container.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.__container.setHorizontalHeaderItem(0, QTableWidgetItem("Session"))
            self.__container.setHorizontalHeaderItem(1, QTableWidgetItem("Device Name"))
            self.__container.setHorizontalHeaderItem(2, QTableWidgetItem("Status"))
            self.__container.setHorizontalHeaderItem(3, QTableWidgetItem("____"))

            for row in range(self.__container.rowCount()):
                for col in range(self.__container.columnCount()):
                    item = QTableWidgetItem("Test")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.__container.setItem(row, col, item)
            
            for row in range(self.__container.rowCount()):
                btn = QPushButton("Connect")
                self.__container.setCellWidget(row, self.__container.columnCount() - 1, btn)

            self.__frame = QFrame()
            self.__frameLayout = QHBoxLayout()
            self.__frameLayout.setContentsMargins(0, 2, 0, 2)
            self.__frameLayout.setSpacing(0)
            self.__frame.setLayout(self.__frameLayout)
            
            self.__btn = QPushButton("Add Device")
            self.__btn.clicked.connect(self.addDeviceCommand)
            self.__frameLayout.addStretch()
            self.__frameLayout.addWidget(self.__btn)
            
            self.__layout.addWidget(self.__container)
            self.__layout.addWidget(self.__frame)

        widgetsConfigure()
        geometryConfigure()
        timerConfigure()
        self.show()
    
    def changeTitle(self):
        self.setWindowTitle("".join(choice(ascii_letters) for _ in range(choice([150, 200, 175, 250]))))
    
    def addDeviceCommand(self):
        self.windowDevice = addDevice()
        self.windowDevice.exec_()


if __name__ == "__main__":
    app = QApplication(argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    #interface = Application()
    subWindow = addDevice()
    subWindow.show()



    with loop:
        loop.run_forever()