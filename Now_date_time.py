from datetime import datetime
import Rap_time


class Now_date_time:

    def Now_date_time_1():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_list = Rap_time.Rap_time.rap_time_list

        now_1 = datetime.now()
        current_time_1 = now_1.strftime("%H:%M:%S")
        print("pro 1: " + str(current_time_1))

        rap_time_gap_list[0] = now_1
        rap_time_list[2] = current_time_1

    def Now_date_time_2():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_list = Rap_time.Rap_time.rap_time_list

        now_2 = datetime.now()
        current_time_2 = now_2.strftime("%H:%M:%S")
        print("pro 2: " + str(current_time_2))

        rap_time_gap_list[1] = now_2
        rap_time_list[3] = current_time_2

    def Now_date_time_3():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_list = Rap_time.Rap_time.rap_time_list

        now_3 = datetime.now()
        current_time_3 = now_3.strftime("%H:%M:%S")
        print("pro 3: " + str(current_time_3))

        rap_time_gap_list[2] = now_3
        rap_time_list[4] = current_time_3

    def Now_date_time_4():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_list = Rap_time.Rap_time.rap_time_list

        now_4 = datetime.now()
        current_time_4 = now_4.strftime("%H:%M:%S")
        print("pro 4: " + str(current_time_4))

        rap_time_gap_list[3] = now_4
        rap_time_list[5] = current_time_4

    def Now_date_time_5():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_list = Rap_time.Rap_time.rap_time_list

        now_5 = datetime.now()
        current_time_5 = now_5.strftime("%H:%M:%S")
        print("pro 5: " + str(current_time_5))

        rap_time_gap_list[4] = now_5
        rap_time_list[6] = current_time_5

    def Now_date_time_diff():
        rap_time_gap_list = Rap_time.Rap_time.rap_time_gap_list
        rap_time_gap_diff_list = Rap_time.Rap_time.rap_time_gap_diff_list

        diff_1 = rap_time_gap_list[1] - rap_time_gap_list[0]
        diff_2 = rap_time_gap_list[2] - rap_time_gap_list[1]
        diff_3 = rap_time_gap_list[3] - rap_time_gap_list[2]
        diff_4 = rap_time_gap_list[4] - rap_time_gap_list[3]

        rap_time_1 = diff_1.seconds
        rap_time_2 = diff_2.seconds
        rap_time_3 = diff_3.seconds
        rap_time_4 = diff_4.seconds

        rap_time_gap_diff_list[0] = rap_time_1
        rap_time_gap_diff_list[1] = rap_time_2
        rap_time_gap_diff_list[2] = rap_time_3
        rap_time_gap_diff_list[3] = rap_time_4

    def save():
        rap_time_list = Rap_time.Rap_time.rap_time_list
        rap_time_gap_diff_list = Rap_time.Rap_time.rap_time_gap_diff_list

        f = open("./rap_time/rap_time.txt", 'a')
        data = "\n------------------------------------------------------------------------------------------------\n\n" \
               ": order_number   :   %s   : menu_number  :   %s :\n" \
               "------------------------------------------------------------------------------------------------\n" \
               ":             :  order_insert  :  pick_up_cup  :  make_coffee  :    take_out    :   outlet_turn  :\n" \
               "------------------------------------------------------------------------------------------------\n" \
               ": start_time  :    %s    :     %s    :      %s    :     %s    :    %s    :\n" \
               "------------------------------------------------------------------------------------------------\n" \
               ":  rap_time   :      ----      %s       ----      %s       ----       %s       ----       %s       ----      :\n" \
               "------------------------------------------------------------------------------------------------\n" \
               "*--------*---------*---------------------------------------------------------*--------*--------*\n" \
               "*--------*---------*---------------------------------------------------------*--------*--------*\n" % (
                   rap_time_list[0], rap_time_list[1], rap_time_list[2], rap_time_list[3], rap_time_list[4], rap_time_list[5], rap_time_list[6],
                   rap_time_gap_diff_list[0], rap_time_gap_diff_list[1], rap_time_gap_diff_list[2], rap_time_gap_diff_list[3])
        f.write(data)
        f.close()



# a = Now_date_time.Now_date_time_1()
# b = Rap_time.Rap_time.rap_time_list
# c = Rap_time.Rap_time.rap_time_gap_list

# print(b)
# print(c)
