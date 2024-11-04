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

    nav_start_time = None
    nav_engine_available_time = None
    nav_map_available_start_time = None
    nav_map_available_end_time = None
    nav_map_available_start_ic = None
    nav_map_available_end_ic = None

    for marker_time, nav_value in parsed_data:
        # NAV_VALUE에 따른 시간을 저장
        if nav_value == "NAV_START":
            nav_start_time = marker_time
        elif nav_value == "NAV_ENGINE_AVAILABLE":
            nav_engine_available_time = marker_time
        elif nav_value == "NAV_MAP_AVAILABLE_START_CID":
            nav_map_available_start_time = marker_time
        elif nav_value == "NAV_MAP_AVAILABLE_END_CID":
            nav_map_available_end_time = marker_time
        elif nav_value == "NAV_MAP_AVAILABLE_START_IC":
            nav_map_available_start_ic = marker_time
        elif nav_value == "NAV_MAP_AVAILABLE_END_IC":
            nav_map_available_end_ic = marker_time

    # NAV_ENGINE_AVAILABLE과 NAV_START 간의 시간 차 계산
    if nav_start_time and nav_engine_available_time:
        formatted_nav_start_time = format_time_string(nav_start_time)
        formatted_nav_engine_available_time = format_time_string(nav_engine_available_time)

        if formatted_nav_start_time is not None and formatted_nav_engine_available_time is not None:
            total_start_time = float(formatted_nav_start_time)
            total_available_time = float(formatted_nav_engine_available_time)
            time_difference = total_available_time - total_start_time

            # 각 시간 출력
            print(f"NAV Value: NAV_ENGINE_AVAILABLE 의 타임은 {formatted_nav_engine_available_time} 초")
            print(f"NAV Value: NAV_START 의 타임은 {formatted_nav_start_time} 초")
            print(f"시간 차: {time_difference:.4f} 초\n")
        else:
            print("타임 포맷팅 중 오류 발생으로 계산을 수행할 수 없습니다.")
    else:
        print("NAV_START 또는 NAV_ENGINE_AVAILABLE 값이 없습니다.")

    # NAV_MAP_AVAILABLE_END_CID와 NAV_MAP_AVAILABLE_START_CID 간의 시간 차 계산
    if nav_map_available_start_time and nav_map_available_end_time:
        formatted_nav_map_available_start_time = format_time_string(nav_map_available_start_time)
        formatted_nav_map_available_end_time = format_time_string(nav_map_available_end_time)

        if formatted_nav_map_available_start_time is not None and formatted_nav_map_available_end_time is not None:
            total_map_start_time = float(formatted_nav_map_available_start_time)
            total_map_end_time = float(formatted_nav_map_available_end_time)
            map_time_difference = total_map_end_time - total_map_start_time

            # 각 시간 출력
            print(f"NAV Value: NAV_MAP_AVAILABLE_END_CID 의 타임은 {formatted_nav_map_available_end_time} 초")
            print(f"NAV Value: NAV_MAP_AVAILABLE_START_CID 의 타임은 {formatted_nav_map_available_start_time} 초")
            print(f"시간 차: {map_time_difference:.4f} 초\n")
        else:
            print("NAV_MAP_AVAILABLE_START_CID 또는 NAV_MAP_AVAILABLE_END_CID의 타임 포맷팅 중 오류 발생.")
    else:
        print("NAV_MAP_AVAILABLE_START_CID 또는 NAV_MAP_AVAILABLE_END_CID 값이 없습니다.")

    # NAV_MAP_AVAILABLE_END_IC와 NAV_MAP_AVAILABLE_START_IC 간의 시간 차 계산
    if nav_map_available_start_ic and nav_map_available_end_ic:
        formatted_nav_map_available_start_ic = format_time_string(nav_map_available_start_ic)
        formatted_nav_map_available_end_ic = format_time_string(nav_map_available_end_ic)

        if formatted_nav_map_available_start_ic is not None and formatted_nav_map_available_end_ic is not None:
            total_ic_start_time = float(formatted_nav_map_available_start_ic)
            total_ic_end_time = float(formatted_nav_map_available_end_ic)
            ic_time_difference = total_ic_end_time - total_ic_start_time

            # 각 시간 출력
            print(f"NAV Value: NAV_MAP_AVAILABLE_END_IC 의 타임은 {formatted_nav_map_available_end_ic} 초")
            print(f"NAV Value: NAV_MAP_AVAILABLE_START_IC 의 타임은 {formatted_nav_map_available_start_ic} 초")
            print(f"시간 차: {ic_time_difference:.4f} 초")
        else:
            print("NAV_MAP_AVAILABLE_START_IC 또는 NAV_MAP_AVAILABLE_END_IC의 타임 포맷팅 중 오류 발생.")
    else:
        print("NAV_MAP_AVAILABLE_START_IC 또는 NAV_MAP_AVAILABLE_END_IC 값이 없습니다.")

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산

def main():
    # dlt_parser에서 파싱된 데이터 가져와 계산 수행
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산
