# -*- coding: utf-8 -*-
"""
gui/chat_view.py

聊天展示区，负责显示用户和AI的对话，支持添加、替换和清空消息。
"""
import tkinter as tk
from tkinter import scrolledtext, WORD, END, NORMAL, DISABLED, LEFT, RIGHT
from config import *

class ChatView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLOR_CHAT_BG)
        # 创建带滚动条的文本区域
        self.chat_area = scrolledtext.ScrolledText(
            self,
            wrap=WORD,
            state=DISABLED,
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            bg=COLOR_CHAT_BG,
            padx=10,
            pady=10
        )
        self.chat_area.pack(expand=True, fill=tk.BOTH)
        # 配置文本标签（样式）
        self._configure_tags()

    def _configure_tags(self):
        """
        定义不同消息类型的文本样式标签。
        """
        self.chat_area.tag_configure('user',
                                     foreground=COLOR_USER_FG,
                                     font=(FONT_FAMILY, FONT_SIZE_NORMAL, 'bold'),
                                     justify=RIGHT,
                                     spacing3=5)
        self.chat_area.tag_configure('ai',
                                     foreground=COLOR_AI_FG,
                                     font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                                     justify=LEFT,
                                     spacing1=5,
                                     spacing3=5)
        self.chat_area.tag_configure('system',
                                     foreground=COLOR_SYS_FG,
                                     font=(FONT_FAMILY, FONT_SIZE_NORMAL - 1, 'italic'),
                                     justify=LEFT,
                                     spacing1=5,
                                     spacing3=5)
        self.chat_area.tag_configure('error',
                                     foreground=COLOR_ERR_FG,
                                     font=(FONT_FAMILY, FONT_SIZE_NORMAL, 'bold'),
                                     justify=LEFT,
                                     spacing1=5,
                                     spacing3=5)
        self.chat_area.tag_configure('thinking',
                                     foreground=COLOR_SYS_FG,
                                     font=(FONT_FAMILY, FONT_SIZE_NORMAL, 'italic'),
                                     justify=LEFT,
                                     spacing1=5,
                                     spacing3=5)

    def display_message(self, prefix, message, tags=('ai',)):
        """
        在聊天区末尾添加一条消息，并应用样式标签。
        返回消息的起始和结束索引（用于后续替换）。
        """
        self.chat_area.configure(state=NORMAL)
        # 如果已有消息，添加空行分隔
        if self.chat_area.index(END + "-1c") != "1.0":
            self.chat_area.insert(END, "\n\n")
        # 插入前缀
        prefix_start = self.chat_area.index(END + "-1c")
        self.chat_area.insert(END, prefix)
        # 插入消息内容
        message_start = self.chat_area.index(END + "-1c")
        self.chat_area.insert(END, message)
        message_end = self.chat_area.index(END + "-1c")
        # 应用样式标签
        primary_tag = tags[0] if isinstance(tags, (list, tuple)) else tags
        self.chat_area.tag_add(primary_tag, prefix_start, message_end)
        if isinstance(tags, (list, tuple)):
            for tag in tags:
                self.chat_area.tag_add(tag, prefix_start, message_end)
        self.chat_area.configure(state=DISABLED)
        self.chat_area.see(END)  # 滚动到最后
        return prefix_start, message_end

    def delete_range(self, start_index, end_index):
        """
        删除指定范围内的文本（用于替换思考提示）。
        """
        self.chat_area.configure(state=NORMAL)
        self.chat_area.delete(start_index, end_index)
        self.chat_area.configure(state=DISABLED)

    def insert_message_at(self, index, text, tags=('ai',)):
        """
        在指定位置插入文本消息，并应用样式标签。
        """
        self.chat_area.configure(state=NORMAL)
        self.chat_area.insert(index, text)
        # 计算插入文本后的结束索引
        end_index = self.chat_area.index(f"{index} + {len(text)} chars")
        primary_tag = tags[0] if isinstance(tags, (list, tuple)) else tags
        self.chat_area.tag_add(primary_tag, index, end_index)
        if isinstance(tags, (list, tuple)):
            for tag in tags:
                self.chat_area.tag_add(tag, index, end_index)
        self.chat_area.configure(state=DISABLED)
        self.chat_area.see(END)

    def clear(self):
        """
        清空聊天区域中的所有内容。
        """
        self.chat_area.configure(state=NORMAL)
        self.chat_area.delete("1.0", END)
        self.chat_area.configure(state=DISABLED)
