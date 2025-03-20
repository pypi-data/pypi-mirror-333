import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from ..exceptions import ConfigurationError


@dataclass
class ModelConfig:
    max_completion_tokens: int = 8192
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None


@dataclass
class Provider:
    api_key: str
    api_url: str
    model: Dict[str, ModelConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Provider":
        model_configs = {
            name: ModelConfig(**config)
            if isinstance(config, dict)
            else ModelConfig(max_completion_tokens=config)
            for name, config in data.get("model", {}).items()
        }
        return cls(
            api_key=data.get("api_key", ""),
            api_url=data.get("api_url", ""),
            model=model_configs,
        )


@dataclass
class ModelType:
    providers: Dict[str, Provider]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelType":
        providers = {
            name: Provider.from_dict(provider_data)
            for name, provider_data in data.get("providers", {}).items()
        }
        return cls(providers=providers)


class Config:
    """配置管理类"""

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器

        Args:
            config_path: 配置文件路径，如果不指定则使用默认路径
        """
        self.config_path = (
            Path(config_path) if config_path else Path.home() /
            ".think-llm-client" / "config.json"
        )
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            if not self.config_path.exists():
                self._create_default_config()

            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception as e:
            raise ConfigurationError(f"无法加载配置文件: {e}")

    def _create_default_config(self) -> None:
        """创建默认配置文件"""
        default_config = {
            "llm": {
                "providers": {
                    "DeepSeek": {
                        "api_key": "<DEEPSEEK_API_KEY>",
                        "api_url": "https://api.deepseek.com",
                        "model": {
                            "deepseek-chat": {
                                "max_completion_tokens": 8192,
                                "temperature": 0.6
                            }
                        }
                    },
                }
            },
            "reasoning": {
                "providers": {
                    "DeepSeek": {
                        "api_key": "<DEEPSEEK_API_KEY>",
                        "api_url": "https://api.deepseek.com",
                        "model": {
                            "deepseek-reasoner": {
                                "max_completion_tokens": 8192,
                                "temperature": 0.6
                            }
                        }
                    }
                }
            },
        }

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

    def get_model_types(self) -> Dict[str, ModelType]:
        """获取模型类型配置"""
        return {
            type_name: ModelType.from_dict(type_data)
            for type_name, type_data in self.config.items()
        }
