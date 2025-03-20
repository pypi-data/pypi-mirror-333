# Think LLM Client

一个灵活的 LLM 和 VLM 模型交互 SDK，支持基础的模型交互和 CLI 界面。

## 特性

- 支持多种模型类型（LLM、VLM）
- 支持多个提供商和模型
- 提供基础的模型交互接口
- 提供丰富的 CLI 界面
- 支持图片分析和比较
- 支持流式输出和思维链
- 支持对话历史管理
- 类型提示和文档完备

## 安装

使用 [uv](https://github.com/astral-sh/uv) 安装（推荐）：

```bash
uv pip install think-llm-client
```

或使用传统的 pip：

```bash
pip install think-llm-client
```

## 快速开始

### 基础用法

```python
import asyncio
from think_llm_client import LLMClient

async def main():
    # 创建客户端
    client = LLMClient()
    
    # 设置模型
    client.set_model("llm", "openai", "gpt-4")
    
    # 基础对话
    reasoning, response = await client.chat("Python 中的装饰器是什么？")
    print(f"回答：{response}")
    
    # 图片分析
    reasoning, response = await client.analyze_image(
        "image.jpg",
        "分析这个产品的优缺点"
    )
    print(f"图片分析：{response}")

if __name__ == "__main__":
    asyncio.run(main())
```

### CLI 界面

```bash
# 启动交互式对话
python -m think_llm_client.cli chat

# 分析图片
python -m think_llm_client.cli analyze image.jpg "描述这个图片"
```

## 配置

### 配置文件位置

配置文件可以放置在以下位置：
1. 项目根目录的 `config.json`
2. 用户目录下的 `.think_llm_client/config.json`

你可以在创建客户端时指定配置文件路径：

```python
from think_llm_client import LLMClient

client = LLMClient(config_path="/path/to/your/config.json")
```

### 配置文件格式

配置文件使用 JSON 格式，支持配置多种模型类型（LLM、VLM）和多个提供商：

```json
{
  "model_types": {
    "llm": {
      "providers": {
        "openai": {
          "api_key": "your-api-key",
          "api_url": "https://api.openai.com/v1",
          "model": {
            "gpt-4": {
              "max_tokens": 2000,
              "system_prompt": "你是一个有帮助的助手"
            },
            "gpt-3.5-turbo": {
              "max_tokens": 1000
            }
          }
        }
      }
    },
    "vlm": {
      "providers": {
        "openai": {
          "api_key": "your-api-key",
          "api_url": "https://api.openai.com/v1",
          "model": {
            "gpt-4-vision-preview": {
              "max_tokens": 1000
            }
          }
        }
      }
    }
  }
}
```

或者使用环境变量：

```bash
export OPENAI_API_KEY=your-api-key
```

## 详细使用说明

### 1. 基础对话

```python
import asyncio
from think_llm_client import LLMClient

async def main():
    # 创建客户端
    client = LLMClient()
    
    # 设置模型
    client.set_model("llm", "openai", "gpt-4")
    
    # 基础对话（默认使用流式输出）
    reasoning, response = await client.chat("Python 中的装饰器是什么？")
    print(f"思维过程：{reasoning}")
    print(f"回答：{response}")
    
    # 非流式对话
    reasoning, response = await client.chat(
        "给我一个装饰器的例子",
        stream=False
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 图片分析

```python
async def analyze_images():
    client = LLMClient()
    client.set_model("vlm", "openai", "gpt-4-vision")
    
    # 分析单张图片
    reasoning, response = await client.analyze_image(
        "product.jpg",
        "分析这个产品的优缺点"
    )
    
    # 比较多张图片
    reasoning, response = await client.compare_images(
        ["image1.jpg", "image2.jpg"],
        "比较这两张图片的区别"
    )
```

### 3. 对话历史管理

```python
async def manage_chat_history():
    client = LLMClient()
    client.set_model("llm", "openai", "gpt-4")
    
    # 进行对话
    await client.chat("你好")
    await client.chat("今天天气不错")
    
    # 保存对话历史
    client.save_chat_history("my_chat.json")
    
    # 清除当前对话历史
    client.clear_history()
    
    # 加载之前的对话历史
    client.load_chat_history_from_file("my_chat.json")
    
    # 获取可用的历史记录
    histories = client.get_available_histories()
    for path, timestamp in histories:
        print(f"历史记录：{path}, 时间：{timestamp}")
```

### 4. 流式输出处理

```python
async def handle_stream():
    client = LLMClient()
    client.set_model("llm", "openai", "gpt-4")
    
    async for type_, chunk, full_content in client.chat_stream("讲个故事"):
        if type_ == "reasoning":
            print(f"思维过程: {chunk}", end="")
        else:
            print(f"内容: {chunk}", end="")
```

## CLI 使用

### 基础对话

```bash
# 启动交互式对话
python -m think_llm_client.cli chat

# 指定模型进行对话
python -m think_llm_client.cli chat --model-type llm --provider openai --model gpt-4
```

### 图片分析

```bash
# 分析单张图片
python -m think_llm_client.cli analyze image.jpg "描述这个图片"

# 比较多张图片
python -m think_llm_client.cli compare image1.jpg image2.jpg "比较这两张图片的区别"
```

## 高级特性

### 流式输出

```python
async def main():
    client = LLMClient()
    client.set_model("llm", "openai", "gpt-4")
    
    # 启用流式输出
    async for chunk_type, chunk, full_content in client.chat_stream("解释量子计算"):
        if chunk_type == "reasoning":
            print(f"思维过程: {chunk}", end="")
        elif chunk_type == "content":
            print(f"回答: {chunk}", end="")
```

### 对话历史管理

```python
# 保存对话历史
client.save_history("chat_history.json")

# 加载对话历史
client.load_history_from_file("chat_history.json")
```

## 开发

使用 [uv](https://github.com/astral-sh/uv) 安装开发依赖（推荐）：

```bash
uv pip install -e ".[dev]"
```

或使用传统的 pip：

```bash
pip install -e ".[dev]"
```

运行测试和代码检查：

```bash
# 运行测试
pytest

# 代码格式化
black .
ruff check .
mypy .
```

## 添加新的 Git 标签并推送到 GitHub

1. 确保所有更改已提交并推送到主分支：
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. 创建新的 Git 标签：
   ```bash
   git tag vX.Y.Z
   ```

3. 推送标签到 GitHub：
   ```bash
   git push origin vX.Y.Z
   ```

## 许可证

MIT License
