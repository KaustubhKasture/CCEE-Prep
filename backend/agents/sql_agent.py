from agents.mcq_agent import generate_questions as base_generate

PYTHON_INSTRUCTION = """
You are an expert in MySQL and SQL programming.

Generate questions ONLY about MySQL:
    -Basic Syntax: SELECT, FROM, WHERE, ORDER BY, LIMIT.
    -Data Definition Language (DDL): CREATE, ALTER,TRUNCATE, DROP (tables, databases, indexes).
    -Data Manipulation Language (DML): INSERT, UPDATE, DELETE.
    -Data Types and Constraints: Primary/Foreign keys, NOT NULL, UNIQUE, VARCHAR, INT, DATE.
    -Joins and Relationships: INNER, LEFT, RIGHT, FULL joins, and how relationships are established.
    -Built-in Functions:Number Functions, String Functions, Date Functions, Coversion Functions
    -ALter Clause
    -Aggregation and Grouping: GROUP BY, HAVING, and aggregate functions (COUNT, SUM, AVG, MAX, MIN).
    -Subqueries, Views, Parition by
    -Stored Routines: Stored Procedures and Functions.
    -Triggers and Window Functions

Do NOT include questions about Python, Java, or other programming languages. Use small SQL code snippets when useful.
"""

async def generate_sql_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="SQL",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=PYTHON_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_sql_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())
