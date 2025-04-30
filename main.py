# -*- coding: utf-8 -*-
"""
main.py

程序入口：初始化主窗口并运行聊天应用。
"""
import sys
import tkinter as tk
from tkinter import messagebox
from config import API_KEY
from gui.main_window import MainWindow

if __name__ == "__main__":
    # 在启动 GUI 前检查 API Key 是否配置
    warning_text = (
        "警告: AI 未配置!\\n"
        "config 错误。"
    )
    if not API_KEY or API_KEY == "YOUR_GITEE_AI_API_KEY_HERE":
        print("\\n" + "*" * 10 + " 警告: Gitee AI API Key 未配置! " + "*" * 10)
        print(warning_text)
        # 弹窗提示
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("配置缺失", warning_text)
        root.destroy()

    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
