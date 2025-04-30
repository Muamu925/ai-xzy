# -*- coding: utf-8 -*-
"""
logic/chat_controller.py

聊天逻辑控制器：处理用户输入，尝试本地匹配；如果没有匹配则调用外部API。
"""
import sys
import time
import requests
import json
from config import API_KEY, API_URL, API_MODEL, API_TIMEOUT

class ChatController:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_response(self, user_input):
        """
        处理用户输入，返回AI回应内容和回应类型。
        """
        # 1. 尝试本地匹配
        local_response = self.db.find_matching_response(user_input)
        if local_response:
            # 模拟处理延迟
            time.sleep(0.3)
            # 保存聊天记录
            self.db.save_chat(user_input, local_response, 'local')
            return local_response, 'local'

        # 2. 调用API
        api_response = self._get_api_response(user_input)
        # 判断是否为错误提示
        if any(err in api_response for err in ["抱歉", "错误"]):
            # 错误类型的回应，不保存历史
            return api_response, 'error'
        else:
            # 正常回应，保存历史
            self.db.save_chat(user_input, api_response, 'api')
            return api_response, 'api'

    def _get_api_response(self, message):
        """
        调用外部 Gitee AI 接口获取回应。
        """
        if not API_KEY or API_KEY == "YOUR_GITEE_AI_API_KEY_HERE":
            return "抱歉，AI服务未配置。"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
        payload = {
            "model": API_MODEL,
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7,
            "messages": [
                {"role": "system", "content": "你是一个名叫 AI徐子越 的友好且乐于助人的AI助手。请提供清晰、准确且有帮助的回答。"},
                {"role": "user", "content": message}
            ]
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            if 'choices' in data and data['choices'] and 'message' in data['choices'][0] and 'content' in data['choices'][0]['message']:
                api_content = data['choices'][0]['message']['content']
                return api_content.strip() if api_content else "API返回了空内容。"
            else:
                # 意外的响应格式
                detail = json.dumps(data, ensure_ascii=False)
                print(f"API 错误: 意外的响应格式: {detail}", file=sys.stderr)
                return "抱歉，API 返回的数据格式不正确。"
        except requests.exceptions.Timeout:
            print(f"API 错误: 请求超时 ({API_TIMEOUT}秒)", file=sys.stderr)
            return "抱歉，连接 AI 服务超时，请稍后再试。"
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code
            error_text = http_err.response.text[:200]
            print(f"API 错误: HTTP {status_code} Error: {http_err}. Response: {error_text}", file=sys.stderr)
            if status_code == 401:
                return "抱歉，AI 服务认证失败，请检查您的 API Key 是否有效。"
            elif status_code == 429:
                return "抱歉，请求过于频繁，请稍后再试。"
            else:
                return f"抱歉，AI 服务返回错误 (代码: {status_code})，请稍后重试。"
        except requests.exceptions.RequestException as req_err:
            print(f"API 错误: 请求失败: {req_err}", file=sys.stderr)
            return "抱歉，连接 AI 服务时出错，请检查网络连接。"
        except Exception as e:
            print(f"API 错误: 未知错误: {e}", file=sys.stderr)
            return "抱歉，处理 AI 服务响应时发生内部错误。"
