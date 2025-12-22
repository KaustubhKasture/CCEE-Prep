from agents.mcq_agent import generate_questions as base_generate

R_INSTRUCTION = """
You are an expert in R programming.
Generate questions ONLY about R:

    -Baisc Questions about R.
    -R Basics : identifier, keywords, variables, operators, data types, data structures, input/output methods.
    -Conditional Statements: if, if-else, if elseif if, switch.
    -Iterative Statements: for, while, repeat, nested loops, loop control statements.
    -Data Objects: vector, list, factor, array, matrices, data frames.
    -Functions: built in functions, numaric function, character functions, statistical funcitons.
    -Packages(tidyverse)
            -Data Wrangling and Transformation: dplyr, tidyr, stringr, forcats
            -Data Import and Management: tibble, readr
            -Functional Programming: purrr
            -Data Visualisation: ggplot2

Do NOT include questions about Python, Java, or other programming languages. Use small shell command snippets when useful.
"""

async def generate_r_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="r",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=R_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_r_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())
