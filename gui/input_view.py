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
        super().__init__(master, bg=COLOR_BG)
        self.send_callback = send_callback

        # 输入框
        self.input_entry = tk.Entry(
            self,
            font=(FONT_FAMILY, FONT_SIZE_INPUT),
            bg=COLOR_INPUT_BG,
            relief=tk.FLAT,
            insertbackground='black'
        )
        self.input_entry.pack(side=LEFT, expand=True, fill=tk.X, ipady=8, padx=(0, 5))
        self.input_entry.bind("<Return>", self._on_enter_pressed)

        # 发送按钮
        self.send_button = tk.Button(
            self,
            text="发送",
            command=self._on_send_click,
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            bg=COLOR_BUTTON_BG,
            fg=COLOR_BUTTON_FG,
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.send_button.pack(side=RIGHT)

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
