"""
Think LLM Client
===============

一个灵活的 LLM 和 VLM 模型交互 SDK，支持基础的模型交互和 CLI 界面。

基础用法:
    >>> from think_llm_client import LLMClient
    >>> client = LLMClient()
    >>> client.set_model("llm", "openai", "gpt-4")
    >>> response = await client.chat("Hello!")

CLI 用法:
    >>> from think_llm_client.cli import LLMCLIClient
    >>> client = LLMCLIClient()
    >>> client.set_model("vlm", "openai", "gpt-4-vision")
    >>> response = await client.chat_cli("描述这张图片", images=["image.jpg"])
"""

from .client import LLMClient
from .exceptions import (APIError, ConfigurationError, ModelNotFoundError,
                         ThinkLLMError)

__version__ = "0.1.0"
__all__ = [
    "LLMClient",
    "ThinkLLMError",
    "ConfigurationError",
    "ModelNotFoundError",
    "APIError",
]
