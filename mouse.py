import tkinter as tk
from tkinter import simpledialog
import pyautogui
import keyboard
import sys
import os

class ClickerApp:
    def __init__(self, root):
        self.root = root
        # 初始化时先隐藏窗口
        self.root.withdraw()
        self.root.title("鼠标左键连点器 By Mikasa F6开启/暂停")

        # 根据 PyInstaller 的环境来确定图标的路径
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # 打包后的环境
            icon_path = os.path.join(sys._MEIPASS, 'Mikasa.ico')
        else:
            # 开发环境
            icon_path = 'Mikasa.ico'
        self.root.iconbitmap(icon_path)

        # 设置窗口尺寸和居中定位
        window_width = 600
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # 界面组件
        self.clicking = False
        self.interval = 10  # 默认间隔设置为10毫秒
        self.label = tk.Label(root, text="按F6键开启/关闭连点器")
        self.label.pack(pady=10)
        self.change_interval_button = tk.Button(root, text="设置点击间隔", command=self.set_interval)
        self.change_interval_button.pack(fill=tk.X, expand=True, padx=20, pady=5)
        self.signature_label = tk.Label(root, text="By Mikasa")
        self.signature_label.pack(side=tk.BOTTOM, fill=tk.X)

        # 设置快捷键
        keyboard.add_hotkey('F6', self.toggle_clicking)

        # 在所有设置完成后显示窗口
        self.root.deiconify()

        # 处理窗口关闭
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_clicking(self):
        self.clicking = not self.clicking
        self.label.config(text="连点器已开启" if self.clicking else "连点器已关闭")
        if self.clicking:
            self.start_clicking()

    def start_clicking(self):
        if self.clicking:
            pyautogui.click()
            self.root.after(self.interval, self.start_clicking)

    def set_interval(self):
        interval = simpledialog.askfloat("输入间隔", "设置点击间隔 (毫秒):", minvalue=1, maxvalue=1000, initialvalue=self.interval)
        if interval is not None:
            self.interval = int(interval)

    def on_close(self):
        keyboard.unhook_all_hotkeys()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)
    root.mainloop()
