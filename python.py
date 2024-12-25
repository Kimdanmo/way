import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow 라이브러리 사용
import pygame

class EscapeRoomApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("방탈출 게임")
        self.geometry("700x500")  # 창 크기 조정
        self.configure(bg="#FFFACD")  # 전체 창의 배경색 설정

        # pygame 초기화
        pygame.mixer.init()
        self.correct_sound = pygame.mixer.Sound("성공.wav")
        self.wrong_sound = pygame.mixer.Sound("실패.wav") 

        # 현재 선택을 저장할 변수
        self.selected_option = None

        # 초기 프레임 설정
        self.current_frame = None
        self.show_start_frame()

    def show_start_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#FFFACD")
        self.current_frame.pack(fill="both", expand=True)

        # 메시지 텍스트
        message = (
            "앞으로 나아가 보니 동서남북으로 된 문이 보인다.\n"
            "각 방향에서 다양한 특징에 난쟁이들이 오고 있다.\n"
            "이중 한 마리는 산타가 난쟁이로 변신한 상태다.\n"
            "진짜 산타가 오는 방향의 정 반대로 도망치자!"
        )

        label = tk.Label(
            self.current_frame,
            text=message,
            justify="left",
            padx=30,
            pady=30,
            font=("Helvetica", 16, "bold"),
            wraplength=650,
            bg="#F0F8FF"
        )
        label.pack()

        start_button = tk.Button(
            self.current_frame,
            text="시작 버튼",
            command=self.show_next_frame,
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        start_button.pack(pady=20)

    def show_next_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self, bg="#FFFACD")
        self.current_frame.pack(fill="both", expand=True)

        # 이미지 표시
        try:
            image = Image.open("image.png")
            image = image.resize((300, 300), Image.ANTIALIAS)  # 이미지 크기 조정
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.current_frame, image=self.photo, bg="#FFFACD")
            image_label.pack(pady=20)
        except Exception as e:
            messagebox.showerror("이미지 로드 실패", f"이미지를 로드하는데 실패했습니다.\n{e}")
            image_label = tk.Label(self.current_frame, text="[이미지 로드 실패]", font=("Helvetica", 16), bg="#FFFACD")
            image_label.pack(pady=20)

        # 선택 버튼 프레임
        options_frame = tk.Frame(self.current_frame, bg="#FFFACD")
        options_frame.pack(pady=10)

        # 선택 버튼 1~4
        self.option_vars = [tk.IntVar() for _ in range(4)]
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                options_frame,
                text=f"{i+1}번 길",
                font=("Helvetica", 12),
                width=10,
                command=lambda idx=i: self.toggle_option(idx)
            )
            btn.grid(row=0, column=i, padx=10, pady=10)
            self.option_buttons.append(btn)

        # 완료 버튼
        self.complete_button = tk.Button(
            self.current_frame,
            text="완료",
            command=self.complete_selection,
            font=("Helvetica", 14, "bold"),
            bg="#2196F3",
            fg="white",
            state="disabled",
            padx=20,
            pady=10
        )
        self.complete_button.pack(pady=20)

    def toggle_option(self, idx):
        if self.selected_option == idx:
            self.selected_option = None
            self.option_vars[idx].set(0)
            self.option_buttons[idx].configure(relief="raised", bg="#f0f0f0")
        else:
            if self.selected_option is not None:
                prev_btn = self.option_buttons[self.selected_option]
                self.option_vars[self.selected_option].set(0)
                prev_btn.configure(relief="raised", bg="#f0f0f0")
            self.selected_option = idx
            self.option_vars[idx].set(1)
            self.option_buttons[idx].configure(relief="sunken", bg="#ADD8E6")
        
        if self.selected_option is not None:
            self.complete_button.configure(state="normal")
        else:
            self.complete_button.configure(state="disabled")

    def complete_selection(self):
        if self.selected_option is not None:
            selected = self.selected_option + 1
            if selected == 3:
                self.correct_sound.play()
                self.show_result_window(
                    title="탈출 성공",
                    message="탈출에 성공 했습니다! 앞에 있는 문으로 나와주세요!",
                    success=True,
                    on_close=self.destroy
                )
            else:
                self.wrong_sound.play()
                self.show_result_window(
                    title="탈출 실패",
                    message="탈출에 실패 했습니다.",
                    success=False
                )
                self.reset_selection()
        else:
            self.show_warning("선택 필요", "선택을 먼저 해주세요.")

    def show_result_window(self, title, message, success=True, on_close=None):
        result_window = tk.Toplevel(self)
        result_window.title(title)
        result_window.geometry("500x300")
        result_window.configure(bg="#FFFFFF")
        result_window.grab_set()

        msg_color = "#4CAF50" if success else "#F44336"
        msg_font = ("Helvetica", 16, "bold")
        message_label = tk.Label(
            result_window,
            text=message,
            font=msg_font,
            fg=msg_color,
            bg="#FFFFFF",
            wraplength=450,
            justify="center"
        )
        message_label.pack(expand=True)

        if success and on_close:
            ok_command = lambda: [result_window.destroy(), on_close()]
        else:
            ok_command = result_window.destroy

        ok_button = tk.Button(
            result_window,
            text="확인",
            command=ok_command,
            font=("Helvetica", 12, "bold"),
            bg="#2196F3" if success else "#F44336",
            fg="white",
            padx=20,
            pady=10
        )
        ok_button.pack(pady=20)

    def show_warning(self, title, message):
        warning_window = tk.Toplevel(self)
        warning_window.title(title)
        warning_window.geometry("400x200")
        warning_window.configure(bg="#FFF3E0")
        warning_window.grab_set()

        message_label = tk.Label(
            warning_window,
            text=message,
            font=("Helvetica", 14, "bold"),
            fg="#FF9800",
            bg="#FFF3E0",
            wraplength=350,
            justify="center"
        )
        message_label.pack(expand=True, pady=20)

        ok_button = tk.Button(
            warning_window,
            text="확인",
            command=warning_window.destroy,
            font=("Helvetica", 12, "bold"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10
        )
        ok_button.pack(pady=10)

    def reset_selection(self):
        if self.selected_option is not None:
            btn = self.option_buttons[self.selected_option]
            btn.configure(relief="raised", bg="#f0f0f0")
            self.option_vars[self.selected_option].set(0)
            self.selected_option = None
        self.complete_button.configure(state="disabled")

if __name__ == "__main__":
    app = EscapeRoomApp()
    app.mainloop()
