from agents.mcq_agent import generate_questions as base_generate

MONGODB_INSTRUCTION = """
You are an expert in MongoDB and NoSQL document-based database design.

Generate questions ONLY about MongoDB:

Core Concepts
    -Document-oriented database principles.
    -BSON vs JSON.
    -Collections vs documents.
Basic CRUD Operations
    -insertOne, insertMany.
    -find, findOne with filters.
    -updateOne, updateMany, replaceOne.
    -deleteOne, deleteMany.
Querying and Filtering
    -Comparison operators ($eq, $gt, $lt, $in).
    -Logical operators ($and, $or, $not).
    -Projection and sorting.
    -Limit and skip.
Data Modeling
    -Embedded documents vs references.
    -Schema design patterns (one-to-one, one-to-many, many-to-many).
    -Schema flexibility and validation.
Indexes
    -Single-field and compound indexes.
    -Multikey indexes.
    -Text indexes and geospatial indexes.
    -Index performance and explain plans.
Aggregation Framework
    -Aggregation pipeline stages:
        -$match, $group, $project, $sort, $lookup, $unwind.
    -Accumulators ($sum, $avg, $max, $min).
Schema Validation and Constraints
    -JSON Schema validation.
    -Required fields and data types.
Transactions and Consistency
    -Multi-document transactions.
    -Write concerns and read preferences.
    -Atomicity at document level.
Advanced MongoDB Features (Extra MongoDB-Specific Topics)
    -Change streams.
    -TTL indexes.
    -Capped collections.
    -GridFS for large file storage.
Replication and Sharding
    -Replica sets.
    -Sharding concepts (shard key, chunks, balancer).
    -Horizontal scaling strategies.
Performance and Optimization
    -Index optimization.
    -Query planner and explain().
    -Common performance anti-patterns.

Do NOT include questions about SQL databases (MySQL, PostgreSQL), Python, Java, or other programming languages.
Use small MongoDB shell or JSON-style code snippets when useful
"""

async def generate_mongodb_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="Mongodb",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=MONGODB_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_mongodb_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())
