import dlt_parser  # dlt_parser.py 모듈을 가져옵니다.

def format_time_string(marker_time):
    """Marker Time을 초 단위의 문자열로 변환하여 반환합니다."""
    try:
        seconds, nanoseconds = marker_time.split('s', 1)  # 첫 번째 's'만 기준으로 분리
        seconds = int(seconds)  # 초 부분은 정수형으로 변환
        nanoseconds = int(nanoseconds[:-2])  # 나노초 부분의 'ns' 제거 후 정수형으로 변환
        total_time = seconds + nanoseconds / 1e9  # 총 시간을 초 단위로 변환
        return f"{total_time:.4f}".rstrip('0').rstrip('.')  # 소수점 이하 4자리 표시하고 불필요한 0 제거
    except Exception as e:
        print(f"타임 포맷팅 중 오류 발생: {e}")
        return None  # 오류 발생 시 None 반환

def calculate_time_difference(parsed_data):
    if parsed_data is None:
        print("파싱된 데이터가 없습니다. DLT 파일을 확인하세요.")
        return  # 데이터가 없으면 함수 종료

    nav_map_traffic_start_time = []
    nav_map_traffic_end_time = None
    nav_map_traffic_end_ic_time = None
    nav_map_traffic_start_ic_time = []

    for marker_time, nav_value in parsed_data:
        # NAV_VALUE에 따른 시간을 저장
        if nav_value == "NAV_MAP_TRAFFIC_AVAILABLE_START_CID":
            nav_map_traffic_start_time.append(marker_time)
        elif nav_value == "NAV_MAP_TRAFFIC_AVAILABLE_END_CID":
            nav_map_traffic_end_time = marker_time
        elif nav_value == "NAV_MAP_TRAFFIC_AVAILABLE_END_IC":
            nav_map_traffic_end_ic_time = marker_time
        elif nav_value == "NAV_MAP_TRAFFIC_AVAILABLE_START_IC":
            nav_map_traffic_start_ic_time.append(marker_time)

    # NAV_MAP_TRAFFIC_AVAILABLE_START_CID에서 가장 작은 타임스탬프 선택
    if nav_map_traffic_start_time:
        nav_map_traffic_start_time.sort()  # 타임스탬프 정렬
        selected_traffic_start_time = nav_map_traffic_start_time[0]  # 가장 작은 값 선택
        formatted_traffic_start_time = format_time_string(selected_traffic_start_time)

        if nav_map_traffic_end_time:
            formatted_traffic_end_time = format_time_string(nav_map_traffic_end_time)

            # None 체크 후 시간 차 계산
            if formatted_traffic_start_time is not None and formatted_traffic_end_time is not None:
                total_start_time = float(formatted_traffic_start_time)
                total_end_time = float(formatted_traffic_end_time)
                time_difference = total_end_time - total_start_time
                
                # 각 시간 출력
                print(f"NAV Value: NAV_MAP_TRAFFIC_AVAILABLE_END_CID 의 타임은 {formatted_traffic_end_time} 초")
                print(f"NAV Value: NAV_MAP_TRAFFIC_AVAILABLE_START_CID 의 타임은 {formatted_traffic_start_time} 초")
                print(f"시간 차: {time_difference:.4f} 초\n")
            else:
                print("타임 포맷팅 중 오류 발생으로 계산을 수행할 수 없습니다.")
        else:
            print("NAV_MAP_TRAFFIC_AVAILABLE_END_CID 값이 없습니다.")
    else:
        print("NAV_MAP_TRAFFIC_AVAILABLE_START_CID 값이 없습니다.")

    # NAV_MAP_TRAFFIC_AVAILABLE_START_IC에서 가장 작은 타임스탬프 선택
    if nav_map_traffic_start_ic_time:
        nav_map_traffic_start_ic_time.sort()  # 타임스탬프 정렬
        selected_traffic_start_ic_time = nav_map_traffic_start_ic_time[0]  # 가장 작은 값 선택
        formatted_traffic_start_ic_time = format_time_string(selected_traffic_start_ic_time)

        if nav_map_traffic_end_ic_time:
            formatted_available_end_ic_time = format_time_string(nav_map_traffic_end_ic_time)

            # None 체크 후 시간 차 계산
            if formatted_traffic_start_ic_time is not None and formatted_available_end_ic_time is not None:
                total_start_ic_time = float(formatted_traffic_start_ic_time)
                total_available_start_time = float(formatted_available_end_ic_time)
                time_difference_ic = total_available_start_time - total_start_ic_time
                
                # 각 시간 출력
                print(f"NAV Value: NAV_MAP_TRAFFIC_AVAILABLE_END_IC 의 타임은 {formatted_available_end_ic_time} 초")
                print(f"NAV Value: NAV_MAP_TRAFFIC_AVAILABLE_START_IC 의 타임은 {formatted_traffic_start_ic_time} 초")
                print(f"시간 차: {time_difference_ic:.4f} 초\n")
            else:
                print("타임 포맷팅 중 오류 발생으로 계산을 수행할 수 없습니다.")
        else:
            print("NAV_MAP_AVAILABLE_START_CID 값이 없습니다.")
    else:
        print("NAV_MAP_TRAFFIC_AVAILABLE_START_IC 값이 없습니다.")

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산

def main():
    # dlt_parser에서 파싱된 데이터 가져와 계산 수행
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산