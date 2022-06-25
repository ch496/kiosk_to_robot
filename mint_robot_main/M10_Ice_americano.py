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

# move_joint_with_q(destination_q = JointVector(j1 = 9.588 , j2 = - 5 , j3 = -98.788, j4 = -90.800), q_velocity = 800, q_acceleration = 400) # 초기모션

vel = 1000
acc = 1000
# ------------------------------ 목차 -------------------------------
#
# ------- 커피 신호 -----------
# 0번 : 아메리카노 (에소프레소)      1번 : 온수 (최대 출력시간 약17초)
# 2번 : 카페라떼(에소프레소 + 파우더)         3번 : 카페모카(파우더)
# 4번 : 핫초코 (파우더 + 파우더 )

# ------- 그외 다른 신호 ------

# 5번 : 제빙기 얼음+물(설정신호 물 3.1초, 얼음 3.5초)
# 7번 : 왼쪽 컵 신호             6번 : 오른쪽 컵 신호

#  ------------------------- 로봇 동작 -------------------

#  ------------------------- 커피 신호 입력 및 컵 디스펜서(왼쪽) 이동 -------------
# sleep(4)
set_digital_output(index=0, value=True)
sleep(0.5)
set_digital_output(index=0, value=False)

# -------------------------- 제빙기 도달 및 출력 --------------------------------
move_linear(destination_pose=ice_in, velocity=vel, acceleration=acc, waypoint_list=ice_in_waypoint)
sleep(0.5)
set_digital_output(index=5, value=True)
sleep(0.5)
set_digital_output(index=5, value=False)
sleep(3.5)

# ------------------------ 커피 대기 및 온수 출력 --------

move_linear(destination_pose=coffe, velocity=vel, acceleration=acc, waypoint_list=ice_waypoint)

move_linear(destination_pose=coffe_in, velocity=vel, acceleration=acc)
# 커피 딜레이 기입 시간 = 커피 출력 시간 - (컵 디스펜서딜레이 시간 + 아이스 디스펜서 딜레이시간 + 로봇 이동 시간)
sleep(25)

move_linear(destination_pose=coffe, velocity=300, acceleration=900)

