from agents.mcq_agent import generate_questions as base_generate

JAVA_INSTRUCTION = """
You are an expert in Java programming.

Generate questions ONLY about Java:
- Java syntax
- OOP (classes, inheritance, polymorphism, interfaces)
- Exceptions, generics, collections, streams
- JVM basics (heap, stack, garbage collection) when relevant

Do NOT include questions about any other language.
Use code snippets in questions where it helps.
"""

async def generate_java_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="Java",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=JAVA_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_java_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,  # uses GEMINI_API_KEY from .env
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())