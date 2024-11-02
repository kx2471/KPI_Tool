import dlt_parser  # dlt_parser.py 모듈을 가져옵니다.

def format_time_string(marker_time):
    """Marker Time을 초 단위의 문자열로 변환하여 반환합니다."""
    try:
        seconds, nanoseconds = marker_time.split('s', 1)  # 첫 번째 's'만 기준으로 분리
        seconds = int(seconds)  # 초 부분은 정수형으로 변환
        nanoseconds = int(nanoseconds[:-2])  # 나노초 부분의 'ns' 제거 후 정수형으로 변환
        total_time = seconds + nanoseconds / 1e9  # 총 시간을 초 단위로 변환
        return total_time  # 총 시간을 초 단위로 반환
    except Exception as e:
        print(f"타임 포맷팅 중 오류 발생: {e}")
        return None  # 오류 발생 시 None 반환

def calculate_route_times(parsed_data):
    if parsed_data is None:
        print("파싱된 데이터가 없습니다. DLT 파일을 확인하세요.")
        return  # 데이터가 없으면 함수 종료

    nav_route_start_time = None
    nav_route_end_times = []

    for marker_time, nav_value in parsed_data:
        if nav_value == "NAV_ROUTE_START":
            nav_route_start_time = marker_time
        elif nav_value == "NAV_ROUTE_END":
            nav_route_end_times.append(marker_time)  # NAV_ROUTE_END 값을 리스트에 추가

    if nav_route_start_time is None or len(nav_route_end_times) < 3:
        print("NAV_ROUTE_START 값이 없거나 NAV_ROUTE_END 값이 3개 미만입니다.")
        return

    # NAV_ROUTE_START 타임 포맷팅
    formatted_nav_route_start_time = format_time_string(nav_route_start_time)

    # NAV_ROUTE_END 값들로부터 시간 차 계산
    results = []
    for i, end_time in enumerate(nav_route_end_times[:3]):  # 처음 3개의 NAV_ROUTE_END만 사용
        formatted_end_time = format_time_string(end_time)
        if formatted_end_time is not None and formatted_nav_route_start_time is not None:
            time_difference = formatted_end_time - formatted_nav_route_start_time
            if i == 0:
                results.append(("티맵추천", time_difference))
            elif i == 1:
                results.append(("최소시간", time_difference))
            elif i == 2:
                results.append(("무료도로", time_difference))

    # 결과 출력
    for name, time in results:
        print(f"{name}의 시간 차: {time:.4f} 초")

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_route_times(parsed_data)  # 시간 차 계산