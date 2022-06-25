
import pymysql.cursors  #pip install pymysql


class DBQuery:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'srs8688'
    DB = 'test'     #DB명 변경

    connection = pymysql.connect(host=HOST,
                            user=USER,
                            password=PASSWORD,
                            db=DB,
                            cursorclass=pymysql.cursors.DictCursor)

    def add_accumulated_data(self, list):
        cursor = DBQuery.connection.cursor()

        insert_sql = "insert into accumulated_data (menuNumber, date, qty) values (%s, %s, %s)"
        for i in range(len(list)):
            insert_val = (list[i][1], list[i][2], list[i][3])
            cursor.execute(insert_sql, insert_val)

        cursor.execute("set @count=0")
        cursor.execute("update accumulated_data set id=@count:=@count+1")

        DBQuery.connection.commit()

        print(i+1, "개의 레코드가 입력되었습니다. (accumulated_Data)")
        cursor.close()

    def add_waiting_order(self, list):
        cursor = DBQuery.connection.cursor()

        insert_sql = "insert into waiting_order (orderNumber, menuNumber, date, barcode, position) values (%s, %s, %s, %s, %s)"

        orderNumberList = []
        menuNumberList = []
        dateList = []
        barcodeList = []
        positionList = []

        #oldPosition
        select_sql = "select position from waiting_order order by id desc limit 1"
        cursor.execute(select_sql)

        allSelectOldPosition = cursor.fetchone()
        oldPosition = allSelectOldPosition.get('position')

        DBQuery.connection.commit()
        print("oldPosition : " + str(oldPosition))

        #totalQty
        totalQty = 0
        for i in range(len(list)):
            totalQty = totalQty + int(list[i][3])
            print("totalQty" + str(totalQty))

        # position

        # error
        if oldPosition == '1':
            if totalQty == 1:
                positionList.append(2)
            else:  # totalQty가 2이상일 때
                positionList.append(2)

                share = totalQty - 1 / 2
                rest = (totalQty - 1) % 2

                for i in range(int(share)):
                    for j in range(2):
                        positionList.append(j + 1)

                for k in range(rest):
                    positionList.append(k + 1)

        if oldPosition == '2':
            share = totalQty / 2
            rest = totalQty % 2

            for i in range(int(share)):
                for j in range(2):
                    positionList.append(j + 1)

            for k in range(rest):
                positionList.append(k + 1)


        print("newPosition : " + str(positionList[-1]))
        recode = 0
        for i in range(len(list)):
            for j in range(int(list[i][3])):
                orderNumberList.append(list[i][0])
                menuNumberList.append(list[i][1])
                dateList.append(list[i][2])
                barcodeList.append(list[i][4])

                recode += 1

        for i in range(totalQty):
            insert_val = (orderNumberList[i], menuNumberList[i], dateList[i], barcodeList[i], positionList[i])
            cursor.execute(insert_sql, insert_val)

        cursor.execute("set @count=0")
        cursor.execute("update waiting_order set id=@count:=@count+1")

        DBQuery.connection.commit()
        cursor.close()

    def first_add_waiting_order(self, list):
        cursor = DBQuery.connection.cursor()

        insert_sql = "insert into waiting_order (orderNumber, menuNumber, date, barcode, position) values (%s, %s, %s, %s, %s)"

        orderNumberList = []
        menuNumberList = []
        dateList = []
        barcodeList = []
        positionList = []

        totalQty = 0
        for i in range(len(list)):
            totalQty = totalQty + int(list[i][3])

        share = totalQty / 2
        rest = totalQty % 2

        for i in range(int(share)):
            for j in range(2):
                positionList.append(j + 1)
        for k in range(rest):
            positionList.append(k + 1)

        recode = 0
        for i in range(len(list)):
            for j in range(int(list[i][3])):
                orderNumberList.append(list[i][0])
                menuNumberList.append(list[i][1])
                dateList.append(list[i][2])
                barcodeList.append(list[i][4])

                recode += 1

        for i in range(totalQty):
            insert_val = (orderNumberList[i], menuNumberList[i], dateList[i], barcodeList[i], positionList[i])
            print(insert_val)
            cursor.execute(insert_sql, insert_val)

        cursor.execute("set @count=0")
        cursor.execute("update waiting_order set id=@count:=@count+1")

        DBQuery.connection.commit()
        cursor.close()

    def add_produced_order(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("insert into produced_order (orderNumber, menuNumber, barcode, position) select orderNumber, menuNumber, barcode, position from waiting_order limit 1")
        DBQuery.connection.commit()
        cursor.close()

    def add_outlet_1(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("insert into outlet_1 (barcode, position) select barcode, position from produced_order limit 1")

        cursor.execute("set @count=0")
        cursor.execute("update outlet_1 set id=@count:=@count+1")

        DBQuery.connection.commit()
        cursor.close()

    def add_outlet_2(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("insert into outlet_2 (barcode, position) select barcode, position from produced_order limit 1")

        cursor.execute("set @count=0")
        cursor.execute("update outlet_2 set id=@count:=@count+1")

        DBQuery.connection.commit()
        cursor.close()

    def delete_waiting_order(self):
        cursor = DBQuery.connection.cursor()

        cursor.execute("delete from waiting_order limit 1")
        cursor.execute("set @count=0")
        cursor.execute("update waiting_order set id=@count:=@count+1")

        DBQuery.connection.commit()
        cursor.close()

    def delete_produced_order(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("delete from produced_order limit 1")
        DBQuery.connection.commit()
        cursor.close()

    def delete_outlet_1(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("delete from outlet_1")
        DBQuery.connection.commit()
        cursor.close()

    def delete_outlet_2(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("delete from outlet_2")
        DBQuery.connection.commit()
        cursor.close()

    def select_waiting_order_orderNumber(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select orderNumber from waiting_order ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existOrderNumber = flag.get('flag')

        if existOrderNumber == 1:
            select_sql = "select orderNumber from waiting_order limit 1"
            cursor.execute(select_sql)

            orderNumber = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return orderNumber.get('orderNumber')

        if existOrderNumber == 0:
            return 0

    def select_waiting_order_orderNumber_second(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select orderNumber from waiting_order where id = 2 ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existOrderNumber = flag.get('flag')

        if existOrderNumber == 1:
            select_sql = "select orderNumber from waiting_order where id = 2"
            cursor.execute(select_sql)

            orderNumber = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return orderNumber.get('orderNumber')

        if existOrderNumber == 0:
            return 0

    def select_waiting_order_orderNumber_third(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select orderNumber from waiting_order where id = 3 ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existOrderNumber = flag.get('flag')

        if existOrderNumber == 1:
            select_sql = "select orderNumber from waiting_order where id = 3"
            cursor.execute(select_sql)

            orderNumber = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return orderNumber.get('orderNumber')

        if existOrderNumber == 0:
            return 0

    def select_waiting_order_orderNumber_fourth(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select orderNumber from waiting_order where id = 4 ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existOrderNumber = flag.get('flag')

        if existOrderNumber == 1:
            select_sql = "select orderNumber from waiting_order where id = 4"
            cursor.execute(select_sql)

            orderNumber = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return orderNumber.get('orderNumber')

        if existOrderNumber == 0:
            return 0

    def select_waiting_order_menuNumber(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select menuNumber from waiting_order limit 1"
        cursor.execute(select_sql)

        menuNum = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return menuNum.get('menuNumber')

    def select_waiting_order_position(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select position from waiting_order ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existPosition = flag.get('flag')

        if existPosition == 1:
            select_sql = "select position from waiting_order limit 1"
            cursor.execute(select_sql)

            position = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return position.get('position')

        if existPosition == 0:
            return "0"

    def select_produced_order(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select position from produced_order ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        existOrderNumber = flag.get('flag')

        if existOrderNumber == 1:
            select_sql = "select orderNumber from produced_order limit 1"
            cursor.execute(select_sql)

            orderNum = cursor.fetchone()
            DBQuery.connection.commit()

            cursor.close()
            return orderNum.get('orderNumber')

        if existOrderNumber == 0:
            return 0

    def select_produced_order_position(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select position from produced_order limit 1"
        cursor.execute(select_sql)

        orderNum = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return orderNum.get('position')

    def existence_waiting_order(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select * from waiting_order ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return flag.get('flag')

    def existence_outlet_1(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select * from outlet_1 ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return flag.get('flag')
    
    def existence_outlet_2(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select exists ( select * from outlet_2 ) as flag"
        cursor.execute(select_sql)

        flag = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return flag.get('flag')

    def select_len_waiting_order(self):
        cursor = DBQuery.connection.cursor()

        select_sql = "select count(id) as count from waiting_order"
        cursor.execute(select_sql)

        count = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return count.get('count')

    def update_process(self, processNumber):
        cursor = DBQuery.connection.cursor()

        update_sql = "update monitoring_data set process = %s"
        update_val = processNumber

        cursor.execute(update_sql, update_val)
        cursor.execute("select process from monitoring_data limit 1")

        DBQuery.connection.commit()
        cursor.close()

    def sensor_state(self, position, state):
        cursor = DBQuery.connection.cursor()

        if position == 1:
            if state == True:   #감지 된 상태
                update_sql = "update monitoring_data set sensor_1 = 1"
                cursor.execute(update_sql)
            if state == False:  #감지 안된 상태
                update_sql = "update monitoring_data set sensor_1 = 0"
                cursor.execute(update_sql)
        if position == 2:
            if state == True:
                update_sql = "update monitoring_data set sensor_2 = 1"
                cursor.execute(update_sql)
            if state == False:
                update_sql = "update monitoring_data set sensor_2 = 0"
                cursor.execute(update_sql)

        DBQuery.connection.commit()
        cursor.close()

    def show_accumulated_data(self):
        cursor = DBQuery.connection.cursor()
        accumulated_data_sql = "select * from accumulated_data"
        cursor.execute(accumulated_data_sql)

        row = cursor.fetchone()
        print(row)

    def show_monitoring_data(self):
        cursor = DBQuery.connection.cursor()
        monitoring_data_sql = "select * from monitoring_data"
        cursor.execute(monitoring_data_sql)

        row = cursor.fetchone()
        print(row)

    def show_wating_order_data(self):
        cursor = DBQuery.connection.cursor()
        waiting_order_data_sql = "select * from waiting_order"
        cursor.execute(waiting_order_data_sql)

        row = cursor.fetchone()
        print(row)

    def show_produced_order_data(self):
        cursor = DBQuery.connection.cursor()
        waiting_order_data_sql = "select * from waiting_order"
        cursor.execute(waiting_order_data_sql)

        row = cursor.fetchone()
        print(row)

    def show_produced_order_data(self):
        cursor = DBQuery.connection.cursor()
        produced_order_data_sql = "select * from waiting_order"
        cursor.execute(produced_order_data_sql)

        row = cursor.fetchone()
        print(row)

    def process_reading(self):

        cursor = DBQuery.connection.cursor()

        process_sql = "select process from monitoring_data limit 1"

        cursor.execute(process_sql)


        process = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return process.get('process')

    def sensor_1_reading(self):

        cursor = DBQuery.connection.cursor()

        sensor_1_sql = "select sensor_1 from monitoring_data limit 1"

        cursor.execute(sensor_1_sql)

        sensor_1 = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return sensor_1.get('sensor_1')

    def sensor_2_reading(self):

        cursor = DBQuery.connection.cursor()

        sensor_2_sql = "select sensor_2 from monitoring_data limit 1"

        cursor.execute(sensor_2_sql)

        sensor_2 = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return sensor_2.get('sensor_2')

    def add_monitoring(self):
        cursor = DBQuery.connection.cursor()
        cursor.execute("insert into monitoring_data (process, sensor_1, sensor_2) value (0, 0, 0)")
        DBQuery.connection.commit()
        cursor.close()

    def update_error_check_code(self, Error_check_code_list3):

        cursor = DBQuery.connection.cursor()

        update_sql = "update error_check_code set error_check_code = %s"
        update_val = Error_check_code_list3

        cursor.execute(update_sql, update_val)
        cursor.execute("select error_check_code from error_check_code limit 1")

        DBQuery.connection.commit()
        cursor.close()

    def select_error_check_code(self):
        cursor = DBQuery.connection.cursor()

        Error_check_code_sql = "select error_check_code from error_check_code limit 1"

        cursor.execute(Error_check_code_sql)

        Error_check_code = cursor.fetchone()
        DBQuery.connection.commit()

        cursor.close()
        return Error_check_code.get('error_check_code')

    def reset_update_error_check_code(self, Error_check_code_NO):

        cursor = DBQuery.connection.cursor()

        update_sql = "update error_check_code set error_check_code = %s"
        update_val = Error_check_code_NO

        cursor.execute(update_sql, update_val)
        cursor.execute("select error_check_code from error_check_code limit 1")

        DBQuery.connection.commit()
        cursor.close()



