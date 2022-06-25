home_waypoint = [
    WayPoint(pose=get_pose_bank(index=0))
]

home = get_pose_bank(index=0)

cup_left_waypoint = [
    WayPoint(pose=get_pose_bank(index=1))
]

cup_left = get_pose_bank(index=1)
cup_left_in = get_pose_bank(index=6)

cup_right = get_pose_bank(index=2)

coffe_waypoint = [
    WayPoint(pose=get_pose_bank(index=3))
]

coffe = get_pose_bank(index=3)
coffe_in = get_pose_bank(index=5)
ice_waypoint = [
    WayPoint(pose=get_pose_bank(index=4)),
    WayPoint(pose=get_pose_bank(index=0))
]
ice_in_waypoint = [
    WayPoint(pose=get_pose_bank(index=4))
]

ice = get_pose_bank(index=4)
ice_in = get_pose_bank(index=7)

left_plate = get_pose_bank(index=10)

left_plate_waypoint = [
    WayPoint(pose=get_pose_bank(index=11)), WayPoint(pose=get_pose_bank(index=12)),
    WayPoint(pose=get_pose_bank(index=3))
]

cup_left_waypoint = [
    WayPoint(pose=get_pose_bank(index=1))
]

cup_left = get_pose_bank(index=1)
cup_left_in = get_pose_bank(index=6)

right_plate = get_pose_bank(index=13)
right_plate_down = get_pose_bank(index=14)

right_plate_waypoint = [
    WayPoint(pose=get_pose_bank(index=4))
]

right_plate_gohome_waypoint = [
    WayPoint(pose=get_pose_bank(index=15)), WayPoint(pose=get_pose_bank(index=4))
]

left_plate = get_pose_bank(index=10)
left_plate_down = get_pose_bank(index=11)

left_plate_waypoint = [
    WayPoint(pose=get_pose_bank(index=12)), WayPoint(pose=get_pose_bank(index=3))
]

vel = 1000
acc = 1000
while (True):
    # --------------------------------------------------왼쪽

    move_linear(destination_pose=cup_left_in, velocity=vel, acceleration=acc, waypoint_list=cup_left_waypoint)

    move_linear(destination_pose=cup_left, velocity=vel, acceleration=acc)

    move_linear(destination_pose=ice_in, velocity=vel, acceleration=acc, waypoint_list=ice_in_waypoint)

    move_linear(destination_pose=coffe, velocity=vel, acceleration=acc, waypoint_list=ice_waypoint)

    move_linear(destination_pose=coffe_in, velocity=vel, acceleration=acc)

    move_linear(destination_pose=coffe, velocity=300, acceleration=900)

    move_linear(destination_pose=left_plate, velocity=300, acceleration=900)
    move_linear(destination_pose=left_plate_down, velocity=300, acceleration=900)

    move_linear(destination_pose=home, velocity=300, acceleration=200, waypoint_list=left_plate_waypoint)

    #  -----------------오른쪽

    move_linear(destination_pose=cup_left_in, velocity=vel, acceleration=acc, waypoint_list=cup_left_waypoint)

    move_linear(destination_pose=cup_left, velocity=vel, acceleration=acc)

    move_linear(destination_pose=ice_in, velocity=vel, acceleration=acc, waypoint_list=ice_in_waypoint)

    move_linear(destination_pose=coffe, velocity=vel, acceleration=acc, waypoint_list=ice_waypoint)

    move_linear(destination_pose=coffe_in, velocity=vel, acceleration=acc)

    move_linear(destination_pose=coffe, velocity=300, acceleration=900)

    move_linear(destination_pose=right_plate, velocity=300, acceleration=900, waypoint_list=right_plate_waypoint)
    move_linear(destination_pose=right_plate_down, velocity=300, acceleration=900)
    move_linear(destination_pose=home, velocity=300, acceleration=400, waypoint_list=right_plate_gohome_waypoint)






