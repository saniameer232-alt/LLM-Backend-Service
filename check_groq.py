import asyncio
from app.services.llm_service import LLMService


async def test():
    service = LLMService()

    result = await service.generate_response(
        message="Say hello in one short sentence."
    )

    print("Groq Response:")
    print(result)


if __name__ == "__main__":
    asyncio.run(test())