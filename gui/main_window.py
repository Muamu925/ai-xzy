# -*- coding: utf-8 -*-
"""
gui/main_window.py

主窗口管理，包含菜单和布局，协调聊天视图和输入视图的交互。
"""
import tkinter as tk
from tkinter import Menu, messagebox, filedialog
import threading
import sys
from config import *
from database.manager import DatabaseManager
from gui.chat_view import ChatView
from gui.input_view import InputView
from logic.chat_controller import ChatController
from logic.history import HistoryManager

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("AI徐子越V3.0")
        self.root.geometry("700x550")
        self.root.configure(bg=COLOR_BG)

        # 初始化数据库管理器和聊天控制器
        self.db_manager = DatabaseManager()
        self.chat_controller = ChatController(self.db_manager)

        # 创建菜单
        self._create_menu()

        # 创建聊天视图
        self.chat_view = ChatView(self.root)
        self.chat_view.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # 创建输入视图
        self.input_view = InputView(self.root, send_callback=self.on_send)
        self.input_view.pack(fill=tk.X, padx=10, pady=(0, 10))

        # 显示初始欢迎消息
        self.chat_view.display_message(PREFIX_AI, "你好！我是 AI徐子越，很高兴为您服务。请问有什么我可以帮您的吗？", tags=('ai',))

    def _create_menu(self):
        """
        创建菜单栏，包括新建对话、导出历史、退出等功能。
        """
        menubar = Menu(self.root)
        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建对话", command=self.new_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="导出为 Markdown", command=lambda: self.export_history(format='md'))
        file_menu.add_command(label="导出为 JSON", command=lambda: self.export_history(format='json'))
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="菜单", menu=file_menu)

        self.root.config(menu=menubar)

    def new_conversation(self):
        """
        清空聊天视图，开始新的对话。
        """
        if messagebox.askyesno("确认", "确定要开始新对话吗？这将清空当前聊天记录，但不会删除历史保存。"):
            self.chat_view.clear()
            # 添加欢迎消息
            self.chat_view.display_message(PREFIX_AI, "又见面了！我是 AI徐子越，很高兴为您服务。请问有什么我可以帮您的吗？", tags=('ai',))

    def export_history(self, format):
        """
        导出聊天历史记录为 Markdown 或 JSON 文件。
        """
        # 获取历史记录数据
        history = self.db_manager.fetch_all_history()
        if not history:
            messagebox.showinfo("导出历史", "没有可用的聊天记录可供导出。")
            return

        # 选择保存文件位置
        filetypes = [("Markdown 文件", "*.md")] if format == 'md' else [("JSON 文件", "*.json")]
        ext = 'md' if format == 'md' else 'json'
        filepath = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=filetypes)
        if not filepath:
            return

        try:
            if format == 'md':
                HistoryManager.export_to_markdown(filepath, history)
            else:
                HistoryManager.export_to_json(filepath, history)
            messagebox.showinfo("导出成功", f"聊天记录已保存到 {filepath}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出历史记录时出错: {e}")

    def on_send(self, user_input):
        """
        处理用户输入：在聊天视图中显示用户消息，并启动后台线程获取响应。
        """
        if not user_input.strip():
            return
        # 显示用户消息
        self.chat_view.display_message(PREFIX_USER, user_input, tags=('user',))
        # 禁用输入区域
        self.input_view.disable()
        # 显示 '思考中...' 占位消息
        thinking_indices = self.chat_view.display_message(PREFIX_THINKING, "思考中...", tags=('thinking',))
        # 启动后台线程处理
        thread = threading.Thread(target=self._process_in_background, args=(user_input, thinking_indices))
        thread.daemon = True
        thread.start()

    def _process_in_background(self, user_input, thinking_indices):
        """
        在后台线程中处理用户输入，通过本地匹配或调用API获取响应。
        处理完成后使用主线程更新聊天视图。
        """
        try:
            response_text, response_type = self.chat_controller.get_response(user_input)
            tags = ('ai',) if response_type in ('local', 'api') else ('error',)
        except Exception as e:
            response_text = f"处理您的请求时发生内部错误: {e}"
            tags = ('error',)
        # 在主线程中更新聊天视图
        self.root.after(0, lambda: self._update_chat_view(response_text, tags, thinking_indices))

    def _update_chat_view(self, response_text, tags, thinking_indices):
        """
        在聊天视图中替换 '思考中...' 消息，并显示实际的回复。
        """
        start_idx, end_idx = thinking_indices
        try:
            # 删除 '思考中...' 占位消息
            self.chat_view.delete_range(start_idx, end_idx)
            # 插入实际响应
            prefix = PREFIX_AI if tags == ('ai',) else PREFIX_SYSTEM_ERROR
            self.chat_view.insert_message_at(start_idx, prefix + response_text, tags=tags)
        except Exception as e:
            # 如果删除或插入过程中发生错误，则直接追加消息
            print(f"GUI 更新错误: {e}", file=sys.stderr)
            fallback_prefix = PREFIX_AI if tags == ('ai',) else PREFIX_SYSTEM_ERROR
            self.chat_view.display_message(fallback_prefix, response_text, tags=tags)
        finally:
            # 重新启用输入区域
            self.input_view.enable()
