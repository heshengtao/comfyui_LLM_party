# API LLM Pipeline

节点名：`☁️API LLM Pipeline（上一轮输出）`

它复用 `☁️API LLM general link` 的 `LLM.chatbot()`，因此保留相同的 Loader、记忆、工具、图像、文件、历史、额外参数、流式输出和五路标准输出；额外增加 `pipeline_status`。

- 第一次运行使用原始用户提示词，同时后台生成第一条 LLM 输出。
- 第二次运行使用第一条输出，同时后台生成第二条。
- `pipeline_reset` 加 1 会清空 Pipeline 缓存及其会话实例。
- 后台尚未完成时重复 Queue，只保留最新的待处理输入。
- LLM 最终回答为空时保留上一轮成功输出，避免 `max_length` 截断导致提示词消失。
