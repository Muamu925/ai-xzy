# -*- coding: utf-8 -*-
"""
logic/history.py

聊天记录管理与导出功能，支持将聊天历史保存为 Markdown 或 JSON。
"""
import json

class HistoryManager:
    @staticmethod
    def export_to_markdown(filepath, history):
        """
        将聊天历史记录导出为 Markdown 文件。
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# 聊天记录导出\\n\\n")
            for idx, (user_input, response, response_type, timestamp) in enumerate(history, start=1):
                f.write(f"### {idx}. 时间: {timestamp}\\n")
                f.write(f"- **你:** {user_input}\\n")
                if response_type == 'error':
                    f.write(f"- **系统错误:** {response}\\n")
                else:
                    f.write(f"- **AI徐子越:** {response}\\n")
                f.write("\\n")

    @staticmethod
    def export_to_json(filepath, history):
        """
        将聊天历史记录导出为 JSON 文件。
        """
        data = []
        for user_input, response, response_type, timestamp in history:
            entry = {
                "timestamp": timestamp,
                "user_input": user_input,
                "response": response,
                "response_type": response_type
            }
            data.append(entry)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
