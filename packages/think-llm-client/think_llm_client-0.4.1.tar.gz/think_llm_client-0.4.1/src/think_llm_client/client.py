from __future__ import annotations

import asyncio
import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from openai import OpenAI
# 导入 Anthropic 库
from anthropic import Anthropic, AsyncAnthropic

from .exceptions import ConfigurationError, ModelNotFoundError
from .utils import Config
from .utils.config import ModelConfig, ModelType, Provider
from .utils.logger import setup_logger
import logging

# 初始化项目特定的日志配置
logger = setup_logger("think-llm-client")

class LLMClient:
    """LLM 客户端基类，提供核心的模型交互功能

    Examples:
        >>> client = LLMClient()
        >>> client.set_model("llm", "openai", "gpt-4")
        >>> response = await client.chat("Hello!")

        >>> # 使用视觉模型
        >>> client.set_model("vlm", "openai", "gpt-4-vision")
        >>> response = await client.chat("描述这张图片", images=["image.jpg"])
    """

    DEFAULT_MAX_TOKENS = 8192

    def __init__(
        self,
        config_path: Optional[str] = None,
        history_dir: Optional[str] = None,
        export_dir: Optional[str] = None,
    ):
        """初始化客户端

        Args:
            config_path: 配置文件路径，如果不指定则使用默认路径 (~/.think-llm-client/config/llm_config.json)
            history_dir: 历史记录目录路径，如果不指定则使用默认路径（config_path的上级目录的history子目录）
            export_dir: 导出文件目录路径，如果不指定则使用默认路径（config_path的上级目录的exports子目录）
        """
        self.config_path = (
            Path(config_path)
            if config_path
            else Path.home() / ".think-llm-client" / "config" / "llm_config.json"
        )
        logger.info(f"大模型配置文件路径：{self.config_path}")

        self.history_dir = (
            Path(history_dir) if history_dir else Path.home() / ".think-llm-client" / "history"
        )
        self.history_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"历史记录目录：{self.history_dir}")

        self.export_dir = (
            Path(export_dir) if export_dir else Path.home() / ".think-llm-client" / "exports"
        )
        self.export_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"导出目录：{self.export_dir}")

        self.model_types: Dict[str, ModelType] = {}
        self.current_model_type: Optional[str] = None
        self.current_provider: Optional[str] = None
        self.current_model: Optional[str] = None
        self.client: Optional[Union[OpenAI, Anthropic, AsyncAnthropic]] = None
        self.messages: List[Dict[str, Any]] = []
        self.system_prompt: Optional[str] = None
    

        logger.info(f"大模型客户端初始化完成")

        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            config = Config(self.config_path)

            # 转换配置数据结构
            self.model_types = {
                type_name: ModelType.from_dict(type_data)
                for type_name, type_data in config.config.items()
            }

        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise ConfigurationError(f"无法加载配置文件: {e}")

    def get_available_models(self) -> List[Tuple[str, str, str]]:
        """获取可用的模型列表

        Returns:
            List[Tuple[str, str, str]]: 返回模型列表，每个元素为 (model_type, provider_key, model_key)
        """
        models = []
        for type_key, type_info in self.model_types.items():
            for provider_key, provider in type_info.providers.items():
                for model_key in provider.model.keys():
                    models.append((type_key, provider_key, model_key))
        return models

    def set_model(self, model_type: str, provider_key: str, model_key: str) -> None:
        """设置当前使用的模型

        Args:
            model_type: 模型类型
            provider_key: 供应商标识
            model_key: 模型标识

        Raises:
            ValueError: 当指定的模型类型、供应商或模型不存在时抛出
        """
        if model_type not in self.model_types:
            raise ValueError(f"未知的模型类型: {model_type}")
        logger.info(f"当前模型类型：{model_type}")
        model_type_config = self.model_types[model_type]
        if provider_key not in model_type_config.providers:
            raise ValueError(f"未知的供应商: {provider_key}")
        logger.info(f"当前供应商：{provider_key}")
        provider = model_type_config.providers[provider_key]
        if model_key not in provider.model:
            raise ValueError(f"未知的模型: {model_key}")

        self.current_model_type = model_type
        self.current_provider = provider_key
        self.current_model = model_key

        # 根据不同的 provider 创建不同的客户端
        if provider_key.lower() == 'anthropic':
            self.client = Anthropic(api_key=provider.api_key)
            logger.info(f"已创建 Anthropic 客户端")
        else:
            self.client = OpenAI(api_key=provider.api_key, base_url=provider.api_url)
            logger.info(f"已创建 OpenAI 客户端")

    async def chat_stream(self, message: str, images: Optional[List[str]] = None):
        """流式对话方法

        Args:
            message: 用户输入的文本消息
            images: 可选的图片路径列表。当使用 VLM 类型模型时，可以传入一个或多个图片路径

        Yields:
            Tuple[str, str, str]: (type, content, full_content)
            - type: "reasoning" 或 "content"
            - content: 当前 chunk 的内容
            - full_content: 到目前为止收到的所有内容的合并
        """
        if not all(
            [
                self.current_model_type,
                self.current_provider,
                self.current_model,
                self.client,
            ]
        ):
            raise RuntimeError("未设置模型")

        provider = self.model_types[self.current_model_type].providers[self.current_provider]
        model_config = provider.model[self.current_model]

        # 构建消息历史
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        # 过滤掉消息中的 reasoning_content 字段
        filtered_messages = []
        for msg in self.messages:
            filtered_msg = {k: v for k, v in msg.items() if k != "reasoning_content"}
            filtered_messages.append(filtered_msg)
        
        messages.extend(filtered_messages)

        if self.current_model_type == "vlm":
            content = [{"type": "text", "text": message}]

            if images:
                for image_path in images:
                    if not os.path.exists(image_path):
                        logger.warning(f"图片不存在: {image_path}")
                        continue
                    try:
                        image_type = os.path.splitext(image_path)[1][1:].lower()
                        if image_type not in ["jpg", "jpeg", "png", "gif", "webp"]:
                            image_type = "jpeg"

                        with open(image_path, "rb") as f:
                            import base64

                            image_base64 = base64.b64encode(f.read()).decode("utf-8")
                            content.append(
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{image_type};base64,{image_base64}"
                                    },
                                }
                            )
                    except Exception as e:
                        logger.error(f"读取图片失败 {image_path}: {e}")
                        continue

            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": message})

        try:
            # 保存用户消息到历史记录
            self.messages.append({"role": "user", "content": message})

            # 根据不同的 provider 使用不同的 API
            if self.current_provider.lower() == 'anthropic':
                # 转换消息格式为 Anthropic 格式
                anthropic_messages = []
                
                # 添加历史消息
                for msg in self.messages[:-1]:  # 不包括刚添加的最后一条用户消息
                    if msg["role"] == "user":
                        anthropic_messages.append({"role": "user", "content": msg["content"]})
                    elif msg["role"] == "assistant":
                        anthropic_messages.append({"role": "assistant", "content": msg["content"]})
                
                # 添加当前用户消息
                anthropic_messages.append({"role": "user", "content": message})
                
                # 准备 API 调用参数
                api_params = {
                    "model": self.current_model,
                    "messages": anthropic_messages,
                    "max_tokens": model_config.max_completion_tokens,
                    "stream": True,
                }
                
                # 添加系统提示（正确的方式是作为单独的参数）
                if self.system_prompt:
                    api_params["system"] = self.system_prompt
                
                # 添加温度参数
                if model_config.temperature is not None:
                    api_params["temperature"] = model_config.temperature
                
                # 如果是 reasoning 模型类型，添加 thinking 参数
                if self.current_model_type == "reasoning":
                    api_params["thinking"] = {
                        "type": "enabled",
                        "budget_tokens": min(16000, model_config.max_completion_tokens // 2)  # 默认使用一半的 token 作为 thinking 预算
                    }
                    # 根据 Anthropic API 的要求，当启用 thinking 时，temperature 必须设置为 1
                    api_params["temperature"] = 1.0
                
                # 调用 Anthropic API
                stream = await asyncio.to_thread(
                    self.client.messages.create,
                    **api_params
                )
                
                reasoning_chunks = []
                content_chunks = []
                
                for event in stream:
                    if event.type == "content_block_delta":
                        # 处理思维链输出（thinking）
                        if hasattr(event.delta, "thinking") and event.delta.thinking:
                            current_reasoning = event.delta.thinking
                            reasoning_chunks.append(current_reasoning)
                            yield "reasoning", current_reasoning, "".join(reasoning_chunks)
                        # 处理正常内容输出
                        elif hasattr(event.delta, "text") and event.delta.text:
                            current_chunk = event.delta.text
                            content_chunks.append(current_chunk)
                            yield "content", current_chunk, "".join(content_chunks)
            else:
                # 使用 OpenAI API
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=self.current_model,
                    messages=messages,
                    max_completion_tokens=model_config.max_completion_tokens,
                    **({"temperature": model_config.temperature} if model_config.temperature is not None else {}),
                    stream=True,
                )

                reasoning_chunks = []
                content_chunks = []

                for chunk in response:
                    # 处理推理模型的思维链输出
                    if (
                        hasattr(chunk.choices[0].delta, "reasoning_content")
                        and chunk.choices[0].delta.reasoning_content
                    ):
                        current_reasoning = chunk.choices[0].delta.reasoning_content
                        if current_reasoning:
                            reasoning_chunks.append(current_reasoning)
                            yield "reasoning", current_reasoning, "".join(reasoning_chunks)

                    # 处理内容输出
                    if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                        current_chunk = chunk.choices[0].delta.content
                        if current_chunk:
                            content_chunks.append(current_chunk)
                            yield "content", current_chunk, "".join(content_chunks)

            # 保存完整的助手回复到历史记录
            content = "".join(content_chunks)
            reasoning_content = "".join(reasoning_chunks)
            if content:  # 只有在有内容时才保存助手回复
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                        "reasoning_content": reasoning_content
                        if self.current_model_type == "reasoning"
                        else None,
                    }
                )

        except Exception as e:
            logger.error(f"LLM 请求失败: {e}")

    async def chat(
        self, message: str, images: Optional[List[str]] = None, stream: bool = True
    ) -> Tuple[Optional[str], Optional[str]]:
        """与 LLM 进行对话

        Args:
            message: 用户输入的文本消息
            images: 可选的图片路径列表。当使用 VLM 类型模型时，可以传入一个或多个图片路径
            stream: 是否使用流式输出

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        if stream:
            # 使用流式输出
            reasoning_chunks = []
            content_chunks = []

            try:
                async for chunk_type, chunk, _ in self.chat_stream(message, images):
                    if chunk_type == "reasoning":
                        reasoning_chunks.append(chunk)
                    elif chunk_type == "content":
                        content_chunks.append(chunk)

                return "".join(reasoning_chunks), "".join(content_chunks)
            except Exception as e:
                logger.error(f"流式对话失败: {e}")
                return None, None
        else:
            # 使用非流式输出
            if not all(
                [
                    self.current_model_type,
                    self.current_provider,
                    self.current_model,
                    self.client,
                ]
            ):
                raise RuntimeError("未设置模型")

            provider = self.model_types[self.current_model_type].providers[self.current_provider]
            model_config = provider.model[self.current_model]

            # 构建消息历史
            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})

            # 过滤掉消息中的 reasoning_content 字段
            filtered_messages = []
            for msg in self.messages:
                filtered_msg = {k: v for k, v in msg.items() if k != "reasoning_content"}
                filtered_messages.append(filtered_msg)
            
            messages.extend(filtered_messages)

            if self.current_model_type == "vlm":
                content = [{"type": "text", "text": message}]

                if images:
                    for image_path in images:
                        if not os.path.exists(image_path):
                            logger.warning(f"图片不存在: {image_path}")
                            continue
                        try:
                            image_type = os.path.splitext(image_path)[1][1:].lower()
                            if image_type not in ["jpg", "jpeg", "png", "gif", "webp"]:
                                image_type = "jpeg"

                            with open(image_path, "rb") as f:
                                import base64

                                image_base64 = base64.b64encode(f.read()).decode("utf-8")
                                content.append(
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/{image_type};base64,{image_base64}"
                                        },
                                    }
                                )
                        except Exception as e:
                            logger.error(f"读取图片失败 {image_path}: {e}")
                            continue

                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "user", "content": message})

            try:
                # 保存用户消息到历史记录
                self.messages.append({"role": "user", "content": message})

                # 根据不同的 provider 使用不同的 API
                if self.current_provider.lower() == 'anthropic':
                    # 转换消息格式为 Anthropic 格式
                    anthropic_messages = []
                    
                    # 添加历史消息
                    for msg in self.messages[:-1]:  # 不包括刚添加的最后一条用户消息
                        if msg["role"] == "user":
                            anthropic_messages.append({"role": "user", "content": msg["content"]})
                        elif msg["role"] == "assistant":
                            anthropic_messages.append({"role": "assistant", "content": msg["content"]})
                    
                    # 添加当前用户消息
                    anthropic_messages.append({"role": "user", "content": message})
                    
                    # 准备 API 调用参数
                    api_params = {
                        "model": self.current_model,
                        "messages": anthropic_messages,
                        "max_tokens": model_config.max_completion_tokens,
                    }
                    
                    # 添加系统提示（正确的方式是作为单独的参数）
                    if self.system_prompt:
                        api_params["system"] = self.system_prompt
                    
                    # 添加温度参数
                    if model_config.temperature is not None:
                        api_params["temperature"] = model_config.temperature
                    
                    # 如果是 reasoning 模型类型，添加 thinking 参数
                    if self.current_model_type == "reasoning":
                        api_params["thinking"] = {
                            "type": "enabled",
                            "budget_tokens": min(16000, model_config.max_completion_tokens // 2)  # 默认使用一半的 token 作为 thinking 预算
                        }
                        # 根据 Anthropic API 的要求，当启用 thinking 时，temperature 必须设置为 1
                        api_params["temperature"] = 1.0
                    
                    # 调用 Anthropic API
                    response = await asyncio.to_thread(
                        self.client.messages.create,
                        **api_params
                    )
                    
                    # 从响应中提取内容
                    content = ""
                    reasoning_content = ""
                    
                    # 遍历所有内容块
                    for content_block in response.content:
                        if content_block.type == "text":
                            content = content_block.text
                        elif content_block.type == "thinking":
                            reasoning_content = content_block.thinking
                else:
                    # 使用 OpenAI API
                    response = await asyncio.to_thread(
                        self.client.chat.completions.create,
                        model=self.current_model,
                        messages=messages,
                        max_completion_tokens=model_config.max_completion_tokens,
                        **({"temperature": model_config.temperature} if model_config.temperature is not None else {}),
                        stream=False,
                    )

                    # 从响应中提取内容
                    content = response.choices[0].message.content
                    reasoning_content = getattr(response.choices[0].message, "reasoning_content", None)

                # 保存助手回复到历史记录
                if content:
                    self.messages.append(
                        {
                            "role": "assistant",
                            "content": content,
                            "reasoning_content": reasoning_content
                            if self.current_model_type == "reasoning"
                            else None,
                        }
                    )

                return reasoning_content, content

            except Exception as e:
                logger.error(f"LLM 请求失败: {e}")
                return None, None

    def clear_history(self) -> None:
        """清除对话历史"""
        self.messages = []

    def get_available_histories(self) -> List[Tuple[Path, str, Optional[str]]]:
        """获取可用的对话历史记录

        Returns:
            List[Tuple[Path, str, Optional[str]]]: 返回历史记录列表，每个元素为 (文件路径, 时间戳, 第一条用户消息)
        """
        histories = []
        for file in self.history_dir.glob("chat_*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp", "")
                    messages = data.get("messages", [])
                    first_message = None
                    # 找到第一条用户消息
                    for msg in messages:
                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            # 如果内容是列表（比如包含图片的消息），只取文本部分
                            if isinstance(content, list):
                                for item in content:
                                    if item.get("type") == "text":
                                        first_message = item.get("text", "")
                                        break
                            else:
                                first_message = content
                            break
                    histories.append((file, timestamp, first_message))
            except:
                continue
        return sorted(histories, key=lambda x: x[1], reverse=True)

    def load_chat_history_from_file(
        self, filepath: Union[str, Path]
    ) -> Tuple[bool, Optional[Path]]:
        """从文件加载对话历史

        Args:
            filepath: 历史文件路径

        Returns:
            Tuple[bool, Optional[Path]]: (是否加载成功, 加载的文件路径)
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return False, None

            with open(filepath, "r", encoding="utf-8") as f:
                history = json.load(f)

            self.messages = history.get("messages", [])
            self.system_prompt = history.get("system_prompt")

            return True, filepath

        except Exception as e:
            logger.error(f"加载对话历史失败: {e}")
            return False, None

    def save_chat_history(
        self, filepath: Optional[Union[str, Path]] = None
    ) -> Tuple[bool, Optional[Path]]:
        """保存当前对话历史

        保存时会确保问答成对出现，如果最后有一个孤立的用户问题，会被剔除。
        如果只有一个用户问题没有回答，则不会保存。

        Args:
            filepath: 保存的文件路径，如果不指定则使用默认路径（history_dir/chat_YYYYMMDD_HHMMSS.json）

        Returns:
            Tuple[bool, Optional[Path]]: (是否保存成功, 保存的文件路径)
        """
        try:
            if not self.messages:
                return False, None

            # 确保问答成对，如果最后有一个孤立的用户问题，将其剔除
            messages_to_save = []
            for i in range(0, len(self.messages) - 1, 2):
                if i + 1 < len(self.messages):
                    if (
                        self.messages[i]["role"] == "user"
                        and self.messages[i + 1]["role"] == "assistant"
                    ):
                        messages_to_save.extend([self.messages[i], self.messages[i + 1]])

            # 如果没有成对的问答，则不保存
            if not messages_to_save:
                return False, None

            if not filepath:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = self.history_dir / f"chat_{timestamp}.json"
            else:
                filepath = Path(filepath)

            filepath.parent.mkdir(parents=True, exist_ok=True)

            history = {
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "messages": messages_to_save,
                "system_prompt": self.system_prompt,
                "model_type": self.current_model_type,
                "provider": self.current_provider,
                "model": self.current_model,
                "max_completion_tokens": self.model_types[self.current_model_type]
                .providers[self.current_provider]
                .model[self.current_model]
                .max_completion_tokens
                if all([self.current_model_type, self.current_provider, self.current_model])
                else None,
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True, filepath

        except Exception as e:
            logger.error(f"保存对话历史失败: {e}")
            return False, None

    async def analyze_image(
        self, image_path: str, prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """分析单张图片的便捷方法

        Args:
            image_path: 图片路径
            prompt: 可选的提示词，默认为"描述这张图片"

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        return await self.chat(prompt or "描述这张图片", images=[image_path])

    async def compare_images(
        self, image_paths: List[str], prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """比较多张图片的便捷方法

        Args:
            image_paths: 图片路径列表
            prompt: 可选的提示词，默认为"比较这些图片的异同"

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        return await self.chat(prompt or "比较这些图片的异同", images=image_paths)

    def export_chat_to_markdown(
        self, chat_file: Union[str, Path], output_file: Optional[Union[str, Path]] = None
    ) -> Tuple[bool, Optional[Path]]:
        """将聊天记录转换为 markdown 文档

        Args:
            chat_file: 聊天记录文件路径
            output_file: 输出的 markdown 文件路径，如果不指定则使用 export_dir 下的同名 .md 文件

        Returns:
            Tuple[bool, Optional[Path]]: (是否转换成功, 输出的文件路径)
        """
        try:
            chat_file = Path(chat_file)
            if not chat_file.exists():
                logger.error(f"聊天记录文件不存在: {chat_file}")
                return False, None

            if not output_file:
                output_file = self.export_dir / chat_file.with_suffix(".md").name
            else:
                output_file = Path(output_file)

            # 读取聊天记录
            with open(chat_file, "r", encoding="utf-8") as f:
                chat_data = json.load(f)

            # 生成 markdown 内容
            markdown_lines = []

            # 添加基本信息
            markdown_lines.append("# 对话记录\n")
            markdown_lines.append(f"- 时间: {chat_data.get('timestamp', '未知')}")
            markdown_lines.append(f"- 模型类型: {chat_data.get('model_type', '未知')}")
            markdown_lines.append(f"- 模型提供商: {chat_data.get('provider', '未知')}")
            markdown_lines.append(f"- 模型: {chat_data.get('model', '未知')}\n")
            markdown_lines.append("---\n")

            # 添加对话内容
            for msg in chat_data.get("messages", []):
                role = msg.get("role", "")
                content = msg.get("content", "")
                reasoning = msg.get("reasoning_content")

                if role == "user":
                    markdown_lines.append("# 用户问题")
                    markdown_lines.append(f"{content}\n")
                elif role == "assistant":
                    if reasoning:
                        markdown_lines.append("# AI思考过程")
                        markdown_lines.append(f"{reasoning}\n")
                    markdown_lines.append("# AI回答结果")
                    markdown_lines.append(f"{content}\n")
                    markdown_lines.append("---\n")

            # 写入 markdown 文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(markdown_lines))

            return True, output_file

        except Exception as e:
            logger.error(f"导出 markdown 失败: {e}")
            return False, None
