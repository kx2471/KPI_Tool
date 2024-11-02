import tkinter as tk
from tkinter import messagebox
import dlt_parser
import nav_start
import nav_fps
import nav_traffic_info  # 필요에 따라 추가
import nav_search
import nav_route

class DLTAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("DLT Analyzer")

        self.result_text = tk.Text(master, height=20, width=70)
        self.result_text.pack()

        self.analyze_button = tk.Button(master, text="DLT 파일 분석", command=self.analyze_dlt_file)
        self.analyze_button.pack()

    def analyze_dlt_file(self):
        parsed_data = dlt_parser.open_file()  # DLT 파일 파싱
        if parsed_data is None:
            messagebox.showerror("오류", "파싱된 데이터가 없습니다.")
            return

        # 각 모듈에서 계산된 결과 가져오기
        nav_start_results = nav_start.calculate_time_difference(parsed_data)
        fps_results = nav_fps.calculate_statistics(parsed_data)
        # 다른 모듈의 결과도 필요에 따라 가져올 수 있습니다.

        # 결과 표시
        self.result_text.delete(1.0, tk.END)  # 기존 내용 삭제
        self.result_text.insert(tk.END, "NAV Start 결과:\n")
        self.result_text.insert(tk.END, f"{nav_start_results}\n\n")
        self.result_text.insert(tk.END, "FPS 통계 결과:\n")
        self.result_text.insert(tk.END, f"{fps_results}\n\n")
        # 다른 모듈의 결과도 표시할 수 있습니다.

if __name__ == "__main__":
    root = tk.Tk()
    app = DLTAnalyzerApp(root)
    root.mainloop()