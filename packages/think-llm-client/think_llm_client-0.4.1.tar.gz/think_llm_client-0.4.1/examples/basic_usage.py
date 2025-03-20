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
    reasoning, response = await client.analyze_image("examples/images/product.jpg", "分析这个产品的优缺点")
    print(f"图片分析：{response}")

    # 多图片比较
    reasoning, response = await client.compare_images(
        ["examples/images/product1.jpg", "examples/images/product2.jpg"], "比较这两个产品的区别"
    )
    print(f"图片比较：{response}")


if __name__ == "__main__":
    asyncio.run(main())
