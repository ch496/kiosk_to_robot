from mrcms.mrcms_binary_protocol_client import *
from mrcms.mrscript_utility import *

import logging
import threading
import time

_logger = logging.getLogger('sqauremint')
_logger.setLevel(logging.DEBUG)

_pal = None
_cup_count = 1

_outlet = {
    # 0:{'occupying_order_number':None, 'is_empty':[True]}
}

_dish_to_motion_index_map = {
    1001: 11,  # 핫 아메리카노
    1002: 10,  # 아이스 아메리카노
    1003: 16,  # ?
    1004: 13,  # 카페라떼
    1005: 14,  # 아이스티
    1006: 12,  # 핫 초코
    1007: 16,
    1008: 17,
    1009: 18,
    1010: 19,
}

_put_on_outlet_to_motion_index_map = {
    (0, 0): 9,
    (1, 1): 8,
}

_flush_outlet_to_motion_index_map = {
    0: 17,
    1: 16,
}

_motion_bank_index_map = {
    0:0,
    101:101,
    107:107,
    106:106,
    108:108,
}


def make_dish(dish_id):
    _logger.debug("make_dish : %s", dish_id)
    motion_index = _dish_to_motion_index_map[dish_id]
    _pal.execute_motion_bank(motion_index, blocking=True)


def find_available_outlet_pair(order_number):
    for outlet_index in range(len(_outlet)):
        outlet = _outlet[outlet_index]
        if (outlet['occupying_order_number'] == None):
            return outlet_index, 0
        else:
            if (outlet['occupying_order_number'] == order_number):
                for position_index in range(len(outlet['is_empty'])):
                    if (outlet['is_empty'][position_index]):
                        return outlet_index, position_index

    ''' There is no availabe outlet now'''
    return None


def put_dish_to_outlet(order_number, outlet_index, outlet_position):
    _logger.debug("put_dish_to_outlet : %s, %s, %s", order_number, outlet_index, outlet_position)
    motion_index = _put_on_outlet_to_motion_index_map[(outlet_index, outlet_position)]
    _pal.execute_motion_bank(motion_index, blocking=True)
    _outlet[outlet_index]['occupying_order_number'] = order_number
    _outlet[outlet_index]['is_empty'][outlet_position] = False
    print(_outlet)
    if (outlet_position == len(_outlet[outlet_index]['is_empty']) - 1):
        return True
    else:
        return False


def wait_take_out(time_sec, outlet_index):
    time.sleep(time_sec)
    _outlet[outlet_index]['occupying_order_number'] = None
    _outlet[outlet_index]['is_empty'] = [True] * len(_outlet[outlet_index]['is_empty'])


def flush_outlet(outlet_index):
    _logger.debug("flush_outlet : %s", outlet_index)
    motion_index = _flush_outlet_to_motion_index_map[outlet_index]
    _pal.execute_motion_bank(motion_index, blocking=True)
    t = threading.Thread(target=wait_take_out, args=(100, outlet_index,))  # 대기 시간 값 초과
    t.start()


def init_squaremint(ip_address_of_robot, number_of_outlets, size_of_outlet):
    global _pal, _outlet
    _pal = PalRobot(ip_address_of_robot)
    _pal.connect()
    _pal.set_process_unit('MM_DEG_G')  # cf : M_RAD_KG

    _outlet = {}
    for index in range(number_of_outlets):
        outlet = {}
        outlet['occupying_order_number'] = None
        outlet['is_empty'] = [True] * size_of_outlet
        _outlet[index] = outlet


def carousel_place_detect():
    _pal.execute_motion_bank(0)


def robot_servo_on():
    _pal.set_servo_on_off_state(True)
    _pal.set_feed_rate(0.2)
    time.sleep(2)


def cup_change():
    global _cup_count

    if (_cup_count == 80):

        print("left")
        # 왼쪽
        if (_cup_count == 160):
            _cup_count == 0
        else:
            _pal.execute_motion_bank(7)
            _cup_count += 1
    else:
        print("right")
        # 오른쪽
        _pal.execute_motion_bank(6)
        _cup_count += 1

        return

def sensor_data(index):

    if (index == 0):
        outlet_1_sensor = _pal.get_digital_input(index=0)  # 반환 true/false 왼쪽
        print("outlet_1_sensor: " + str(outlet_1_sensor))

        if index == 0:
            return outlet_1_sensor
    elif (index == 1):
        outlet_2_sensor = _pal.get_digital_input(index=2)
        print("outlet_2_sensor: " + str(outlet_2_sensor))

        if index == 1:
            return outlet_2_sensor

    elif (index == 2):
        cup_1_sensor = _pal.get_digital_input(index=2)
        print("cup_1_sensor: " + str(cup_1_sensor))

        if index == 2:
            return cup_1_sensor

    elif (index == 3):
        cup_2_sensor = _pal.get_digital_input(index=3)
        print("cup_2_sensor: " + str(cup_2_sensor))

        if index == 3:
            return cup_2_sensor

    elif (index == 7):
        teach_mode_sensor = _pal.get_digital_input(index=7)
        print("teach_mode_sensor_on: " + teach_mode_sensor)

        if (index == 7):
            return teach_mode_sensor



def cup_change_2():
    # PL, out_put 7

    _pal.execute_motion_bank(106)
    time.sleep(2)

    while True:
        cup_2_sensor = sensor_data(3)
        time.sleep(1)

        if cup_2_sensor == True:
            # P1
            _pal.execute_motion_bank(101)
            time.sleep(1)

            break
        else:
            # PR
            _pal.execute_motion_bank(107)
            time.sleep(2)
            cup_1_sensor = sensor_data(2)
            if cup_1_sensor == True:
                #P1
                _pal.execute_motion_bank(101)
                time.sleep(1)

                break
            else:
                # PL
                _pal.execute_motion_bank(106)
                time.sleep(1)
                continue


def motion_bank(motion_id):
    _logger.debug("motion_bank : %s", motion_id)
    motion_index = _motion_bank_index_map[motion_id]
    _pal.execute_motion_bank(motion_index, blocking=True)












