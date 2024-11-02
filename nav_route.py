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

    nav_route_start_time = None
    nav_route_end_time = None

    for marker_time, nav_value in parsed_data:
        if nav_value == "NAV_ROUTE_START":
            nav_route_start_time = marker_time
        elif nav_value == "NAV_ROUTE_END":
            # 가장 처음 나온 NAV_ROUTE_END 값을 사용
            if nav_route_end_time is None:
                nav_route_end_time = marker_time

    if nav_route_end_time and nav_route_start_time:
        # NAV_ROUTE_END 타임을 포맷팅
        formatted_nav_route_end_time = format_time_string(nav_route_end_time)

        # NAV_ROUTE_START 타임을 포맷팅
        formatted_nav_route_start_time = format_time_string(nav_route_start_time)

        # None 체크 후 시간 차 계산
        if formatted_nav_route_end_time is not None and formatted_nav_route_start_time is not None:
            total_end_time = float(formatted_nav_route_end_time)
            total_start_time = float(formatted_nav_route_start_time)
            time_difference = total_end_time - total_start_time
            
            # 각 시간 출력
            print(f"NAV Value: NAV_ROUTE_END 의 타임은 {formatted_nav_route_end_time} 초")
            print(f"NAV Value: NAV_ROUTE_START 의 타임은 {formatted_nav_route_start_time} 초")
            print(f"시간 차: {time_difference:.4f} 초")
        else:
            print("타임 포맷팅 중 오류 발생으로 계산을 수행할 수 없습니다.")
    else:
        print("NAV_ROUTE_START 또는 NAV_ROUTE_END 값이 없습니다.")

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산  