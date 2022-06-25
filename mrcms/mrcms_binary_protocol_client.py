'''
Copyright (C) MINTROBOT Co., Ltd. - All Rights Reserved

'''

import logging
import socket
import math
import threading
import time
import struct
import json
from mrcms.mrscript_utility import *
from typing import List

class PalRobot():
            
    __command_id_lookup_table = {
        # robot control commands
        'stop': 0,
        'stop_joint': 1,
        'stop_linear': 2,
        'pause': 3,
        'resume': 4,
        'move_joint_with_q': 5,
        'move_joint': 6,
        'move_linear': 7,
        'move_circle': 8,
        'speed_joint_with_qq': 9,  # Future
        'speed_joint': 10,  # Future
        'speed_linear': 11,  # Future
        'is_finished': 12, 
        'solve_forward_kinematics': 13,
        'solve_inverse_kinematics': 14,

        # robot setting command
        'set_direct_teaching_on_off_state': 20,
        'set_tool_information': 21,
        'set_collision_detection_sensitivity': 22,
        'set_collision_detection_mode': 23,
        'set_user_joint_limit': 25,
        'set_user_joint_limit_on_off_state': 26,
        'set_feed_rate': 28,
        'forcely_set_arrived_status_to_true': 29,

        # servo drive setting
        'set_servo_on_off_state': 50,
        'reset_servo_error': 51,
        'reset_servo_absolute_encoder': 52,
        'set_servo_encoder_origin': 53,
        'set_all_servo_to_quickstop': 54,

        # robot status
        'get_actual_joint_position': 150,
        'get_actual_joint_velocity': 151,
        'get_actual_task_pose': 152,
        'get_actual_task_velocity': 153,
        'get_target_joint_position': 154,
        'get_target_joint_velocity': 155,
        'get_target_task_pose': 156,
        'get_target_task_velocity': 157,
        'get_joint_torque': 158,
        'get_joint_temperature': 159,
        'get_task_force': 160,
        'get_current_feed_rate': 163,
        'get_current_is_finished_state': 164,
        'get_current_tool_setting': 165,
        'get_current_user_joint_limit': 166,
        'get_current_user_joint_limit_on_off_state': 167,
        'get_current_default_joint_limit': 168,
        'get_current_actual_joint_limit': 169,

        # bank control
        'get_tool_bank': 201,
        'get_pose_bank': 203,
        'execute_motion_bank': 206,
        'stop_executing_motion_bank': 207,

        # IO control
        'set_digital_output':231,
        'get_digital_input':232,
        'set_all_digital_output_as_number':233,
        'get_all_digital_input_as_number':234,
        'register_io_digital_input_event_callback_function':235,

        # modbus control
        'set_modbus_register_value': 221,
        'get_modbus_register_value': 222,
        'register_modbus_co_event_callback_function': 223,
                
        # Accessory
        'process_transaction_with_accessory':241,

    }
        
    '''
    CONSTRUCTOR and DESTRUCTOR
    '''    
    def __init__(self, ip_address):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.INFO)

        self.__ip_address = ip_address
        
        self.__is_connected = False
        
        # Display unit   
        self.__process_unit = 'MM_DEG_G'

        # Sever parameter
        self.__server_lookup_table = {
            'COMMAND': {'name': 'Command Server', 'socket': None, 'port': 13001, 'semaphore': threading.Semaphore(1), 'connection': False},
            'EVENT' : {'name': 'Event Server', 'socket': None, 'port': 13002, 'semaphore': threading.Semaphore(1), 'connection': False},
        }

    '''
    PUBLIC FUNCTIONS
    '''    
    # ------------------------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------------------------
    def set_process_unit(self, unit):
        self.__process_unit = unit

        
    # ------------------------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------------------------
    def connect(self):
        command_server = self.__server_lookup_table['COMMAND']
        event_server = self.__server_lookup_table['EVENT']

        if (self.__is_connected):
            return 0
                
        command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        command_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        event_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        try:
            ''' --- pairing process '''
            ''' 1). connect to both command and event server '''
            command_socket.connect((self.__ip_address, command_server['port']))
            event_socket.connect((self.__ip_address, event_server['port']))

            ''' 2). receive command server's socket_fid '''
            packed_data = self.__receive_data(command_socket)
            unpacked_data = struct.unpack('<i', packed_data)
            command_socket_fid = unpacked_data[0]

            ''' 3). receive event server's socket_fid '''
            packed_data = self.__receive_data(event_socket)
            unpacked_data = struct.unpack('<i', packed_data)
            event_socket_fid = unpacked_data[0]
            
            ''' 3). send received socket_fid to each server crossly '''
            self.__send_data(command_socket, struct.pack('<i', event_socket_fid))
            self.__send_data(event_socket, struct.pack('<i', command_socket_fid))

            ''' 4). wait pairing process is confirmed '''
            ''' 5). receive command server's socket_fid for cross check '''
            packed_data = self.__receive_data(command_socket)
            unpacked_data = struct.unpack('<i', packed_data)
            command_socket_fid_crosscheck = unpacked_data[0]

            ''' 6). receive event server's socket_fid for cross check '''
            packed_data = self.__receive_data(event_socket)
            unpacked_data = struct.unpack('<i', packed_data)
            event_socket_fid_crosscheck = unpacked_data[0]
            ''' --- paring process end '''

            ''' 7). compare the received socket_fids for the final checking '''
            if ((command_socket_fid == command_socket_fid_crosscheck) and (event_socket_fid == event_socket_fid_crosscheck)):
                   
                ''' Start event process thread (event process only receive packet from the event server) '''
                event_process_thread = threading.Thread(target=self.__event_process, args=(event_socket,))
                event_process_thread.daemon = True
                event_process_thread.start()
                                 
        except Exception as e:
            self.__logger.warning('connected to mrscsript binary protocol server failed')
            command_socket.close()
            event_socket.close()
            command_server['socket'] = None
            command_server['connection'] = False
            event_server['socket'] = None
            event_server['connection'] = False
            self.__is_connected = False
            return -1
        else:
            self.__logger.info('connected to mrscsript binary protocol server')
            command_server['socket'] = command_socket
            command_server['connection'] = True
            event_server['socket'] = event_socket
            event_server['connection'] = True
            self.__is_connected = True
            return 0


    def disconnect(self): 
        for server in self._server_lookup_table:
            if (server['connection'] == True):
                try:
                    server['socket'].close()
                except Exception:
                    self.__logger.warning("Cannot close socket %s", server['name'])
                    res = -1
                else:
                    self.__logger.info("disconnected from %s", server['name'])
                finally:
                    server['connection'] = False
                    server['socket'] = None 
                    self.__is_connected = False
        return 0


    def is_connected(self, server_name):
        return self.__is_connected


    ''' 
    ------------------------------------------------------------------------------------
    Command Server 
    ------------------------------------------------------------------------------------              
    '''


    '''
    ============================================================================================
    1. Robot manipulation
    ============================================================================================
    '''    
    def stop(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['stop'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
    
    def pause(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['pause'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    def resume(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['resume'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]

    
    '''
    move_joint_with_q : move joints to the absolute position
    1. argument
        destination_q : target joint angle list (j1 ~ j7), absolute angle
        q_velocity : target joint velocity
        q_acceleration : target joint acceleration
        q_deceleration : target joint deceleration

    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''
    def move_joint_with_q(self, destination_q:list, q_velocity:float = -1, q_acceleration:float = -1, q_deceleration:float = -1, blocking:bool = True):
        if("MM_DEG_G" == self.__process_unit):
            destination_q_list = [math.radians(destination_q[i]) for i in range(len(destination_q))]
            destination_q_list[2]=0.001*destination_q[2]
            print(destination_q_list)

            q_velocity, q_acceleration, q_deceleration = map(lambda x : math.radians(x) if x else x, [q_velocity, q_acceleration, q_deceleration])
 
        destination_q_list.extend([0] * (7-len(destination_q)))       
        packed_command = struct.pack('<B7dddd', self.__command_id_lookup_table['move_joint_with_q'], *destination_q_list, q_velocity, q_acceleration, q_deceleration)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (blocking == True):
                return self.wait_finish(10)
            else:
                return 0
        else:
            return -1


    '''
    move_joint : move to the position by joint interpolation
    1. argument
        destination_pose : target pose (position and orientation)
        velocity : target joint velocity
        acceleration : target joint acceleration
        deceleration : target joint deceleration
        tool_bank_index : tool bank index to apply only for this command (if nagative, current tool bank is used)
        finish_mode : finish mode (-1 : fine, 0 : ruff)

    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''
    def move_joint(self, destination_pose:Pose, q_velocity:float = -1, q_acceleration:float = -1, q_deceleration:float = -1, tool_bank_index:int=-1, finish_mode:int=0, blocking:bool=True):
        if ("MM_DEG_G" == self.__process_unit):
            destination_pose = to_meter_radian(destination_pose)
            q_velocity, q_acceleration, q_deceleration = map(lambda x : math.radians(x) if x else x, [q_velocity, q_acceleration, q_deceleration])
            
        packed_command = struct.pack('<B6ddddbb', self.__command_id_lookup_table['move_joint'], *destination_pose, q_velocity, q_acceleration, q_deceleration, tool_bank_index, finish_mode)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (blocking == True):
                return self.wait_finish(10)
            else:
                return 0
        else:
            return -1
        
        
    '''
    move_linear : move to the position by linear interpolation
    1. argument
        destination_pose : target pose (position and orientation)
        velocity : target velocity
        acceleration : target acceleration
        deceleration : target deceleration
        tool_bank_index : tool bank index to apply only for this command (if nagative, current tool bank is used)
        finish_mode : finish mode (-1 : fine, 0 : ruff)
        waypoint_list : waypoint instances

    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''    
    def move_linear(self, destination_pose:Pose, velocity:float = -1, acceleration:float = -1, deceleration:float = -1, tool_bank_index:int=-1, finish_mode:int=-1, waypoint_list:List[WayPoint]=[], blocking:bool=True):
        if ("MM_DEG_G" == self.__process_unit):
            destination_pose = to_meter_radian(destination_pose)
            velocity, acceleration, deceleration = map(lambda x : x*0.001 if x else x, [velocity, acceleration, deceleration])
            waypoint_list = [to_meter_radian(waypoint_list[i]) for i in range(len(waypoint_list))]

        number_of_waypoionts = len(waypoint_list)
        packed_command = struct.pack('<B6ddddbbi', self.__command_id_lookup_table['move_linear'], *destination_pose, velocity, acceleration, deceleration, tool_bank_index, finish_mode, number_of_waypoionts)
        if (number_of_waypoionts > 0):    
            packed_waypoint_list = [struct.pack('<6d', *(waypoint_list[i].pose)) for i in range(number_of_waypoionts)]
            packed_radius_list = [struct.pack('<d', waypoint_list[i].radius) for i in range(number_of_waypoionts)]
            for i in range(number_of_waypoionts):
                packed_command += packed_waypoint_list[i]
            for i in range(number_of_waypoionts):
                packed_command += packed_radius_list[i]                      

        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (blocking == True):
                return self.wait_finish(10)
            else:
                return 0
        else:
            return -1
            
            
    '''
    move_circle : move to the position by 3 points circle interpolation
    1. argument
        destination_pose : target pose (position and orientation)
        via_pose : via pose (position and orientation, but only position is used)
        velocity : target velocity
        acceleration : target acceleration
        deceleration : target deceleration
        tool_bank_index : tool bank index to apply only for this command (if nagative, current tool bank is used)
        finish_mode : finish mode (-1 : fine, 0 : ruff)

    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''              
    def move_circle(self, destination_pose:Pose, via_pose:Pose, velocity:float=-1, acceleration:float=-1, deceleration:float=-1, tool_bank_index:int=-1, finish_mode:int=-1, blocking:bool=True):
        if ("MM_DEG_G" == self.__process_unit):
            destination_pose = to_meter_radian(destination_pose)
            via_pose = to_meter_radian(via_pose)        
            velocity, acceleration, deceleration = map(lambda x : x*0.001 if x else x, [velocity, acceleration, deceleration])

        packed_command = struct.pack('<B6d6ddddbb', self.__command_id_lookup_table['move_circle'], *destination_pose, *via_pose, velocity, acceleration, deceleration, tool_bank_index, finish_mode)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (blocking == True):
                return self.wait_finish(10)
            else:
                return 0
        else:
            return -1
    
    
    '''
    solve_forward_kinematics_solution : solve the forward kinematics problem
    1. argument
        target_q : target joint angle list (j1 ~ j7), absolute angle

    2. return    
        result : (0 : success, -1 : failed to solve)
        forward_kunematics_pose : solved pose
    '''      
    def solve_forward_kinematics(self, target_q_list:List[float]):
        packed_command = struct.pack('<B7d', self.__command_id_lookup_table['solve_forward_kinematics'], *target_q_list)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("6d", packed_response)
        forward_kinematics_position = unpacked_response[0][0:3]
        forward_kinematics_orientation = unpacked_response[0][3:6]
        forward_kinematics_solution = Pose(forward_kinematics_position, forward_kinematics_orientation)
        
        if ("MM_DEG_G" == self.__process_unit):
            forward_kinematics_solution = to_millimeter_degree(forward_kinematics_solution)
            
        return forward_kinematics_solution
        
        
    '''
    solve_inverse_kinematics_solution : solve the inverse kinematics problem
    1. argument
        target_p : target pose (position and orientation)

    2. return    
        result : (0 : success, -1 : failed to solve)
        inverse_kinematics : solved joint angle list
    '''           
    def solve_inverse_kinematics(self, target_p:Pose):
        if ("MM_DEG_G" == self.__process_unit):
            destination_pose = [math.radians(target_p[i]) for i in range(len(target_p))]
            
        packed_command = struct.pack('<B6d', self.__command_id_lookup_table['solve_inverse_kinematics'], *target_p)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("7d", packed_response)
        inverse_kinematics_solution = unpacked_response
        
        if ("MM_DEG_G" == self.__process_unit):
            inverse_kinematics_solution = [math.degrees(inverse_kinematics_solution[i]) for i in range(len(inverse_kinematics_solution))]
        
        return inverse_kinematics_solution


    def is_finished(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['is_finished'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
    
    def wait_finish(self, wait_mode:int = -1, timeout_sec:float = -1):
        elapsed_time = 0
        condition = 1 if wait_mode < 0 else (1 or 10)
        while True:
            if self.is_finished() ==  condition:
                return 0
            if (timeout_sec > 0 and elapsed_time >= timeout_sec):
                return 1
            elapsed_time += 0.01
            try:
                time.sleep(0.01)
            except Exception as e:
                pass
            

    '''
    ============================================================================================
    2. Robot setting
    ============================================================================================
    '''
    
    '''
    set_direct_teaching_on_off_state : set the direct teaching mode state
    1. argument
        state : state for direct teaching mode

    2. return    
        result : (0 : success, -1 : failed to set, -2 : comamnd denided because of some higher priority)
        inverse_kinematics : solved joint angle list
    '''    
    def set_direct_teaching_on_off_state(self, state:bool):
        packed_command = struct.pack('<B?', self.__command_id_lookup_table['set_direct_teaching_on_off_state'], state)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    set_tool_option : set tool option and apply it immediately
    1. argument
        tool_center_position : x, y, z position of the tool center point (TCP)
        center_of_mass_position : x, y, z position of the center of mass
        mass : mass of the tool
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''    
    def set_tool_option(self, tool_option:ToolOption):
        if ("MM_DEG_G" == self.__process_unit):
            tool_option = to_meter_radian(tool_option)
            
        tool_center_position = tool_option.position
        center_of_mass_position = tool_option.center_of_mass
        mass = tool_option.mass
            
        packed_command = struct.pack('<B3d3dd', self.__command_id_lookup_table['set_tool_information'], *tool_center_position, *center_of_mass_position, mass)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
    
    '''
    set_collision_detection_sensitivity : set the sensitivity parameter for collision detection algorithm
    1. argument
        sensitivity : sensitivity parameter
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''   
    def set_collision_detection_sensitivity(self, sensitivity:float):
        packed_command = struct.pack('<Bd', self.__command_id_lookup_table['set_collision_detection_sensitivity'], sensitivity)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    set_collision_detection_mode : set the collision detection mode
    1. argument
        detection_mode : detection mode
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''   
    def set_collision_detection_mode(self, detection_mode:int):
        packed_command = struct.pack('<Bb', self.__command_id_lookup_table['set_collision_detection_mode'], detection_mode)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    set_user_joint_limit : set user joint limit
    1. argument
        joint_index : joint index to set
        nagative_limit : nagative joint limit
        positive_limit : positive joint limit
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''   
    def set_user_joint_limit(self, joint_index:int, nagative_limit:float, positive_limit:float):
        if ("MM_DEG_G" == self.__process_unit):
            nagative_limit = math.radians(nagative_limit)
            positive_limit = math.radians(positive_limit)

        packed_command = struct.pack('<Bidd', self.__command_id_lookup_table['set_user_joint_limit'], joint_index, nagative_limit, positive_limit)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    set_user_joint_limit_on_off_state : set user joint limit on/off state
    1. argument
        state : user joint limit activation state
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''         
    def set_user_joint_limit_on_off_state(self, state:bool):
        packed_command = struct.pack('<B?', self.__command_id_lookup_table['set_user_joint_limit_on_off_state'], state)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
    
    '''
    set_feed_rate : set feed rate of the whole motion
    1. argument
        feed_rate : feed_rate
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''          
    def set_feed_rate(self, feed_rate:float):
        packed_command = struct.pack('<Bd', self.__command_id_lookup_table['set_feed_rate'], feed_rate)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    set_forcely_set_arrived_status_to_true : set arrived state to true forcely
    1. argument
        
    2. return    
        result : (0 : success, -1 : failed to set)
    ''' 
    def set_forcely_set_arrived_status_to_true(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['forcely_set_arrived_status_to_true'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    ============================================================================================
    3. Servo drive setting
    ============================================================================================
    '''

    '''
    set_servo_on_off_state : set servo on/off state
    1. argument
        state : servo on/off state
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''       
    def set_servo_on_off_state(self, state:bool):
        packed_command = struct.pack('<B?', self.__command_id_lookup_table['set_servo_on_off_state'], state)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
    
    '''
    set_all_servo_to_quickstop : set all servo to quick stop mode (and make them servo off)
    1. argument
        
    2. return    
        result : (0 : success, -1 : failed to set)
    '''    
    def set_all_servo_to_quickstop(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['set_all_servo_to_quickstop'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    
        
    '''
    ============================================================================================
    4. Robot data
    ============================================================================================
    '''        
    
    
    '''
    get_actual_joint_position : get actual joint poistion list (j1 ~ j7)
    1. argument
        
    2. return    
        actual_joint_position : current actual joint position value list
    '''    
    def get_actual_joint_position(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_actual_joint_position'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("<7d", packed_response)
        joint_position_list = unpacked_response
        
        if ("MM_DEG_G" == self.__process_unit):
            joint_position_list = [math.degrees(joint_position_list[i]) for i in range(len(joint_position_list))]
            
        return joint_position_list


    '''
    get_actual_joint_velocity : get actual joint velocity list (j1 ~ j7)
    1. argument
        
    2. return    
        actual_joint_velocity : current actual joint velocity value list
    '''           
    def get_actual_joint_velocity(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_actual_joint_velocity'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("<7d", packed_response)
        joint_speeds_list = unpacked_response[0]     
        
        if ("MM_DEG_G" == self.__process_unit):
            joint_speed_list = [math.degrees(joint_speeds_list[i]) for i in range(len(joint_speeds_list))]

        return joint_speed_list
    
    
    '''
    get_actual_task_pose : get actual tcp pose (position, orientation)
    1. argument
        
    2. return    
        actual_task_pose : current actual tcp pose
    '''                      
    def get_actual_task_pose(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_actual_task_pose'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("6d", packed_response)
        position = unpacked_response[0:3]
        orientation = unpacked_response[3:6]
        tcp_pose = Pose(position, orientation)
        
        if ("MM_DEG_G" == self.__process_unit):
            tcp_pose = to_millimeter_degree(tcp_pose)
        
        return tcp_pose
        
        
    '''
    get_actual_task_velocity : get actual tcp velocity (translation, angular)
    1. argument
        
    2. return    
        actual_task_velocity : current actual tcp velocity represented with Pose structure (position, orientation)
    '''          
    def get_actual_task_velocity(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_actual_task_velocity'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("6d", packed_response)
        translation_speed = unpacked_response[0:3]
        angluar_speed = unpacked_response[3:6]
        tcp_speed = Pose(translation_speed, angluar_speed)
        
        if ("MM_DEG_G" == self.__process_unit):
            tcp_speed = to_millimeter_degree(tcp_speed)
        
        return tcp_speed


    '''
    get_target_joint_position : get actual joint poistion list (j1 ~ j7)
    1. argument
        
    2. return    
        target_joint_position : current target joint position value list
    '''         
    def get_target_joint_position(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_target_joint_position'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("<7d", packed_response)
        joint_position_list = unpacked_response
        
        if ("MM_DEG_G" == self.__process_unit):
            joint_position_list = [math.degrees(joint_position_list[i]) for i in range(len(joint_position_list))]
            
        return joint_position_list


    '''
    get_target_joint_velocity : get target joint velocity list (j1 ~ j7)
    1. argument
        
    2. return    
        target_joint_velocity : current target joint velocity value list
    '''              
    def get_target_joint_velocity(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_target_joint_velocity'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("<7d", packed_response)
        joint_speeds_list = unpacked_response 
        
        if ("MM_DEG_G" == self.__process_unit):
            joint_speeds_list = [math.degrees(joint_speeds_list[i]) for i in range(len(joint_speeds_list))]

        return joint_speeds_list


    '''
    get_target_task_pose : get target tcp pose (position, orientation)
    1. argument
        
    2. return    
        target_task_pose : current target tcp pose
    '''              
    def get_target_task_pose(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_target_task_pose'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("6d", packed_response)
        position = unpacked_response[0][0:3]
        orientation = unpacked_response[0][3:6]
        tcp_pose = Pose(position, orientation)
        
        if ("MM_DEG_G" == self.__process_unit):
            tcp_pose = to_millimeter_degree(tcp_pose)
        
        return tcp_pose


    '''
    get_target_task_velocity : get target tcp velocity (translation, angular)
    1. argument
        
    2. return    
        target_task_velocity : current target tcp velocity represented with Pose structure (position, orientation)
    '''                
    def get_target_task_velocity(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_target_task_velocity'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack("6d", packed_response)
        translation_speed = unpacked_response[0][0:3]
        angluar_speed = unpacked_response[0][3:6]
        tcp_speed = Pose(translation_speed, angluar_speed)
        
        if ("MM_DEG_G" == self.__process_unit):
            tcp_speed = to_millimeter_degree(tcp_speed)
        
        return tcp_speed


    ''' Not implemented yet'''           
    def get_joint_torque(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_joint_torque'])
        #packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        
        
    ''' Not implemented yet'''           
    def get_joint_temperature(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_joint_temperature'])
        #packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        
        
    ''' Not implemented yet'''           
    def get_task_force(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_task_force'])
        #packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        

    '''
    get_current_feed_rate : get current system feed rate
    1. argument
        
    2. return    
        feed_rate : feed rate
    '''         
    def get_current_feed_rate(self):
        packed_command = struct.packs('<B', self.__command_id_lookup_table['get_current_feed_rate'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<d', packed_response)
        feed_rate = unpacked_response[0]
        return feed_rate


    '''
    get_current_is_finished_state : get current "is_finished" status
    1. argument
        
    2. return    
        is_finished_state : feed rate
    '''                    
    def get_current_is_finished_state(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_current_is_finished_state'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        is_finished_state = unpacked_response[0]
        return is_finished_state


    '''
    get_current_tool_setting : get current applied tool setting
    1. argument
        
    2. return    
        tool_setting : tool setting information
    '''         
    def get_current_tool_setting(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_current_tool_setting'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<3d3dd', packed_response)
        tool_position = unpacked_response[0]
        tool_center_of_mass = unpacked_response[1]
        tool_weight = unpacked_response[2]
        tool_setting = ToolOption(tool_position, tool_center_of_mass, tool_weight)
        
        if ('MM_DEG_G' == self.__process_unit):
            tool_setting = to_millimeter_degree(tool_setting)
            
        return tool_setting


    '''
    get_current_user_joint_limit : get current user limit setting
    1. argument
        joint_index : joint index
        
    2. return    
        nagative_joint_limit : nagative limit
        positive_joint_limit : positive limit
    '''            
    def get_current_user_joint_limit(self, joint_index:int):
        packed_command = struct.pack('<Bi', self.__command_id_lookup_table['get_current_user_joint_limit'], joint_index)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<dd', packed_response)
        nagative_joint_limit = unpacked_response[0]
        positive_joint_limit = unpacked_response[1]
        
        if ('MM_DEG_G' == self.__process_unit):
            nagative_joint_limit = math.degrees(nagative_joint_limit)
            positive_joint_limit = math.degrees(positive_joint_limit)
        
        return (nagative_joint_limit, positive_joint_limit)


    '''
    get_current_user_joint_limit_on_off_state : get current activation status of user limit
    1. argument
        
    2. return    
        user_limit_of_off_state : user limit activation status
    '''                   
    def get_current_user_joint_limit_on_off_state(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_current_user_joint_limit_on_off_state'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_data = struct.unpack('b', packed_response)
        joint_limit_on_off_state = unpacked_data[0]
        return joint_limit_on_off_state


    '''
    get_current_default_joint_limit : get current default limit setting (of motion control algorithm)
    1. argument
        joint_index : joint index
        
    2. return    
        nagative_joint_limit : nagative limit
        positive_joint_limit : positive limit
    '''            
    def get_current_default_joint_limit(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_current_default_joint_limit'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<dd', packed_response)
        nagative_joint_limit = unpacked_response[0]
        positive_joint_limit = unpacked_response[1]
        
        if ('MM_DEG_G' == self.__process_unit):
            nagative_joint_limit = math.degrees(nagative_joint_limit)
            positive_joint_limit = math.degrees(positive_joint_limit)
        
        return (nagative_joint_limit, positive_joint_limit)


    '''
    get_current_actual_joint_limit : get current actual limit setting by considering the both user and default setting
    1. argument
        joint_index : joint index
        
    2. return    
        nagative_joint_limit : nagative limit
        positive_joint_limit : positive limit
    '''           
    def get_current_actual_joint_limit(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_current_actual_joint_limit'])
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<dd', packed_response)
        nagative_joint_limit = unpacked_response[0]
        positive_joint_limit = unpacked_response[1]
        
        if ('MM_DEG_G' == self.__process_unit):
            nagative_joint_limit = math.degrees(nagative_joint_limit)
            positive_joint_limit = math.degrees(positive_joint_limit)
        
        return (nagative_joint_limit, positive_joint_limit)



    '''
    ============================================================================================
    5. Bank control
    ============================================================================================
    '''
    
    '''
    get_tool_bank : get tool option setting from the tool option bank
    1. argument
        tool_bank_index : tool bank index
        
    2. return    
        tool_bank_index : tool setting
    '''  
    def get_tool_bank(self, ToolOption_index:int):
        packed_command = struct.pack('<Bi', self.__command_id_lookup_table['get_tool_bank'], ToolOption_index)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        response_result = struct.unpack('<b', packed_response[0:1])[0]
        if (response_result == 0):
            unpacked_response = struct.unpack('<3d3dd', packed_response[1:])
            position = unpacked_response[0:3]
            center_of_mass = unpacked_response[3:6]
            weight = unpacked_response[6]
            tool_option = ToolOption(position, center_of_mass, weight)
            if ('MM_DEG_G' == self.__process_unit):
                tool_option = to_millimeter_degree(tool_option)
            return tool_option
        else:
            return None
        

    '''
    get_pose_bank : get pose data from the pose bank
    1. argument
        pose_index : pose bank index
        
    2. return    
        pose : pose data
    '''         
    def get_pose_bank(self, pose_index:int):
        packed_command = struct.pack('<Bi', self.__command_id_lookup_table['get_pose_bank'], pose_index)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        response_result = struct.unpack('<b', packed_response[0:1])[0]
        if (response_result == 0):
            unpacked_response = struct.unpack('<3d3d', packed_response[1:])
            position = unpacked_response[0:3]
            orientation = unpacked_response[3:6]
            pose = Pose(position, orientation)
            if ('MM_DEG_G' == self.__process_unit):
                pose = to_millimeter_degree(pose)
            return pose
        else:
            return None


    '''
    execute_motion_bank : execute motion data from the motion bank
    1. argument
        motion_index : motion bank index
        blocking : blocking option (True : the function is blocked until finished, False : the function is not blocked and execute it concurrently)
        
    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''          
    def execute_motion_bank(self, motion_index:int, blocking=True):
        packed_command = struct.pack('<Bi?', self.__command_id_lookup_table['execute_motion_bank'], motion_index, blocking)
        packed_response = self.__transmit_command_packet('COMMAND',packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    stop_executing_motion_bank : stop all currently executing motion datas
    1. argument
        
    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''      
    def stop_executing_motion_bank(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['stop_executing_motion_bank'])
        packed_response = self.__transmit_command_packet('COMMAND',packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    


    '''
    ============================================================================================
    6. IO control
    ============================================================================================
    '''    
    
    __registered_co_event_rising_callback_list = {}
    __registered_co_event_falling_callback_list = {}


    '''
    set_digital_output : set do value of the default io module
    1. argument
        index : io port number (start from 0)
        value : value
        timeout : triggering time (0 : is infinite)
            
    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''       
    def set_digital_output(self, index:int, value:bool, timeout:float=0):
        if (timeout):
            packed_command = struct.pack('<Bbb?H', self.__command_id_lookup_table['set_digital_output'], 
                                    index,
                                    value,
                                    True,
                                    timeout) 
        else:
            packed_command = struct.pack('<Bbb?', self.__command_id_lookup_table['set_digital_output'], 
                                    index, 
                                    value,
                                    False)
            
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]


    '''
    get_digital_input : get di value
    1. argument
        index : io port number (start from 0)
            
    2. return    
        result : (0 : success, -1 : failed to read)
        value : value
    '''   
    def get_digital_input(self, index):
        packed_command = struct.pack('<Bb', self.__command_id_lookup_table['get_digital_input'], 
                                index)        
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response[0:1])
        res = unpacked_response[0]
        if (res == 0):
            data = struct.unpack('<?', packed_response[1:2])[0]
            return data            
        else:
            return None
        
        
    '''
    set_all_digital_output_as_number : set all do values of the default io module by using binary number
    1. argument
        value : value (ex. 146 = 0b10010010)
            
    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
    '''                     
    def set_all_digital_output_as_number(self, value:int):
        packed_command = struct.pack('<Bi', self.__command_id_lookup_table['set_all_digital_output_as_number'], value)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]
    

    '''
    get_all_digital_input_as_number : get all di values of the default io module as binary number
    1. argument
            
    2. return    
        result : (0 : success, -1 : execution failed, -2 : comamnd denided because of some higher priority)
        value : value
    '''     
    def get_all_digital_input_as_number(self):
        packed_command = struct.pack('<B', self.__command_id_lookup_table['get_all_digital_input_as_number'])        
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response[0:1])
        res = unpacked_response[0]
        if (res == 0):
            data_list = struct.unpack('<16b', packed_response[1:])
            return data_list            
        else:
            return None


    '''
    register_digital_input_event_callback_function : register callback function that triggered when di event is occured
    1. argument
        index : io port number
        trigger_type : edge type (True(1) : rising edge, False(1) : falling edge)
        callback : name of callback function
            
    2. return    
        result : (0 : success, -1 : failed to register)
    '''     
    def register_io_digital_input_event_callback_function(self, index:int, trigger_type:bool, callback):
        packed_command = struct.pack('<Bbb', self.__command_id_lookup_table['register_io_digital_input_event_callback_function'], index, trigger_type)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (trigger_type == 1):
                callback_list = self.__registered_di_event_rising_callback_list.get(index)
                if (not callback_list):
                    callback_list = []
                    self.__registered_di_event_rising_callback_list[index] = callback_list
                callback_list.append(callback)
            elif (trigger_type == 0):
                callback_list = self.__registered_di_event_falling_callback_list.get(index)
                if (not callback_list):
                    callback_list = []
                    self.__registered_di_event_falling_callback_list[index] = callback_list
                callback_list.append(callback)
        return res
                
    __registered_di_event_rising_callback_list = {}
    __registered_di_event_falling_callback_list = {}



    '''
    ============================================================================================
    6. Accessory control
    ============================================================================================
    '''
    def process_transaction_with_accessory(self, accessory_id, json_object):
        packed_command = struct.pack('<BB', self.__command_id_lookup_table['process_transaction_with_accessory'], accessory_id)        
        json_object_string = json.dumps(json_object).encode('utf-8')
        json_object_string_length = len(json_object_string)
        packed_command += struct.pack('<i%ds'%json_object_string_length, json_object_string_length, json_object_string)        
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        
        unpacked_data = struct.unpack('<i', packed_response[0:4])
        result_json_string_length = unpacked_data[0]
        result_json_string = struct.unpack('%ds'%result_json_string_length, packed_response[4:])[0]
        result_json_object = json.loads(result_json_string.decode('utf-8'))    
        
        return result_json_object

    
    
    __modbus_data_type_packing_code_lookup_table = {
        0:'H',
        1:'i',
        2:'f',
    }
    
    def get_modbus_register_value(self, memory_type:int, address:int, data_type:int, length:int):
        packed_command = struct.pack('<Bbibi', self.__command_id_lookup_table['get_modbus_register_value'], 
                                     memory_type, 
                                     address, 
                                     data_type, 
                                     length)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<bi', packed_response[0:5])
        res = unpacked_response[0]
        length = unpacked_response[1]
        if (res == 0):
            unpacking_code = '<%d' + self.__modbus_data_type_packing_code_lookup_table[data_type]
            value_list = struct.unpack(unpacking_code%length, packed_response[5:])
            if (memory_type == 0):
                value_list = [bool(data) for data in value_list]
            return value_list                                       
        else:
            return None
            
    # Set modbus register value
    # - param memory_type : 0(coil_output), 1(digital input), 3(input register), 4(holding register)
    # - param address : address of each memory type
    # - param data_type : 0(2bytes word), 1(4bytes integer), 2(4bytes float)
    # - param data_list : list of data (must be list)
    # - return : 0(success) / -1(failed)
    def set_modbus_register_value(self, memory_type:int, address:int, data_type:int, data_list:list):
        packed_command = struct.pack('<Bbib', self.__command_id_lookup_table['set_modbus_register_value'],
                                     memory_type,
                                     address, 
                                     data_type)
        length = len(data_list)
        packing_code = '<i%d' + self.__modbus_data_type_packing_code_lookup_table[data_type]
        packed_command += struct.pack(packing_code%length, length, *data_list)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        return unpacked_response[0]

    def register_modbus_co_event_callback_function(self, address, trigger_type, callback):
        packed_command = struct.pack('<Bib', self.__command_id_lookup_table['register_modbus_co_event_callback_function'], address, trigger_type)
        packed_response = self.__transmit_command_packet('COMMAND', packed_command)
        unpacked_response = struct.unpack('<b', packed_response)
        res = unpacked_response[0]
        if (res == 0):
            if (trigger_type == 1):
                callback_list = self.__registered_co_event_rising_callback_list.get(address)
                if (not callback_list):
                    callback_list = []
                    self.__registered_co_event_rising_callback_list[address] = callback_list
                callback_list.append(callback)
            elif (trigger_type == 0):
                callback_list = self.__registered_co_event_falling_callback_list.get(address)
                if (not callback_list):
                    callback_list = []
                    self.__registered_co_event_falling_callback_list[address] = callback_list
                callback_list.append(callback)
        return res                
                
                    
    '''
    PRIVATE FUNCTIONS
    '''
    def __process_callback_co_event(self, args):
        unpacked_data = struct.unpack('<ib', args)
        address = unpacked_data[0]
        trigger_type = unpacked_data[1]
        
        if (trigger_type == 1):
            target_callback_list = self.__registered_co_event_rising_callback_list
        elif (trigger_type == 0):
            target_callback_list = self.__registered_co_event_falling_callback_list
            
        callback_list = target_callback_list.get(address)
        if (callback_list):
            for callback in callback_list:
                t = threading.Thread(target=callback)
                t.daemon = True
                t.start()


    def __process_callback_di_event(self, args):
        unpacked_data = struct.unpack('<ib', args)
        address = unpacked_data[0]
        trigger_type = unpacked_data[1]
        
        if (trigger_type == 1):
            target_callback_list = self.__registered_di_event_rising_callback_list
        elif (trigger_type == 0):
            target_callback_list = self.__registered_di_event_falling_callback_list
            
        callback_list = target_callback_list.get(address)
        if (callback_list):
            for callback in callback_list:
                t = threading.Thread(target=callback)
                t.daemon = True
                t.start()                    
                

                
    __event_id_dispatch_lookup_table = {
        223: __process_callback_co_event,
        235: __process_callback_di_event,
    }
    
    def __event_process(self, event_socket):
        self.__logger.debug("event_process thread is started for %s", self.__class__.__name__)
        try:
            while True:
                buf = self.__receive_data(event_socket)
                if (buf):
                    command = buf[0]
                    callback = self.__event_id_dispatch_lookup_table.get(command)
                    if (callback):
                        callback(self, buf[1:])
                else:
                    # self.__logger.info("client is disconnected from mrscsript binary protocol command server : %s", addr)
                    self.disconnect()
                    break            
        except Exception as e:
            self.__logger.warning("event faced exception : %s", e)
            self.disconnect()
               
    def __transmit_command_packet(self, server_name, buf):
        res = None
        server = self.__server_lookup_table[server_name]        
        if(server['connection'] == True):
            server['semaphore'].acquire()
            try:
                self.__send_data(server['socket'], buf)
                response_buf = self.__receive_data(server['socket'])
            except Exception as e:
                server['connection'] = False
                return None
            finally:
                server['semaphore'].release()
            return response_buf
        else:
            self.__logger.warning("%s is not connected", server['name'])
            return None

    def __send_data(self, socket, buf):
        transmit_buffer = bytearray()
        transmit_buffer.extend(b'MR')
        transmit_buffer.extend(struct.pack('<i', len(buf)))
        transmit_buffer.extend(buf)
        try:
            socket.send(transmit_buffer)
        except Exception:
            socket.close()
            
    def __receive_data(self, socket):
        try:
            buf = socket.recv(2)
            if (buf == b'MR'):    
                buf = socket.recv(4)
                read_len = struct.unpack('<i', buf)[0]
                receive_buffer = socket.recv(read_len)
                return receive_buffer
            else:
                return None
        except Exception:
            socket.close()
            return None

    
if __name__ == '__main__':
    p1 = Pose(Position(1,2,3), Orientation(5,6,7))
    p2 = Pose(Position(2,3,4), Orientation(11,22,33))
    p3 = Pose(Position(3,4,5), Orientation(111, 222, 333))

    robot1 = PalRobot('127.0.0.1')
    robot1.connect()
    
    robot1.get_actual_joint_position()
    
    while(True):
        time.sleep(3600)

    # robot1.stop()
    # robot1.pause()
    # robot1.resume()
    # robot1.move_joint_with_q([1,2,3,4,5,6])
    # robot1.move_joint(p1)
    # robot1.move_linear(p1, waypoint_list = [WayPoint(p2, 1.0), WayPoint(p3, 3.0)])
    # robot1.move_circle(p1, p2)
    # robot1.is_finished()

    # robot1.set_direct_teaching_on_off_state(True)
    # robot1.set_tool_information(Position(1,2,3), Position(4,5,6), 1.3)
    # robot1.set_collision_sensitivity(3.14)
    # robot1.set_collision_detection_mode(3)
    # robot1.set_default_joint_value(1, 6.28)
    # robot1.set_user_joint_limit(3, -3.14, 3.14)
    # robot1.set_user_joint_limit_on_off_state(True)
    # robot1.set_ignore_orientation_for_ik_on_off_state(True)
    # robot1.set_feed_rate(0.5)
    # robot1.set_forcely_set_arrived_status_to_true()

    # robot1.set_servo_on_off_state(True)
    # robot1.reset_servo_error(6)
    # robot1.reset_servo_absolute_encoder(5)
    # robot1.set_servo_encoder_origin(4, 123456)
    # robot1.set_all_servo_to_quickstop()

    # robot1.get_actual_joint_position()
    # robot1.get_actual_joint_velocity()
    # robot1.get_actual_task_pose()
    # robot1.get_actual_task_velocity()
    # robot1.get_target_joint_position()
    # robot1.get_target_joint_velocity()
    # robot1.get_target_task_pose()
    # robot1.get_target_task_velocity()
    # robot1.get_joint_torque()
    # robot1.get_joint_temperature()
    # robot1.get_task_force()
    # robot1.solve_forward_kinematics()
    # robot1.solve_inverse_kinematics()
    # robot1.get_current_feed_rate()
    # robot1.get_current_is_finished_state()
    # robot1.get_current_tool_setting()
    # robot1.get_current_user_joint_limit()
    # robot1.get_current_user_joint_limit_on_off_state()
    # robot1.get_current_default_joint_limit()
    # robot1.get_current_actual_joint_limit()
    # robot1.get_servo_status()
    # robot1.get_servo_coe_pds()
    # robot1.get_servo_coe_mode_of_operation()
    # robot1.get_servo_error()

    # res = robot1.save_ToolOption_bank(1, ToolOption(Position(7,7,7), Position(7,7,7), 3.14))
    # print(res)
    # print('\n')
    
    # res = robot1.get_tool_bank(1)
    # print(res.position)
    # print(res.center_of_mass)
    # print(res.weight)
    # print('\n')
    
    # res = robot1.save_pose_bank(1, Pose(Position(1,2,3), Orientation(11, 22, 33)))
    # print(res)
    # print('\n')
    
    
    # res = robot1.get_tool_bank(1)
    # print(res)
    # print('\n')
    
    # res = robot1.save_motion_bank(1, 'import math')
    # print(res)
    # print('\n')
    
    # res = robot1.load_motion_bank(1)
    # print(res)
    # print('\n')
    
    # res = robot1.execute_motion_bank(1)
    # print(res)
    # print('\n')
    
    p1 = Pose(Position(1,2,3), Orientation(5,6,7))
    q = [360,360,360,360,360,360]
    robot1.move_joint_with_q(q)

    p = to_meter_radian(Position(1000,2000,3000))
    print(p)
