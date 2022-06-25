cup_left_waypoint = [
    WayPoint(pose=get_pose_bank(index=1))
]

cup_left = get_pose_bank(index=1)
cup_left_in = get_pose_bank(index=6)

vel = 1000
acc = 1000
# ------------------------------ 목차 -------------------------------
#
# ------- 커피 신호 -----------
# 0번 : 아메리카노 (액기스)      1번 : 온수 (최대 출력시간 약17초)
# 2번 : 카페라떼(액기스)         3번 : 카페모카(액기스)
# 4번 : 핫초코 (얘도 액기스였나?)

# ------- 그외 다른 신호 ------

# 5번 : 제빙기 얼음+물(설정신호 물 3.1초, 얼음 3.5초)
# 7번 : 왼쪽 컵 신호             6번 : 오른쪽 컵 신호

#  ------------------------- 로봇 동작 -------------------

#  ------------------------- 커피 신호 입력 및 컵 디스펜서(왼쪽) 이동 -------------
move_linear(destination_pose=cup_left_in, velocity=vel, acceleration=acc, waypoint_list=cup_left_waypoint)
# ---- 임시 오프_01_25
set_digital_output(index=7, value=True)
sleep(0.5)
set_digital_output(index=7, value=False)
sleep(2)
# ---- 임시 오프_01_25

move_linear(destination_pose=cup_left, velocity=vel, acceleration=acc)
