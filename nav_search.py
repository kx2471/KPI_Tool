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

    nav_search_start_times = []
    nav_search_end_times = []

    for marker_time, nav_value in parsed_data:
        # NAV_VALUE에 따른 시간을 저장
        if nav_value == "NAV_SEARCH_START":
            nav_search_start_times.append(marker_time)
        elif nav_value == "NAV_SEARCH_END":
            nav_search_end_times.append(marker_time)

    # 가장 처음 NAV_SEARCH_END 찾기
    if nav_search_end_times:
        first_end_time = nav_search_end_times[0]
        
        # 첫 번째 NAV_SEARCH_END의 직전에 나온 NAV_SEARCH_START 찾기
        previous_start_time = None
        for marker_time, nav_value in parsed_data:
            if nav_value == "NAV_SEARCH_START":
                previous_start_time = marker_time
            elif nav_value == "NAV_SEARCH_END":
                # 첫 번째 NAV_SEARCH_END가 발견된 후 중단
                break
        
        if previous_start_time is not None:
            # 각 시간을 포맷팅
            formatted_previous_start_time = format_time_string(previous_start_time)
            formatted_first_end_time = format_time_string(first_end_time)

            # None 체크 후 시간 차 계산
            if (formatted_previous_start_time is not None and
                formatted_first_end_time is not None):
                
                total_previous_start_time = float(formatted_previous_start_time)
                total_first_end_time = float(formatted_first_end_time)

                time_difference = total_first_end_time - total_previous_start_time
                
                # 각 시간 출력
                print(f"가장 처음 NAV_SEARCH_END 의 타임은 {formatted_first_end_time} 초")
                print(f"가장 직전에 나온 NAV_SEARCH_START 의 타임은 {formatted_previous_start_time} 초")
                print(f"시간 차: {time_difference:.4f} 초")
            else:
                print("타임 포맷팅 중 오류 발생으로 계산을 수행할 수 없습니다.")
        else:
            print("직전에 나온 NAV_SEARCH_START 값이 없습니다.")
    else:
        print("NAV_SEARCH_END 값이 없습니다.")

if __name__ == "__main__":
    parsed_data = dlt_parser.open_file()  # dlt_parser.py에서 파싱된 데이터 가져오기
    calculate_time_difference(parsed_data)  # 시간 차 계산  
