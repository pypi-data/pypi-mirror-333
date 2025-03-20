from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from ..client import LLMClient
from ..utils.display import ThinkingAnimation
from ..utils.terminal_config import console, TABLE_STYLE
from ..utils.logger import logging

logger = logging.getLogger("think-llm-client")

class LLMCLIClient(LLMClient):
    """CLI 版本的 LLM 客户端，提供丰富的控制台交互界面

    Examples:
        >>> client = LLMCLIClient()
        >>> client.set_model("llm", "openai", "gpt-4")
        >>> response = await client.chat_cli("Hello!")  # 使用 chat_cli 获得格式化输出
    """

    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)
        self.thinking_animation = ThinkingAnimation()

    def display_available_models(self) -> List[Tuple[str, str, str]]:
        """以表格形式显示所有可用的模型"""
        try:
            models = self.get_available_models()

            if not models:
                console.print("\n没有找到可用的模型", style="warning")
                return []

            table = Table(
                title="✨ 可用的模型列表",
                caption=f"选择一个模型来开始对话（可通过配置文件来添加自己的模型：{self.config_path}）",
                caption_style="dim",
                title_style=TABLE_STYLE["table.title"],
                box=TABLE_STYLE["box"],
                header_style=TABLE_STYLE["table.header"],
                border_style=TABLE_STYLE["table.border"],
                show_lines=TABLE_STYLE["show_lines"],
            )

            table.add_column("序号", justify="right", style="cyan", no_wrap=True)
            table.add_column("模型类型", style="blue")
            table.add_column("供应商", style="green")
            table.add_column("模型", style="yellow")
            table.add_column("最大输出Token", style="magenta", justify="right")
            table.add_column("Temperature", style="magenta", justify="right")

            for i, (model_type, provider, model) in enumerate(models, 1):
                model_config = self.model_types[model_type].providers[provider].model[model]
                table.add_row(
                    str(i),
                    f"[bold]{model_type.upper()}[/bold]",
                    provider,
                    model,
                    str(model_config.max_completion_tokens),
                    str(model_config.temperature if model_config.temperature is not None else "默认"),
                )

            console.print("\n")
            console.print(table)
            console.print("\n")

            return models

        except Exception as e:
            console.print(f"\n加载模型配置失败: {e}", style="error")
            return []

    async def chat_cli(
        self, message: str, images: Optional[List[str]] = None, stream: bool = True
    ) -> Tuple[Optional[str], Optional[str]]:
        """CLI 版本的对话方法，提供丰富的控制台输出

        Args:
            message: 用户输入的文本消息
            images: 可选的图片路径列表
            stream: 是否使用流式输出

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        self.thinking_animation.start()

        # 如果是视觉模型且有图片输入，显示图片信息
        if self.current_model_type == "vlm" and images:
            console.print("\n[bold cyan]正在处理以下图片：[/bold cyan]")
            for image_path in images:
                if os.path.exists(image_path):
                    console.print(f"✓ {image_path}", style="green")
                else:
                    console.print(f"✗ {image_path}", style="red")

        try:
            if stream:
                reasoning_chunks = []
                content_chunks = []
                has_shown_reasoning_title = False
                has_shown_content_title = False

                async for chunk_type, chunk, full_content in super().chat_stream(message, images):
                    if chunk_type == "reasoning":
                        if not has_shown_reasoning_title:
                            self.thinking_animation.stop()
                            current_time = datetime.now().strftime("%H:%M:%S")
                            console.print(f"\n思维链（原始输出）[{current_time}]：", style="bold yellow")
                            has_shown_reasoning_title = True
                        console.print(chunk, end="", style="yellow")
                        reasoning_chunks.append(chunk)

                    elif chunk_type == "content":
                        if not has_shown_content_title:
                            if not has_shown_reasoning_title:  # 如果之前没有显示过思维链标题，需要先停止动画
                                self.thinking_animation.stop()
                            current_time = datetime.now().strftime("%H:%M:%S")
                            console.print(f"\n\n回答（原始输出）[{current_time}]：", style="bold green")
                            has_shown_content_title = True
                        console.print(chunk, end="", style="green")
                        content_chunks.append(chunk)

                # 如果没有任何输出，停止动画
                if not has_shown_reasoning_title and not has_shown_content_title:
                    self.thinking_animation.stop()
                    return None, None

                # 显示格式化的面板
                current_reasoning = "".join(reasoning_chunks)
                current_content = "".join(content_chunks)

                if current_reasoning:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    preview_reasoning_panel = Panel(
                        Markdown(current_reasoning),
                        title=f"🌈 思维链（格式渲染）[{current_time}]",
                        style=TABLE_STYLE["highlight"],
                        border_style=TABLE_STYLE["highlight"],
                        padding=(1, 2),
                    )
                    console.print("\n")
                    console.print(preview_reasoning_panel)

                if current_content:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    preview_content_panel = Panel(
                        Markdown(current_content),
                        title=f"✨ 回答（格式渲染）[{current_time}]",
                        style=TABLE_STYLE["green"],
                        border_style=TABLE_STYLE["green"],
                        padding=(1, 2),
                    )
                    console.print("\n")
                    console.print(preview_content_panel)

                return (
                    current_reasoning if current_reasoning else None,
                    current_content if current_content else None,
                )
            else:
                # 非流式输出
                reasoning_content, content = await super().chat(message, images, stream=False)

                # 如果没有任何输出，停止动画并返回
                if not reasoning_content and not content:
                    self.thinking_animation.stop()
                    return None, None

                # 停止动画
                self.thinking_animation.stop()

                if reasoning_content:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    preview_reasoning_panel = Panel(
                        Markdown(reasoning_content),
                        title=f"✨ 思维链（格式渲染）[{current_time}]",
                        style=TABLE_STYLE["highlight"],
                        border_style=TABLE_STYLE["highlight"],
                        padding=(1, 2),
                    )
                    console.print("\n")
                    console.print(preview_reasoning_panel)

                if content:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    preview_content_panel = Panel(
                        Markdown(content),
                        title=f"🌈 回答（格式渲染）[{current_time}]",
                        style=TABLE_STYLE["green"],
                        border_style=TABLE_STYLE["green"],
                        padding=(1, 2),
                    )
                    console.print("\n")
                    console.print(preview_content_panel)

                return reasoning_content, content

        except Exception as e:
            self.thinking_animation.stop()
            raise e
        finally:
            self.thinking_animation.stop()

    async def analyze_image_cli(
        self, image_path: str, prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """CLI 版本的图片分析方法

        Args:
            image_path: 图片路径
            prompt: 可选的提示词

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        return await self.chat_cli(prompt or "描述这张图片", images=[image_path])

    async def compare_images_cli(
        self, image_paths: List[str], prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """CLI 版本的图片比较方法

        Args:
            image_paths: 图片路径列表
            prompt: 可选的提示词

        Returns:
            Tuple[Optional[str], Optional[str]]: (reasoning_content, content)
        """
        return await self.chat_cli(prompt or "比较这些图片的异同", images=image_paths)

    def display_available_histories(self) -> List[Tuple[Path, str, Optional[str]]]:
        """显示可用的对话历史记录

        Returns:
            List[Tuple[Path, str, Optional[str]]]: 历史记录文件路径、时间戳和第一条用户消息的列表
        """
        histories = self.get_available_histories()

        if not histories:
            console.print("\n没有找到历史对话记录", style=TABLE_STYLE["warning"])
            return []

        table = Table(
            title="📚 历史对话记录",
            caption="选择一个记录来加载历史对话",
            caption_style=TABLE_STYLE["table.row.odd"],
            title_style=TABLE_STYLE["table.title"],
            box=box.ROUNDED,
            header_style=TABLE_STYLE["table.header"],
            border_style=TABLE_STYLE["table.border"],
            show_lines=True,  # 显示横线
        )

        table.add_column("序号", justify="right", style=TABLE_STYLE["cyan"], no_wrap=True)
        table.add_column("时间", style=TABLE_STYLE["blue"])
        table.add_column("文件", style=TABLE_STYLE["green"])
        table.add_column("预览", style=TABLE_STYLE["yellow"], max_width=50)  # 限制消息列宽，避免表格过宽

        for i, (file, timestamp, content) in enumerate(histories, 1):
            # 格式化时间戳
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp

            # 处理消息内容，如果太长则截断
            if content:
                if len(content) > 47:  # 预留3个字符给省略号
                    content = content[:47] + "..."
            else:
                content = "[dim]无内容[/dim]"

            table.add_row(str(i), formatted_time, str(file), content)

        console.print("\n")
        console.print(table)
        console.print("\n")

        return histories

    def display_chat_history(self) -> None:
        """显示当前的对话历史"""
        if not self.messages:
            console.print("\n没有对话历史", style=TABLE_STYLE["warning"])
            return

        console.print("\n[bold cyan]对话历史：[/bold cyan]")
        for msg in self.messages:
            if msg["role"] == "user":
                console.print(f"\n你：{msg['content']}")
            elif msg["role"] == "assistant":
                if msg.get("reasoning_content"):
                    console.print("\n思维链：", style="bold yellow")
                    console.print(
                        Panel(
                            Markdown(msg["reasoning_content"]),
                            style="yellow",
                            border_style="yellow",
                            padding=(1, 2),
                        )
                    )
                console.print("\n回答：", style="bold green")
                console.print(
                    Panel(
                        Markdown(msg["content"]),
                        style="green",
                        border_style="green",
                        padding=(1, 2),
                    )
                )

    def save_chat_history(
        self, filepath: Optional[Union[str, Path]] = None
    ) -> Tuple[bool, Optional[Path]]:
        """保存当前对话历史，带有格式化输出

        Args:
            filepath: 保存的文件路径，如果不指定则使用默认路径

        Returns:
            Tuple[bool, Optional[Path]]: (是否保存成功, 保存的文件路径)
        """
        try:
            success, saved_path = super().save_chat_history(filepath)
            if success:
                console.print(f"\n✓ 对话历史已保存", style="green")
                logger.info("对话历史已保存")
                if saved_path:
                    console.print(f"  保存路径: {saved_path}", style="green")
                    logger.info(f"对话历史保存路径：{saved_path}")
            else:
                console.print(f"\n✗ 保存对话历史失败", style="red")
                logger.error("保存对话历史失败")
            return success, saved_path
        except Exception as e:
            console.print(f"\n✗ 保存对话历史失败: {e}", style="red")
            logger.error(f"保存对话历史失败: {e}")
            return False, None

    def load_chat_history_from_file(
        self, filepath: Union[str, Path]
    ) -> Tuple[bool, Optional[Path]]:
        """从文件加载对话历史，带有格式化输出

        Args:
            filepath: 历史文件路径

        Returns:
            Tuple[bool, Optional[Path]]: (是否加载成功, 加载的文件路径)
        """
        try:
            success, loaded_path = super().load_chat_history_from_file(filepath)
            if success:
                console.print(f"\n✓ 已加载对话历史", style="green")
                logger.info("已加载对话历史")
                if loaded_path:
                    console.print(f"  文件路径: {loaded_path}", style="green")
                    logger.info(f"对话历史加载路径：{loaded_path}")
                self.display_chat_history()
            else:
                console.print(f"\n✗ 加载对话历史失败", style="red")
                logger.error("加载对话历史失败")
            return success, loaded_path
        except Exception as e:
            console.print(f"\n✗ 加载对话历史失败: {e}", style="red")
            logger.error(f"加载对话历史失败: {e}")
            return False, None

    def export_chat_history(
        self, chat_file: Union[str, Path], export_dir: Optional[Union[str, Path]] = None
    ) -> Tuple[bool, Optional[Path]]:
        """导出聊天记录到 markdown 文件

        Args:
            chat_file: 要导出的聊天记录文件路径
            export_dir: 导出目录，如果不指定则使用默认导出目录

        Returns:
            Tuple[bool, Optional[Path]]: (是否导出成功, 导出的文件路径)
        """
        try:
            console.print(f"正在导出聊天记录: {chat_file}", style="blue")
            logger.info(f"正在导出聊天记录：{chat_file}")

            success, output_path = super().export_chat_to_markdown(chat_file, export_dir)

            if success and output_path:
                console.print(f"成功导出到: {output_path}", style="green")
                logger.info(f"成功导出到：{output_path}")
            else:
                console.print("导出失败", style="red")
                logger.error("导出失败")

            return success, output_path

        except Exception as e:
            console.print(f"导出时发生错误: {e}", style="red")
            logger.error(f"导出时发生错误：{e}")
            return False, None
