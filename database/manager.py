# -*- coding: utf-8 -*-
"""
database/manager.py

用于管理 SQLite 数据库连接和操作，包括响应模板和聊天历史记录的管理。
"""
import sqlite3
import sys
import os

# 添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_NAME

class DatabaseManager:
    """
    管理 SQLite 数据库，用于存储响应模板和聊天历史记录。
    """
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_database()
        self._load_initial_data()

    def _get_connection(self):
        """
        获取数据库连接，并设置超时时间。
        """
        try:
            return sqlite3.connect(self.db_name, timeout=10)
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}", file=sys.stderr)
            return None

    def _execute_query(self, query, params=(), fetchone=False, fetchall=False, commit=False):
        """
        执行 SQL 查询。
        """
        conn = self._get_connection()
        if not conn:
            return None
        result = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            elif fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"数据库查询错误 (Query: {query[:50]}...): {e}", file=sys.stderr)
        finally:
            conn.close()
        return result

    def _init_database(self):
        """
        如果数据库表不存在，则创建它们。
        """
        # 响应模板表
        create_templates_table = (
            "CREATE TABLE IF NOT EXISTS response_templates ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pattern TEXT NOT NULL UNIQUE,"
            "response TEXT NOT NULL,"
            "category TEXT,"
            "priority INTEGER DEFAULT 1"
            ")"
        )
        # 聊天历史表
        create_history_table = (
            "CREATE TABLE IF NOT EXISTS chat_history ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_input TEXT NOT NULL,"
            "response TEXT NOT NULL,"
            "response_type TEXT NOT NULL CHECK(response_type IN ('local','api','error')),"
            "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
            ")"
        )
        self._execute_query(create_templates_table, commit=True)
        self._execute_query(create_history_table, commit=True)

    def _load_initial_data(self):
        """
        加载预定义的响应模板（仅插入一次，避免重复）。
        """
        initial_templates = [
            {"pattern": "你好|打招呼|hello|hi|您好", "response": "你好呀！我是AI徐子越，很高兴和你聊天。有什么我可以帮忙的吗？", "category": "greeting", "priority": 10},
            {"pattern": "再见|拜拜|goodbye|bye", "response": "再见！期待下次和你交流。", "category": "farewell", "priority": 10},
            {"pattern": "你是谁|你叫什么|名字", "response": "我是AI徐子越。", "category": "introduction", "priority": 9},
            {"pattern": "天气怎么样|天气如何", "response": "我无法实时查询天气呢，建议您查看专业的天气预报应用获取最新信息哦。", "category": "weather", "priority": 5},
            {"pattern": "谢谢|感谢", "response": "不客气！能帮到你就好。", "category": "thanks", "priority": 8}
        ]
        insert_query = "INSERT OR IGNORE INTO response_templates (pattern, response, category, priority) VALUES (?, ?, ?, ?)"
        conn = self._get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            data = [(t["pattern"], t["response"], t["category"], t["priority"]) for t in initial_templates]
            cursor.executemany(insert_query, data)
            conn.commit()
        except sqlite3.Error as e:
            print(f"加载初始数据时出错: {e}", file=sys.stderr)
        finally:
            conn.close()

    def find_matching_response(self, user_input):
        """
        根据用户输入中的关键词，查找匹配的本地响应模板。
        如果找到匹配的模板则返回对应回复，否则返回 None。
        """
        if not user_input:
            return None
        templates = self._execute_query(
            "SELECT pattern, response FROM response_templates ORDER BY priority DESC",
            fetchall=True
        )
        if not templates:
            return None
        user_input_lower = user_input.lower()
        for pattern, response in templates:
            keywords = [kw.strip().lower() for kw in pattern.split('|') if kw.strip()]
            if any(keyword in user_input_lower for keyword in keywords):
                return response
        return None

    def save_chat(self, user_input, response, response_type):
        """
        将一次聊天交互保存到历史记录表。
        """
        self._execute_query(
            "INSERT INTO chat_history (user_input, response, response_type) VALUES (?, ?, ?)",
            (user_input, response, response_type),
            commit=True
        )

    def fetch_all_history(self):
        """
        获取所有聊天历史记录，按照时间顺序返回。
        """
        rows = self._execute_query(
            "SELECT user_input, response, response_type, timestamp FROM chat_history ORDER BY timestamp",
            fetchall=True
        )
        return rows or []
