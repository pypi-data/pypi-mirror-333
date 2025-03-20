import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# 日志文件名格式
LOG_FILE_FORMAT = "app_{}.log"
LOG_DATE_FORMAT = "%Y%m%d"
DEFAULT_PROJECT = "think-llm-client-default"

# 用于跟踪已初始化的日志器
_initialized_loggers = set()


def setup_logger(project_name: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """配置日志系统

    Args:
        project_name: 项目名称，用于区分不同项目的日志。如果为 None，则使用默认值
        log_level: 日志级别，默认为 INFO

    Returns:
        logging.Logger: 配置好的日志器实例
    """
    # 使用项目名或默认名
    project = project_name or DEFAULT_PROJECT
    # if not project.startswith('.'):
    #     project = f".{project}"

    # 获取日志器实例
    logger = logging.getLogger(project)
    
    # 如果该日志器已经初始化过，直接返回
    if project in _initialized_loggers:
        return logger

    # 创建日志目录结构：~/project_name/log/
    log_dir = Path.home() / f".{project}" / "log"
    log_dir.mkdir(parents=True, exist_ok=True)

    # 生成日志文件名（按日期）
    log_file = log_dir / LOG_FILE_FORMAT.format(datetime.now().strftime(LOG_DATE_FORMAT))

    # 配置日志格式
    formatter = logging.Formatter(
        f"%(asctime)s - {project} - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 文件处理器 - 记录所有级别的日志
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)  # 使用相同的日志级别

    # 设置日志器级别    
    logger.setLevel(log_level)
    
    # 如果日志器已经有处理器，先清除它们
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 设置不传播到父日志器
    logger.propagate = False

    # 设置 httpx 日志级别（如果在当前项目中使用）
    if project == "think-llm-client":
        logging.getLogger("httpx").setLevel(logging.WARNING)
        
    # 标记该日志器已经初始化
    _initialized_loggers.add(project)

    return logger


def get_log_file_path(project_name: Optional[str] = None) -> Path:
    """获取当前日志文件的路径

    Args:
        project_name: 项目名称，用于区分不同项目的日志。如果为 None，则使用默认值

    Returns:
        Path: 日志文件路径
    """
    project = project_name or DEFAULT_PROJECT
    if not project.startswith('.'):
        project = f".{project}"
    log_dir = Path.home() / project / "log"
    return log_dir / LOG_FILE_FORMAT.format(datetime.now().strftime(LOG_DATE_FORMAT))
