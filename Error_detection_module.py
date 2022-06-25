
import Error_detection_check_list
import database_query_main as DB



class Error_detection_module:

    def waiting_menuNumber_error(waiting_menuNumber):
        dataBase = DB.DBQuery()

        Error_check_list_3 = Error_detection_check_list.Error_detection_check_list.Error_detection_check_C03_list

        if waiting_menuNumber != 1001 and \
            waiting_menuNumber != 1002 and \
            waiting_menuNumber != 1004 and \
            waiting_menuNumber != 1005 and \
            waiting_menuNumber != 1006:
            print(waiting_menuNumber)
            Error_check_code_C03_001 = Error_check_list_3[0]
            dataBase.update_error_check_code(Error_check_code_C03_001)

    def produced_position_error(produced_position):
        dataBase = DB.DBQuery()

        Error_check_list_3 = Error_detection_check_list.Error_detection_check_list.Error_detection_check_C03_list

        if produced_position != "1" and \
            produced_position != "2" and \
            produced_position != "3" and \
            produced_position != "4":
            print(produced_position)
            Error_check_code_C03_002 = Error_check_list_3[1]
            dataBase.update_error_check_code(Error_check_code_C03_002)

    def flag_outlet_1_NO_data(flag_outlet_1):
        dataBase = DB.DBQuery()

        Error_check_list_3 = Error_detection_check_list.Error_detection_check_list.Error_detection_check_C03_list

        if flag_outlet_1 == 0:
            print(flag_outlet_1)
            Error_check_code_C03_003 = Error_check_list_3[2]
            dataBase.update_error_check_code(Error_check_code_C03_003)

    def flag_outlet_2_NO_data(flag_outlet_2):
        dataBase = DB.DBQuery()

        Error_check_list_3 = Error_detection_check_list.Error_detection_check_list.Error_detection_check_C03_list

        if flag_outlet_2 == 0:
            print(flag_outlet_2)
            Error_check_code_C03_004 = Error_check_list_3[3]
            dataBase.update_error_check_code(Error_check_code_C03_004)










