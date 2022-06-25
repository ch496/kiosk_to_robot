import time
import threading

from mrcms.mrcms_binary_protocol_client import *
from mrcms.mrscript_utility import *
import database_query_main as DB
import sqauremint_main as squaremint
import soundplayer as sound
from datetime import datetime
import Rap_time
import Now_date_time
import Error_detection_module
import Error_detection_check_list



def main_loop():
    dataBase = DB.DBQuery()
    rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
    rap_time_gap_diff_list = Rap_time.Rap_time.rap_time_gap_diff_list
    rap_time_list = Rap_time.Rap_time.rap_time_list

    while True:
        Error_check_list_3 = Error_detection_check_list.Error_detection_check_list.Error_detection_check_C03_list
        # flag == 1 제조중인것
        flag_waiting_order = dataBase.existence_waiting_order()

        if flag_waiting_order == 1:
            waiting_menuNumber = dataBase.select_waiting_order_menuNumber()
            print("order insert")

            Error_detection_module.Error_detection_module.waiting_menuNumber_error(waiting_menuNumber)
            #Error_check_code = dataBase.select_error_check_code()
            while True:
                Error_check_code = dataBase.select_error_check_code()
                if Error_check_code == Error_check_list_3[0]:
                    print("C03_001")
                    time.sleep(1)
                else:
                    break

            rap_time_list[1] = waiting_menuNumber
            Now_date_time.Now_date_time.Now_date_time_1()

            #    sound.OrderNumberSound(dataBase.select_waiting_order_orderNumber())
            #    sound.OrderStart()

            dataBase.add_produced_order()
            dataBase.delete_waiting_order()

            print("\nmenuNumber " + str(waiting_menuNumber) + " making start")
            time.sleep(0.5)


            # 컵 뽑기
           #  squaremint.cup_change_2()
            time.sleep(5)
            dataBase.update_process(1)
            time.sleep(0.5)

            Now_date_time.Now_date_time.Now_date_time_2()

            print("pick a cup ...")

            # 음료 제조
           #  squaremint.make_dish(waiting_menuNumber)
            time.sleep(10)
            dataBase.update_process(2)
            time.sleep(0.5)

            Now_date_time.Now_date_time.Now_date_time_3()

            print("making ...")

            produced_position = dataBase.select_produced_order_position()

            Error_detection_module.Error_detection_module.produced_position_error(produced_position)
            #Error_check_code = dataBase.select_error_check_code()
            while True:
                Error_check_code = dataBase.select_error_check_code()
                if Error_check_code == Error_check_list_3[1]:
                    print("C03_002")
                    time.sleep(1)
                else:
                    break

            if produced_position == "1":
                outlet_index = 0
                outlet_position = 0
            if produced_position == "2":
                outlet_index = 1
                outlet_position = 1
            #        if produced_position == "3":
            #            outlet_index = 1
            #            outlet_position = 0
            #        if produced_position == "4":
            #            outlet_index = 1
            #            outlet_position = 1

            # 회전판 센서
            if outlet_index == 0:
                while True:
                    outlet_1_sensor = dataBase.sensor_1_reading()
                    if outlet_1_sensor == True:
                        print("1번 토출구 센서 감지")
                        time.sleep(1)
                    if outlet_1_sensor == False:
                        break

            if outlet_index == 1:
                while True:
                    outlet_2_sensor = dataBase.sensor_2_reading()
                    if outlet_2_sensor == True:
                        print("2번 토출구 센서 감지")
                        time.sleep(1)
                    if outlet_2_sensor == False:
                        break

            produced_orderNumber = dataBase.select_produced_order()
            rap_time_list[0] = produced_orderNumber

            print("outlet_index: " + str(outlet_index))
            print("outlet_position: " + str(outlet_position))
            print("produced_orderNumber: " + str(produced_orderNumber))



            # 음료 투출
           #  squaremint.put_dish_to_outlet(produced_orderNumber, outlet_index, outlet_position)
            time.sleep(5)
            dataBase.update_process(3)
            time.sleep(0.5)

            Now_date_time.Now_date_time.Now_date_time_4()

            if outlet_index == 0:
            #    print("outlet_1_NO_insert")
                dataBase.add_outlet_1()

            if outlet_index == 1:
            #    print("outlet_2_NO_insert")
                dataBase.add_outlet_2()

            dataBase.delete_produced_order()

            time.sleep(0.5)

            # 회전판
            waiting_orderNumber = dataBase.select_waiting_order_orderNumber

            if flag_waiting_order == 0 or produced_orderNumber != waiting_orderNumber:

                waiting_position = dataBase.select_waiting_order_position()
                if int(waiting_position) != int(
                        produced_position) + 1:  # 다음 주문이 지금 주문 position값+1이 아니면(투출구에 더 놓일 게 없으면)
                    flag_outlet_1 = dataBase.existence_outlet_1()
                    flag_outlet_2 = dataBase.existence_outlet_2()
                    if flag_outlet_1 == 1:
                       #  squaremint.flush_outlet(0)
                        time.sleep(5)
                        dataBase.update_process(4)
                        time.sleep(0.5)

                        Now_date_time.Now_date_time.Now_date_time_5()
                        Now_date_time.Now_date_time.Now_date_time_diff()
                        Now_date_time.Now_date_time.save()

                        print(rap_time_list)
                        print(rap_time_gap_diff_list)

                        print("1번 토출구")
                        dataBase.delete_outlet_1()

                    else:
                        Error_detection_module.Error_detection_module.flag_outlet_1_NO_data(flag_outlet_1)
                        #Error_check_code = dataBase.select_error_check_code()
                        while True:
                            Error_check_code = dataBase.select_error_check_code()
                            if Error_check_code == Error_check_list_3[2]:
                                print("C03_003")
                                time.sleep(1)
                            else:
                                break


                    if flag_outlet_2 == 1:
                       #  squaremint.flush_outlet(1)
                        time.sleep(5)
                        dataBase.update_process(4)
                        time.sleep(0.5)

                        Now_date_time.Now_date_time.Now_date_time_5()
                        Now_date_time.Now_date_time.Now_date_time_diff()
                        Now_date_time.Now_date_time.save()

                        print(rap_time_list)
                        print(rap_time_gap_diff_list)

                        print("2번 토출구")
                        dataBase.delete_outlet_2()

                    else:
                        Error_detection_module.Error_detection_module.flag_outlet_2_NO_data(flag_outlet_2)
                        #Error_check_code = dataBase.select_error_check_code()
                        while True:
                            Error_check_code = dataBase.select_error_check_code()
                            if Error_check_code == Error_check_list_3[3]:
                                print("C03_004")
                                time.sleep(1)
                            else:
                                break

                    # 음성출력
                #    sound.OrderNumberSound(produced_orderNumber)
                #    sound.OrderComplete()

            dataBase.update_process(0)
            print("menuNumber " + str(waiting_menuNumber) + " making finish\n")

        if flag_waiting_order == 0:
            time.sleep(1)


if __name__ == '__main__':
    # squaremint.init_squaremint('192.168.10.10', 2, 2)
    # squaremint.robot_servo_on()

    # robopresso_thread = threading.Thread(target=main_loop)
    # http_thread = threading.Thread(target=http_server.start_http_server)

    # print('start http')
    # http_thread.start()
    print('start main')
    # robopresso_thread.start()

    main_loop()
