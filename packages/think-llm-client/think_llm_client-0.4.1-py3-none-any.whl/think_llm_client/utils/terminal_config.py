"""终端显示配置模块"""
import os
import platform
import sys
from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from rich.box import ASCII, SIMPLE
from rich import box


def detect_terminal_capabilities():
    """
    检测终端类型和功能支持情况

    Returns:
        tuple: (supports_truecolor: bool, is_dark_background: bool, terminal_type: str)
    """
    system = platform.system().lower()
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    term = os.environ.get("TERM", "").lower()
    colorterm = os.environ.get("COLORTERM", "").lower()

    # 检测终端类型
    if system == "windows":
        if "WT_SESSION" in os.environ:  # Windows Terminal
            terminal_type = "windows_terminal"
        elif term_program == "vscode":  # VS Code 集成终端
            terminal_type = "vscode"
        else:  # 传统的 CMD 或 PowerShell
            terminal_type = "windows_legacy"
    else:  # Unix-like systems
        if term_program in ("iterm.app", "apple_terminal"):
            terminal_type = term_program
        elif "KONSOLE" in os.environ:
            terminal_type = "konsole"
        elif "GNOME_TERMINAL" in os.environ:
            terminal_type = "gnome_terminal"
        elif term.startswith("xterm"):
            terminal_type = "xterm"
        else:
            terminal_type = "unknown"

    # 检测真彩色支持
    supports_truecolor = any([
        terminal_type in ("windows_terminal", "vscode", "iterm.app",
                          "apple_terminal", "konsole", "gnome_terminal"),
        colorterm == "truecolor",
        term.endswith("-24bit"),
        term.endswith("-direct"),
    ])

    # 检测是否为暗色主题
    # Windows Terminal 和 VS Code 有专门的环境变量
    if terminal_type in ("windows_terminal", "vscode"):
        is_dark_background = os.environ.get("WT_PROFILE_BACKGROUND", "").lower() == "dark" or \
            os.environ.get("VSCODE_THEME_KIND", "").lower() == "dark"
    else:
        # 其他终端尝试通过环境变量检测
        is_dark_background = (
            "dark" in os.environ.get("COLORFGBG", "").lower() or
            os.environ.get("BACKGROUND", "").lower() == "dark" or
            term.endswith("-dark")
        )

    return supports_truecolor, is_dark_background, terminal_type


def get_terminal_config() -> tuple[Console, dict]:
    """
    获取终端配置

    根据不同的终端环境返回适当的 Console 实例和样式配置

    Returns:
        tuple: (Console 实例, 表格样式配置字典)
    """
    supports_truecolor, is_dark_background, terminal_type = detect_terminal_capabilities()

    # 根据终端类型和颜色支持选择颜色方案
    if supports_truecolor:
        color_scheme = {
            "info": "bright_blue",
            "warning": "bright_yellow",
            "error": "bright_red",
            "success": "bright_green",
            "table.header": "bold bright_cyan",
            "table.border": "bright_white",
            "table.title": "bold bright_white",
            "table.row.even": "none",
            "table.row.odd": "dim",
            "cyan": "bright_cyan",
            "green": "bright_green",
            "blue": "bright_blue",
            "yellow": "bright_yellow",
            "red": "bright_red",
            "magenta": "bright_magenta",
        }
    else:
        # 对于不支持真彩色的终端（如传统的 CMD），使用基本 ANSI 颜色
        color_scheme = {
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "success": "green",
            "table.header": "bold cyan",
            "table.border": "white",
            "table.title": "bold",
            "table.row.even": "none",
            "table.row.odd": "dim",
            "cyan": "cyan",
            "green": "green",
            "blue": "blue",
            "yellow": "yellow",
            "red": "red",
            "magenta": "magenta",
        }

    # 创建主题
    theme = Theme(color_scheme)

    # 配置 Console
    console = Console(
        color_system="truecolor" if supports_truecolor else "standard",
        theme=theme,
        force_terminal=True,
        # Windows CMD 和 PowerShell 可能需要特殊处理
        legacy_windows=terminal_type == "windows_legacy",
        # 某些终端可能需要调整宽度
        width=None if terminal_type in ("windows_terminal", "vscode") else None
    )

    # 配置表格样式
    table_style = {
        "table.header": "table.header",
        "table.border": "table.border",
        "table.title": "table.title",
        "table.row.even": "table.row.even",
        "table.row.odd": "table.row.odd",
        "error": "error",
        "warning": "warning",
        "info": "info",
        "success": "success",
        "highlight": "yellow",
        "cyan": "cyan",
        "green": "green",
        "blue": "blue",
        "yellow": "yellow",
        "red": "red",
        "magenta": "magenta",
        "box": box.ASCII if terminal_type == "windows_legacy" else box.SIMPLE,
        "show_lines": True,
    }

    return console, table_style


# 导出全局实例
console, TABLE_STYLE = get_terminal_config()
