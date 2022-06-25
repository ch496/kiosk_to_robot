import sys
from robopresso_main_simulator_4 import Ui_MainWindow  # 수정부분
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import qApp
from PyQt5 import uic
from PyQt5.QtCore import Qt
import database_query_main as DB
import robot_process_list


class kinwriter(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # self.timer = QTimer(self)
        # self.timer.setSingleShot(False)
        # self.timer.setInterval(5000) # in milliseconds, so 5000 = 5 seconds
        # # self.timer.timeout.connect(self.start_Macro)
        # self.timer.start()i0nscn2kdlr2k

        # print(self.hasMouseTracking())
        self.show()






app = QApplication([])
sn = kinwriter()
QApplication.processEvents()
sys.exit(app.exec_())