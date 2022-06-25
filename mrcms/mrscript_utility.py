'''
Copyright (C) MINTROBOT Co., Ltd. - All Rights Reserved

'''

import math
import numpy as np

class Position(list):
    def __init__(self, x = 0, y = 0, z = 0):
        self.extend(x) if type(x)==list else self.extend([x, y, z])
    
    @property
    def x(self):
        return self[0]
    
    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, y):
        self[1] = y

    @property
    def z(self):
        return self[2]
    
    @z.setter
    def z(self, z):
        self[2] = z

    
class Orientation(list):
    def __init__(self, rx = 0, ry = 0, rz = 0):
        self.extend(rx) if type(rx)==list else self.extend([rx, ry, rz])
        
    @property
    def rx(self):
        return self[0]
    
    @rx.setter
    def rx(self, rx):
        self[0] = rx
        
    @property
    def ry(self):
        return self[1]
    
    @ry.setter
    def ry(self, ry):
        self[1] = ry

    @property
    def rz(self):
        return self[2]
    
    @rz.setter
    def rz(self, rz):
        self[2] = rz
  
  
class Pose(list):
    def __init__(self, position:Position = Position(), orientation:Orientation = Orientation()):
        self.extend(position)
        self.extend(orientation)
   
    @property
    def position(self):
        return Position(self[0:3])
    
    @property
    def orientation(self):
        return Orientation(self[3:6])


class WayPoint():
    def __init__(self, pose:Pose, radius:float = 0):
        self.pose = pose
        self.radius = radius


class ToolOption():
    def __init__(self, position:Position = Position(), center_of_mass:Position = Position(), mass:float = 0):
        self.position = position
        self.center_of_mass = center_of_mass
        self.mass = mass


class Palletizer2D():
    def __init__(self, area, number_of_row, number_of_column, direction='raw'):       
        self.list_p1_to_p2 = np.linspace((area[0].x, area[0].y), (area[1].x, area[1].y), number_of_row).tolist()
        self.list_p1_to_p3 = np.linspace((area[0].x, area[0].y), (area[2].x, area[2].y), number_of_row).tolist()
        self.list_p2_to_p4 = np.linspace((area[1].x, area[1].y), (area[3].x, area[3].y), number_of_row).tolist()
        self.list_p3_to_p4 = np.linspace((area[2].x, area[2].y), (area[3].x, area[3].y), number_of_row).tolist()

        self.matrix = []
        if (direction =='raw'):
            for row_index in range(number_of_row):
                start = self.list_p1_to_p3[row_index]
                end = self.list_p2_to_p4[row_index]
                self.matrix.append(np.linspace(start, end, number_of_row).tolist())
                
            self.list_flattern = []
            for item in self.matrix:
                self.list_flattern = self.list_flattern + item
                
        elif (direction == 'column'):
            for row_index in range(number_of_row):
                start = self.list_p1_to_p2[row_index]
                end = self.list_p3_to_p4[row_index]
                self.matrix.append(np.linspace(start, end, number_of_row).tolist())
                
            self.list_flattern = []
            for item in self.matrix:
                self.list_flattern = self.list_flattern + item
            
    def get_position_by_index(self, index):
        return self.list_flattern[index]


def offset_pose(source_pose:Pose, x=None, y=None, z=None, rx=None, ry=None, rz=None):
    offset_position = source_pose.position
    offset_orientation = source_pose.orientation
    if (x != None): offset_position.x += x
    if (y != None): offset_position.y += y
    if (z != None): offset_position.z += z
    if (rx != None): offset_orientation.rx += rx
    if (ry != None): offset_orientation.ry += ry
    if (rz != None): offset_orientation.rz += rz
    
    return Pose(position=offset_position, orientation=offset_orientation)
    

def blend_pose(source_pose:Pose, x=None, y=None, z=None, rx=None, ry=None, rz=None):
    blend_position = source_pose.position
    blend_orientation = source_pose.orientation
    if (x != None): blend_position.x = x
    if (y != None): blend_position.y = y
    if (z != None): blend_position.z = z
    if (rx != None): blend_orientation.rx = rx
    if (ry != None): blend_orientation.ry = ry
    if (rz != None): blend_orientation.rz = rz
    
    return Pose(position=blend_position, orientation=blend_orientation)
        

def tooloffset_pose(source_pose:Pose, offset_relative_pose:Pose):
    pass


def __to_meter_radian_position(position:Position):
    return Position(position[0] / 1000.0, position[1] / 1000.0, position[2] / 1000.0)


def __to_meter_radian_orientation(orientation:Orientation):
    return Orientation(math.radians(orientation[0]), math.radians(orientation[1]), math.radians(orientation[2]))
    
    
def __to_meter_radian_pose(pose:Pose):
    return Pose(__to_meter_radian_position(pose.position), __to_meter_radian_orientation(pose.orientation))


def __to_meter_radian_waypoint(waypoint:WayPoint):
    return WayPoint(__to_meter_radian_pose(Pose(waypoint.pose)), math.radians(waypoint.radius))
        
        
def __to_meter_radian_toolset(toolset:ToolOption):
    return ToolOption(__to_meter_radian_position(toolset.position), __to_meter_radian_position(toolset.center_of_mass), toolset.weight)

def __to_millimeter_degree_position(position:Position):
    return Position(position[0] * 1000.0, position[1] * 1000.0, position[2] * 1000.0)


def __to_millimeter_degree_orientation(orientation:Orientation):
    return Orientation(math.degrees(orientation[0]), math.degrees(orientation[1]), math.degrees(orientation[2]))


def __to_millimeter_degree_pose(pose:Pose):
    return Pose(__to_millimeter_degree_position(pose.position), __to_millimeter_degree_orientation(pose.orientation))


def __to_millimeter_degree_waypoint(waypoint:WayPoint):
    return WayPoint(__to_millimeter_degree_pose(waypoint.pose), math.degrees(waypoint.radius))

 
def __to_millimeter_degree_toolset(tool_option:ToolOption):
    return ToolOption(__to_millimeter_degree_position(tool_option.position), __to_millimeter_degree_position(tool_option.center_of_mass), tool_option.mass*0.001)


__toMeterRadian_dispatch_lookup_table = {Position: __to_meter_radian_position,
                                         Orientation: __to_meter_radian_orientation,
                                         Pose: __to_meter_radian_pose,
                                         WayPoint: __to_meter_radian_waypoint,
                                         ToolOption: __to_meter_radian_toolset,
                                         }


__toMillimeterDegree_dispatch_lookup_table = {Position: __to_millimeter_degree_position,
                                              Orientation: __to_millimeter_degree_orientation,
                                              Pose: __to_millimeter_degree_pose,
                                              WayPoint: __to_millimeter_degree_waypoint,
                                              ToolOption: __to_millimeter_degree_toolset
                                              }


def to_meter_radian(target):
    return __toMeterRadian_dispatch_lookup_table[target.__class__](target)


def to_millimeter_degree(target):
    return __toMillimeterDegree_dispatch_lookup_table[target.__class__](target)



    

