import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KPI Calculator")
        self.geometry("600x800")  # 창 크기 설정

        # 텍스트 박스 추가
        self.output_box = scrolledtext.ScrolledText(self, width=70, height=20)
        self.output_box.pack(pady=10)

        # 각 모듈을 위한 버튼 생성
        self.create_module_buttons()

    def create_module_buttons(self):
        # NAV_START 버튼
        nav_start_button = tk.Button(self, text="Run NAV_START", command=lambda: self.run_module("nav_start.py"))
        nav_start_button.pack(pady=5)

        # NAV_SEARCH 버튼
        nav_search_button = tk.Button(self, text="Run NAV_SEARCH", command=lambda: self.run_module("nav_search.py"))
        nav_search_button.pack(pady=5)

        # NAV_TRAFFIC_INFO 버튼
        nav_traffic_info_button = tk.Button(self, text="Run NAV_TRAFFIC_INFO", command=lambda: self.run_module("nav_traffic_info.py"))
        nav_traffic_info_button.pack(pady=5)

        # NAV_ROUTE 버튼
        nav_route_button = tk.Button(self, text="Run NAV_ROUTE", command=lambda: self.run_module("nav_route.py"))
        nav_route_button.pack(pady=5)

        # NAV_ALTERNATIVE_ROUTE 버튼
        nav_alternative_route_button = tk.Button(self, text="Run NAV_ALTERNATIVE_ROUTE", command=lambda: self.run_module("nav_alternative_route.py"))
        nav_alternative_route_button.pack(pady=5)

        # NAV_FPS 버튼
        nav_fps_button = tk.Button(self, text="Run NAV_FPS", command=lambda: self.run_module("nav_fps.py"))
        nav_fps_button.pack(pady=5)

    def run_module(self, module_name):
        # 텍스트 박스를 초기화
        self.output_box.delete(1.0, tk.END)
        # 별도의 스레드에서 모듈 실행
        thread = threading.Thread(target=self.execute_module, args=(module_name,))
        thread.start()

    def execute_module(self, module_name):
        try:
            # subprocess.Popen을 사용하여 모듈 실행
            process = subprocess.Popen(["python", module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()  # 출력을 캡처
            if output:
                self.display_output(output)
            if error:
                self.display_output(error)
        except Exception as e:
            self.display_output(f"Error: {str(e)}")

    def display_output(self, output):
        # 텍스트 박스에 출력을 표시
        self.output_box.insert(tk.END, output)
        self.output_box.yview(tk.END)  # 스크롤을 가장 아래로 이동

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
