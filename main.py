import tkinter as tk
from tkinter import scrolledtext
import threading
import sys
import io
import nav_alternative_route
import nav_fps
import nav_route
import nav_search
import nav_start
import nav_traffic_info

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KPI Calculator")
        self.geometry("600x800")

        # 텍스트 박스 추가
        self.output_box = scrolledtext.ScrolledText(self, width=70, height=20)
        self.output_box.pack(pady=10)

        # 각 모듈을 위한 버튼 생성
        self.create_module_buttons()

    def create_module_buttons(self):
        # 각 버튼을 생성하고, 각 모듈의 함수를 호출
        modules = {
            "NAV_START": nav_start.main,
            "NAV_SEARCH": nav_search.main,
            "NAV_TRAFFIC_INFO": nav_traffic_info.main,
            "NAV_ROUTE": nav_route.main,
            "NAV_ALTERNATIVE_ROUTE": nav_alternative_route.main,
            "NAV_FPS": nav_fps.main,
        }

        for name, function in modules.items():
            button = tk.Button(self, text=f"Run {name}", command=lambda func=function: self.run_module(func))
            button.pack(pady=5)

    def run_module(self, function):
        # 텍스트 박스를 초기화
        self.output_box.delete(1.0, tk.END)
        # 별도의 스레드에서 모듈 실행
        thread = threading.Thread(target=self.execute_module, args=(function,))
        thread.start()

    def execute_module(self, function):
        # print 출력 캡처를 위한 StringIO 객체 생성
        output_capture = io.StringIO()
        sys.stdout = output_capture  # print 출력을 캡처
        
        try:
            # 함수 실행
            function()  # 각 모듈의 `main` 함수 실행
            output = output_capture.getvalue()  # 캡처된 출력 내용 가져오기
            self.display_output(output)
        except Exception as e:
            self.display_output(f"Error: {str(e)}")
        finally:
            sys.stdout = sys.__stdout__  # 원래 stdout으로 복원

    def display_output(self, output):
        # 텍스트 박스에 출력을 표시
        self.output_box.insert(tk.END, output)
        self.output_box.yview(tk.END)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
