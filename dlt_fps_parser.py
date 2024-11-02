import tkinter as tk
from tkinter import filedialog
import re

def analyze_dlt_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()  # 전체 내용을 읽음
            decoded_content = content.decode('latin-1', errors='ignore')  # Latin-1로 디코딩
           
            # 정규식을 사용하여 특정 패턴 추출
            pattern = r'(\d+)\s(KPI_MARKER\s(\d+s\d+ns)\s(NAV_\w+.*?)(?:\s*:\s*(\d+\.\d+))?)'
            matches = re.findall(pattern, decoded_content)

            parsed_data = []
            
            if matches:
                for match in matches:
                    marker_time = match[2]  # 96s812863087ns
                    nav_value = match[3]    # NAV_~~
                    numeric_value = match[4] if match[4] else None  # 숫자값 (예: 120.0) 또는 None
                    
                    # NAV_MAP_FPS에 대해서만 numeric_value 추가
                    if "NAV_MAP_FPS" in nav_value:
                        parsed_data.append((marker_time, nav_value, numeric_value))
                        #print(f'Marker Time: {marker_time}, NAV Value: {nav_value} : {numeric_value}')
                    else:
                        parsed_data.append((marker_time, nav_value))  # numeric_value를 포함하지 않음
                        #print(f'Marker Time: {marker_time}, NAV Value: {nav_value}')
            else:
                print("일치하는 데이터가 없습니다.")
            
            return parsed_data  # 파싱된 데이터를 반환

    except Exception as e:
        print(f"파일을 여는 중 오류 발생: {e}")
        return None  # 오류 발생 시 None 반환

def open_file():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="DLT 로그 파일 선택",
        filetypes=(("DLT 파일", "*.dlt"), ("모든 파일", "*.*"))
    )
    
    if file_path:
        return analyze_dlt_file(file_path)  # 파싱된 데이터를 반환
    else:
        print("파일이 선택되지 않았습니다.")
        return None  # 파일 선택이 없으면 None 반환

if __name__ == "__main__":
    parsed_data = open_file()  # 파싱된 데이터 가져오기
    if parsed_data is not None:
        # 여기서 추출된 데이터로 추가 작업을 할 수 있습니다.
        print("최종 파싱 데이터:", parsed_data)