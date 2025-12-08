from agents.mcq_agent import generate_questions as base_generate

PYTHON_INSTRUCTION = """
You are an expert in Python programming.

Generate questions ONLY about Python:
- Syntax, indentation
- Lists, tuples, dicts, sets
- Functions, *args/**kwargs, lambdas
- Generators, Constructors, Decorators
- Classes, inheritance, data classes
- List/dict comprehensions, String functions, string manilpulations
- Common standard library features

Do NOT include questions about Java or other languages.
Use small code snippets when useful.
"""

async def generate_python_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="Python",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=PYTHON_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_python_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())
