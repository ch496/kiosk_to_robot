from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import database_query_main as DB
import random_order


def order_insert(repeat_Number):
    order_list = random_order.random_order_list.order_list_button
    personOrderDataList = order_list[0]
    personOrderDataList[0][3] = str(repeat_Number)


    dataBase = DB.DBQuery()
    dataBase.add_accumulated_data(personOrderDataList)

    flag = dataBase.existence_waiting_order()
    if flag == 1:  # 대기 주문이 있으면
        dataBase.add_waiting_order(personOrderDataList)
        # dataBase.add_waiting_order_error(personOrderDataList)
    if flag == 0:  # 대기 주문이 없으면
        dataBase.first_add_waiting_order(personOrderDataList)
    # dataBase.first_add_waiting_order_error(personOrderDataList)









