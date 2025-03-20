import asyncio

from think_llm_client.cli import LLMCLIClient


async def main():
    # 创建 CLI 客户端
    client = LLMCLIClient()

    # 显示可用模型
    models = client.display_available_models()

    # 设置模型
    client.set_model("llm", "openai", "gpt-4")

    # CLI 对话（带格式化输出）
    await client.chat_cli("Python 中的装饰器是什么？")

    # CLI 图片分析（带进度显示）
    await client.analyze_image_cli("examples/images/product.jpg", "分析这个产品的优缺点")

    # CLI 多图片比较（带进度显示）
    await client.compare_images_cli(
        ["examples/images/product1.jpg", "examples/images/product2.jpg"], "比较这两个产品的区别"
    )

    # 显示对话历史
    client.display_chat_history()


if __name__ == "__main__":
    asyncio.run(main())
