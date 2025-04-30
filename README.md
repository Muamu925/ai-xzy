# AI徐子越 智能对话助手

AI徐子越是一款基于大语言模型（LLM）的本地智能对话程序，支持本地问答模板、Gitee AI 接口调用、多会话管理、打字机动画、Markdown 渲染、聊天记录持久化、分页浏览与导出，界面采用现代 Apple 风格设计，适合教育、日常问答和研发实验使用。

---

## ✨ 功能特色

- 🧠 **本地+API混合对话**：优先本地响应，匹配不到再调用 Gitee AI API。
- 💬 **打字机动画效果**：AI 回复逐字符呈现，增强拟人感与沉浸体验。
- 🌈 **Apple 风格界面**：使用 `ttkbootstrap` 实现圆角、美观、浅/深色主题。
- 🗂️ **多会话管理**：支持新建会话、切换历史、自动保存。
- 📝 **Markdown 渲染**：AI 输出支持标题、列表、加粗等 Markdown 语法。
- 🕘 **聊天记录保存与分页浏览**：本地 SQLite 自动持久化，支持翻页查看历史。
- ⌨️ **快捷键支持**：Enter/Ctrl+Enter 发送消息，快速高效。

---

## 📁 项目结构

```text
├── main.py                # 程序入口
├── chat_gui.py            # 界面逻辑（GUI）
├── database_manager.py    # 数据管理与 API 调用
├── assets/                # 图标、截图等资源
├── requirements.txt       # 所有依赖
```

---

## 📄 License

MIT License © 2025 AI徐子越

---

## 🙌 鸣谢

感谢 Gitee AI 提供高质量接口支持，以及开源社区的贡献。

---

> Made with ❤️ by Muamu925c

