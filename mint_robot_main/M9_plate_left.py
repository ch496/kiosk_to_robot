home = get_pose_bank(index = 0)



left_plate = get_pose_bank(index = 10)
left_plate_down = get_pose_bank(index = 11)


left_plate_waypoint = [
                      WayPoint(pose = get_pose_bank(index = 12)),WayPoint(pose = get_pose_bank(index = 3))
                      ]


#  -----------------커피 선반 도달 및 복귀 (따로 작성필요 유무..)
move_linear(destination_pose = left_plate, velocity =300, acceleration = 900)
move_linear(destination_pose = left_plate_down, velocity = 300, acceleration = 900)

move_linear(destination_pose = home, velocity = 300, acceleration = 200, waypoint_list = left_plate_waypoint)

