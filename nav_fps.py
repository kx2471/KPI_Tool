import dlt_parser  # dlt_parser.py 모듈을 가져옵니다.

def extract_fps_data(parsed_data):
    fps_values = []

    for entry in parsed_data:
        # entry의 길이에 따라 처리
        if len(entry) == 3:  # NAV_MAP_FPS인 경우
            marker_time, nav_value, numeric_value = entry
            if numeric_value:  # numeric_value가 있을 경우 추가
                fps_values.append((marker_time, nav_value, float(numeric_value)))
        elif len(entry) == 2:  # NAV_MAP_FPS가 아닌 경우
            marker_time, nav_value = entry
            fps_values.append((marker_time, nav_value))  # numeric_value는 없으므로 단순 추가

    return fps_values

def calculate_statistics(fps_values):
    cid_values = []
    ic_values = []

    for entry in fps_values:
        if len(entry) == 3:  # NAV_MAP_FPS인 경우
            marker_time, nav_value, numeric_value = entry
            if "NAV_MAP_FPS_CID" in nav_value:
                cid_values.append(numeric_value)
            elif "NAV_MAP_FPS_IC" in nav_value:
                ic_values.append(numeric_value)

    # 평균과 최솟값 계산
    cid_avg = sum(cid_values) / len(cid_values) if cid_values else None
    cid_min = min(cid_values) if cid_values else None
    ic_avg = sum(ic_values) / len(ic_values) if ic_values else None
    ic_min = min(ic_values) if ic_values else None

    return {
        "NAV_MAP_FPS_CID": {"average": cid_avg, "min": cid_min},
        "NAV_MAP_FPS_IC": {"average": ic_avg, "min": ic_min}
    }

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    fps_values = extract_fps_data(parsed_data)  # FPS 값 추출
    

    statistics = calculate_statistics(fps_values)  # 통계 계산
    print("NAV_MAP_FPS_CID 통계:", statistics["NAV_MAP_FPS_CID"])
    print("NAV_MAP_FPS_IC 통계:", statistics["NAV_MAP_FPS_IC"])
