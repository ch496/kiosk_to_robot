class Error_detection_check_list:

    Error_detection_check_code = ["Error_code"]

    Error_detection_check_C01_list = ["CO1_001",  # 컵 디스펜서 오른쪽 (DO_06 Error)
                                      "CO1_002",  # 컵 디스펜서 왼쪽   (DO_07 Error)
                                      "CO1_003",  # 커피머신 에소프레소 (DO_00 Error)
                                      "CO1_004",  # 커피머신 온수      (DO_01 Error)
                                      "CO1_005",  # 커피머신 카페라떼   (DO_02 Error)
                                      "CO1_006",  # 커피머신 아이스티   (DO_03 Error)
                                      "CO1_007",  # 커피머신 핫초코     (DO_04 Error)
                                      "CO1_008"]  # 제빙기             (DO_05 Error)

    Error_detection_check_C02_list = ["CO2_001",  # 컵 디스펜서 오른쪽 컵 부족
                                      "CO2_002",  # 컵 디스펜서 왼쪽   컵 부족
                                      "CO2_003",  # 커피 원두 부족
                                      "CO2_004",  # 초코 원두 부족
                                      "CO2_005",  # 우유 부족
                                      "CO2_006",  # 아이스티 원두 부족
                                      "CO2_007"]  # 제빙기 얼음 부족

    Error_detection_check_C03_list = ["CO3_001",  # 주문번호 Error (품목에 없는 주문번호)
                                      "CO3_002",  # Position Error (저되 어있는 position 이외의 번호 지정)
                                      "CO3_003",  # 왼쪽 회전판 테이블 Error (주문이 들어 왔지만 회전판 테이블에 정보가 없는 경우)
                                      "CO3_004"]  # 오른쪽 회전판 테이블 Error (주문이 들어 왔지만 회전판 테이블에 정보가 없는 경우)