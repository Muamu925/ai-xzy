# -*- coding: utf-8 -*-
"""
gui/input_view.py

输入与发送区，包含文本输入框和发送按钮。
"""
import tkinter as tk
from tkinter import LEFT, RIGHT, END, DISABLED, NORMAL
from config import *


class InputView(tk.Frame):
    def __init__(self, master, send_callback):
        super().__init__(master, bg=COLOR_BG, padx=2, pady=2)
        self.send_callback = send_callback

        # 创建带样式的容器
        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(expand=True, fill=tk.X)

        # 输入框容器（带有边框和圆角效果）
        self.entry_frame = tk.Frame(
            self.container,
            bg=COLOR_INPUT_BG,
            highlightbackground=BORDER_COLOR,
            highlightcolor=BORDER_COLOR,
            highlightthickness=1,
            bd=0
        )
        self.entry_frame.pack(side=LEFT, expand=True, fill=tk.X, padx=(0, 8))

        # 输入框
        self.input_entry = tk.Entry(
            self.entry_frame,
            font=(FONT_FAMILY, FONT_SIZE_INPUT),
            bg=COLOR_INPUT_BG,
            fg="#000000",
            relief=tk.FLAT,
            insertbackground='#000000',
            insertwidth=2
        )
        self.input_entry.pack(expand=True, fill=tk.X, ipady=10, padx=10)
        self.input_entry.bind("<Return>", self._on_enter_pressed)

        # 发送按钮（带有圆角效果）
        self.send_button = tk.Button(
            self.container,
            text="发送",
            command=self._on_send_click,
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            bg=COLOR_BUTTON_BG,
            fg=COLOR_BUTTON_FG,
            relief=tk.FLAT,
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
            activebackground="#0069d9",  # 按钮按下时的颜色
            activeforeground=COLOR_BUTTON_FG
        )
        self.send_button.pack(side=RIGHT)

        # 美化按钮边缘
        self.send_button.config(highlightthickness=0, bd=0)

    def _on_enter_pressed(self, event):
        self._on_send_click()

    def _on_send_click(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        # 清空输入框
        self.input_entry.delete(0, END)
        # 调用回调函数传递用户输入
        if self.send_callback:
            self.send_callback(user_input)

    def disable(self):
        """
        禁用输入框和发送按钮。
        """
        self.input_entry.config(state=DISABLED)
        self.send_button.config(state=DISABLED)

    def enable(self):
        """
        启用输入框和发送按钮。
        """
        self.input_entry.config(state=NORMAL)
        self.send_button.config(state=NORMAL)
        self.input_entry.focus()