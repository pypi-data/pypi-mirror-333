import itertools
import re
import sys
import threading
import time
from datetime import datetime
from typing import List, Optional

from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from .terminal_config import console, TABLE_STYLE


class ThinkingAnimation:
    """思考动画类"""

    def __init__(self):
        self.running = False
        self.thread: threading.Thread | None = None
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.live: Live | None = None

    def _animate(self):
        with Live(console=console, transient=True) as live:
            self.live = live
            for frame in itertools.cycle(self.frames):
                if not self.running:
                    break
                live.update(Text(f"{frame} 思考中...", style="bold cyan"))
                time.sleep(0.1)
            # 清除动画
            live.update(Text(""))

    def start(self):
        """开始动画"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.start()

    def stop(self):
        """停止动画"""
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None


def print_markdown(
    content: str,
    title: str = "✨💖💖💖💖✨",
    show_time: bool = True,
    style: str = "green",
    border_style: str = "green",
) -> bool:
    """使用 rich.markdown 渲染 Markdown 格式的文本

    Args:
        content: Markdown 格式的文本内容
        title: 面板标题，默认为 "✨💖💖💖💖✨"
        show_time: 是否在标题后显示时间，默认为 True
        style: 面板内容的颜色样式，默认为 "green"
        border_style: 面板边框的颜色样式，默认为 "green"

    Returns:
        bool: 是否包含 Markdown 格式
    """
    if not content:
        return False

    try:
        # 移除多余的空行
        content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

        # 定义 Markdown 特征的正则表达式
        MARKDOWN_PATTERNS = [
            r"^\s*#{1,6}\s+.+$",  # 标题
            r"^\s*[-*+]\s+.+$",  # 无序列表
            r"^\s*\d+\.\s+.+$",  # 有序列表
            r"^\s*\|[^|]+\|.+\|$",  # 表格
            r"^\s*```[\s\S]*?```\s*$",  # 代码块
            r"^\s*>\s+.+$",  # 引用
            r"\*\*.+?\*\*",  # 粗体
            r"`[^`]+`",  # 行内代码
            r"\[.+?\]\(.+?\)",  # 链接
        ]

        patterns = [re.compile(pattern, re.MULTILINE)
                    for pattern in MARKDOWN_PATTERNS]
        has_markdown = any(pattern.search(content) for pattern in patterns)

        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            panel_title = f"{title} [{current_time}]" if show_time else title

            # 根据是否包含 Markdown 选择不同的内容渲染方式
            panel_content = Markdown(
                content) if has_markdown else Text(content)

            preview_panel = Panel(
                panel_content,
                title=panel_title,
                style=style,
                border_style=border_style,
                padding=(1, 2),
            )
            console.print("\n")
            console.print(preview_panel)
        except Exception as e:
            # 如果渲染失败，使用普通文本显示
            console.print("\n")
            fallback_panel = Panel(
                Text(content),
                title=f"{panel_title} (渲染失败: {str(e)})",
                style=TABLE_STYLE["error"],
                border_style=TABLE_STYLE["error"],
                padding=(1, 2),
            )
            console.print(fallback_panel)

        return has_markdown

    except Exception as e:
        # 如果发生其他异常，使用普通文本显示
        console.print("\n")
        error_panel = Panel(
            Text(content),
            title=f"{title} (错误: {str(e)})",
            style=TABLE_STYLE["error"],
            border_style=TABLE_STYLE["error"],
            padding=(1, 2),
        )
        console.print(error_panel)
        return False
