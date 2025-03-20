class ThinkLLMError(Exception):
    """基础异常类"""

    pass


class ConfigurationError(ThinkLLMError):
    """配置错误"""

    pass


class ModelNotFoundError(ThinkLLMError):
    """模型未找到错误"""

    pass


class APIError(ThinkLLMError):
    """API 调用错误"""

    pass
