import os
from agents.mcq_agent import generate_questions as base_generate

JAVA_INSTRUCTION = """
You are an expert in Java programming.

Generate questions ONLY about Java:
- JDK,JVM and JRE
- Data types, Operators, Conditional Statements, Iterative Statements
- Array, String
- Java syntax
- OOP concepts(classes, inheritance, polymorphism, interfaces)
- Constructor, Overloading constructor, array of objects
- this reference, static data, static function, static constructor, static code block
- Packages, accesssing classes from packages, running classes created in package, nested package, package scope, jar files
- Built in packages, math, string, array, date, wrapper classes
- Association, aggregation association, momposition association
- Inheritance, base class, super class, inheritance hierarchy, single inheritance, mutli-level inheritance, hierarchical inheritance, multiple inheritance, hybrid inheritance, protected access specifier, scope of class and obejcts after inehritance
- Polymorphism, compile time polymorphism, run-time polymorphism
- Abstract methods and classes, final variable, final method and class
- Interfaces, Normal Interface, Marker Interface, Functional Interface
- Nested classes, statc class, inner class, anonymous inner class, lambda expression
- Exceptions, generics, collections, streams, File IO
- Collection Framework, MutliThreading, Stream API
- JDBC
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

if __name__ == "__main__" and os.getenv("ENV") == "local":
    asyncio.run(_test())