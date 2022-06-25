import sys
from Error_status_2 import Ui_MainWindow  # 수정부분
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
import Error_detection_check_list



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
        self.showFullScreen()


        while True:
            DataBase = DB.DBQuery()

            Error_check_code_NO = Error_detection_check_list.Error_detection_check_list.Error_detection_check_code
            Error_check_code = DataBase.select_error_check_code()

            waitingOrderCount = DataBase.select_len_waiting_order()
            self.waiting_operation.setText(str(waitingOrderCount))

            robot_process = DataBase.process_reading()

            if robot_process == 0:
                process_0 = robot_process_list.robot_process_list.robot_process_0
                self.order_waiting.setText(process_0)
            else:
                self.order_waiting.setText("")

            if robot_process == 1:
                process_1 = robot_process_list.robot_process_list.robot_process_1
                self.pick_up_cup.setText(process_1)
            else:
                self.pick_up_cup.setText("")

            if robot_process == 2:
                process_2 = robot_process_list.robot_process_list.robot_process_2
                self.make_beverage.setText(process_2)
            else:
                self.make_beverage.setText("")

            if robot_process == 3:
                process_3 = robot_process_list.robot_process_list.robot_process_3
                self.outlet_to_beverage.setText(process_3)
            else:
                self.outlet_to_beverage.setText("")


            if robot_process == 4:
                process_4 = robot_process_list.robot_process_list.robot_process_0
                self.turn_outlet.setText(process_4)
            else:
                self.turn_outlet.setText("")

            if Error_check_code == str(Error_check_code_NO[0]):
                self.Error_code.setText("")
            else:
                self.Error_code.setText(str(Error_check_code))

            QApplication.processEvents()
            time.sleep(1)

    def keyPressEvent(self, k):
        Database = DB.DBQuery()
        Error_check_code_NO = Error_detection_check_list.Error_detection_check_list.Error_detection_check_code[0]

        if k.key() == Qt.Key_Escape:
            sys.exit()
        if k.key() == Qt.Key_F:
            self.showFullScreen()
        if k.key() == Qt.Key_R:
            Database.reset_update_error_check_code(Error_check_code_NO)









app = QApplication([])
sn = kinwriter()
QApplication.processEvents()
sys.exit(app.exec_())