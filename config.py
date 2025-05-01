# -*- coding: utf-8 -*-
"""
config.py

配置文件，统一管理常量（字体、颜色、API 配置等）和全局设置。
"""
import base64
import sys
import platform

# -------------------- API 配置 --------------------
try:
    # 这里使用 Base64 编码存储 API Key，提高代码安全性
    API_KEY = base64.b64decode("SUYwTUVXVUtNSThUSzdRR0hZRUozNk9XTTJKTTBOT0RENU9WRk9QVg==").decode('utf-8')
except Exception as e:
    print(f"警告: API Key 解码失败 ({e})。将使用默认占位符。", file=sys.stderr)
    API_KEY = "YOUR_GITEE_AI_API_KEY_HERE"

API_URL = "https://ai.gitee.com/v1/chat/completions"
API_MODEL = "Qwen2.5-7B-Instruct"
API_TIMEOUT = 45  # API 请求超时时间（秒）

# ------------------ 数据库配置 -------------------
DB_NAME = "xzy.db"  # 数据库文件名，存储聊天记录和响应模板

# --------------- 界面样式配置 (Apple 风格) -------------------
# 根据操作系统选择最佳字体
if platform.system() == "Darwin":  # macOS
    FONT_FAMILY = "SF Pro"
elif platform.system() == "Windows":
    FONT_FAMILY = "Microsoft YaHei UI"
else:  # Linux 和其他
    FONT_FAMILY = "Noto Sans CJK SC"

# 字体设置
FONT_SIZE_NORMAL = 11           # 普通文本字体大小
FONT_SIZE_INPUT = 12            # 输入框文本字体大小

# 颜色设置 (Apple 风格配色)
COLOR_BG = "#F5F5F7"             # 应用程序背景色 (Apple 浅灰)
COLOR_CHAT_BG = "#FFFFFF"        # 聊天区域背景色 (白色)
COLOR_INPUT_BG = "#FFFFFF"       # 输入框背景色 (白色)
COLOR_USER_FG = "#007AFF"        # 用户消息文本颜色 (苹果蓝)
COLOR_AI_FG = "#34C759"          # AI 消息文本颜色 (苹果绿)
COLOR_SYS_FG = "#8E8E93"         # 系统/提示消息文本颜色 (苹果灰)
COLOR_ERR_FG = "#FF3B30"         # 错误消息文本颜色 (苹果红)
COLOR_BUTTON_BG = "#007AFF"      # 按钮背景色
COLOR_BUTTON_FG = "#FFFFFF"      # 按钮文字颜色

# 边框和阴影
BORDER_COLOR = "#E5E5EA"         # 边框颜色
BORDER_RADIUS = 8                # 圆角大小
SHADOW_COLOR = "#00000015"       # 阴影颜色 (带透明度)

# 文本前缀
PREFIX_USER = "你: "
PREFIX_AI = "AI徐子越: "
PREFIX_SYSTEM_ERROR = "系统错误: "
PREFIX_THINKING = "AI徐子越: "  # "思考中..." 的前缀