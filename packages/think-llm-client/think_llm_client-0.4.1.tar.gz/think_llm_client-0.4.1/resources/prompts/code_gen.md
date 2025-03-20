---
description: 【技术开发文档】解决聊天记录转Markdown文档问题，通过编写脚本实现层级分明、信息完整的转换功能，达到文档美观且易于查看的效果。
name: code_gen
---
帮我给 client.py 增加一个将聊天记录转换为 markdown文档的功能，主要作用如下：

1. 输入是聊天记录的路径，输出是文档的存储。
2. 聊天记录的格式如下：
{
  "timestamp": "20250212_142142",
  "messages": [
    {
      "role": "user",
      "content": "hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I assist you today? 😊",
      "reasoning_content": null
    }
  ],
  "system_prompt": null,
  "model_type": "llm",
  "provider": "deepseek",
  "model": "deepseek-chat",
  "max_completion_tokens": 8192
}
3. 在转换的时候要注意层级分明，顶端是这次对话的基本信息，不要把 system Prompt 暴露出去。model_type, provider, model可以提供。

主要需要包含：

用户问题：
AI思考过程：
AI回答结果：
---
用户问题：
AI思考过程：
AI回答结果：

如果没有 AI 思考过程的话，可以不用放这个字段。

4. 注意转出来的 markdown 要方便用户查看，美观