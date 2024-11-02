import tkinter as tk
from tkinter import filedialog

def analyze_dlt_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read(1000)  # 파일의 처음 1000바이트를 읽음
            print("원본 바이트 데이터:")
            print(content)

            # 인코딩 시도 목록
            encodings = [
                ('utf-8', 'UTF-8 디코딩 결과:'),
                ('utf-16', 'UTF-16 디코딩 결과:'),
                ('latin-1', 'Latin-1 디코딩 결과:'),
                ('ascii', 'ASCII 디코딩 결과:'),
                ('cp1252', 'CP1252 디코딩 결과:'),
                ('utf-32', 'UTF-32 디코딩 결과:'),
                ('EBCDIC', 'EBCDIC 디코딩 결과:', 'EBCDIC')
            ]

            for encoding in encodings:
                try:
                    if encoding[0] == 'EBCDIC':
                        # EBCDIC 인코딩은 특별한 라이브러리가 필요할 수 있음
                        print(f"{encoding[1]} (EBCDIC는 일반적으로 별도의 처리 필요)")
                    else:
                        decoded_content = content.decode(encoding[0], errors='ignore')
                        print(encoding[1])
                        print(decoded_content)
                except Exception as e:
                    print(f"{encoding[1]} 실패:", e)

    except Exception as e:
        print(f"파일을 여는 중 오류 발생: {e}")

def open_file():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="DLT 로그 파일 선택",
        filetypes=(("DLT 파일", "*.dlt"), ("모든 파일", "*.*"))
    )
    
    if file_path:
        analyze_dlt_file(file_path)

open_file()
