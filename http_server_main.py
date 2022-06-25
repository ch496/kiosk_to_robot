from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import database_query_main as DB
import model as model

DataDuplication_Check_Number = 0

class KioskServer(BaseHTTPRequestHandler):
    def do_POST(self):

        global  DataDuplication_Check_Number

        length = int(self.headers.get('content-length'))
        order_information_raw = json.loads(self.rfile.read(length).decode('utf-8'))
        orderNumber = int(order_information_raw['LISTS'][0]['LIST_H'][0]['BILL_NO'])


        # if (orderNumber == 1003 or orderNumber == model.DataDuplicationCheck.previousOrderNumber):
        #     return

        if (orderNumber == 1000 or orderNumber == model.DataDuplicationCheck.previousOrderNumber):
            return

        elif (order_information_raw != 1000 and orderNumber != DataDuplication_Check_Number):
            print("body:")
            print(order_information_raw)

            personOrderDataList = []
            for i in range(len(order_information_raw['LISTS'][1]['LIST_D'])):  # 1인의 주문 수량만큼 반복
                personOrderDataList.append([])

                personOrderDataList[i].append(orderNumber)  # 인덱스 0, 주문번호

                menuNumber = order_information_raw['LISTS'][1]['LIST_D'][i]['ITEM_CD']
                personOrderDataList[i].append(menuNumber)  # 인덱스 1, 메뉴 번호

                inputDate = order_information_raw['LISTS'][1]['LIST_D'][i]['ORDER_TM']
                date = inputDate[:4] + '-' +\
                       inputDate[4:6] + '-' +\
                       inputDate[6:8] + ' ' +\
                       inputDate[ 8:10] + ':' +\
                       inputDate[ 10:12] + ':' +\
                       inputDate[ 12:]
                personOrderDataList[i].append(date)  # 인덱스 2, 주문 시각

                qty = order_information_raw['LISTS'][1]['LIST_D'][i]['QTY']
                personOrderDataList[i].append(qty)  # 인덱스 3, 수량

                barcode = inputDate[:12] + menuNumber
                personOrderDataList[i].append(barcode)  # 인덱스 4, 바코드 번호

            print(personOrderDataList)

            dataBase = DB.DBQuery()
            dataBase.add_accumulated_data(personOrderDataList)

            flag = dataBase.existence_waiting_order()
            if flag == 1:  # 대기 주문이 있으면
                dataBase.add_waiting_order(personOrderDataList)
            if flag == 0:  # 대기 주문이 없으면
                dataBase.first_add_waiting_order(personOrderDataList)

        DataDuplication_Check_Number = model.DataDuplicationCheck.previousOrderNumber
        print("Da: " + str(DataDuplication_Check_Number))

        model.DataDuplicationCheck.previousOrderNumber = orderNumber
        


def start_http_server():
    #PORT = 80
    #server = HTTPServer(('192.168.1.8', PORT), KioskServer)
    PORT = 6001
    server = HTTPServer(('192.168.10.3', PORT), KioskServer)
    print('Kiosk Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    start_http_server()
