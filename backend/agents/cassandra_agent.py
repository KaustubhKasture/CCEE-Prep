from agents.mcq_agent import generate_questions as base_generate

CASANDRA_INSTRUCTION = """
You are an expert in Apache Cassandra and CQL (Cassandra Query Language).

Generate questions ONLY about Apache Cassandra:
Core Concepts
    -Cassandra architecture: nodes, clusters, datacenters, racks.
    -CAP theorem, eventual consistency, and tunable consistency.
Basic CQL Syntax
    -SELECT, FROM, WHERE.
    -LIMIT, ORDER BY (with partition key restrictions).
Data Definition (Schema Design)
    -CREATE, ALTER, DROP:
        -Keyspaces (replication strategies: SimpleStrategy, NetworkTopologyStrategy).
        -Tables and user-defined types (UDTs).
    -Table options (clustering order, compaction, compression).
Data Manipulation
    -INSERT, UPDATE, DELETE.
    -TTL (Time To Live) and USING TIMESTAMP.
Data Modeling Concepts
    -Partition keys and clustering columns.
    -Primary key structure (single vs composite keys).
    -Denormalization and query-driven design.
Indexes and Search
    -Secondary indexes.
    -SASI indexes (concepts and use cases).
    -Materialized views (limitations and best practices).
Consistency and Performance
    -Consistency levels (ONE, QUORUM, ALL, LOCAL_QUORUM).
    -Read/write paths and performance trade-offs.
    -Lightweight transactions (LWT) and IF conditions.
Batching and Transactions
    -BATCH statements (logged vs unlogged).
    -Atomicity limitations in Cassandra.
Functions and Advanced Features
    -Built-in CQL functions (UUID, timeuuid, date functions).
    -User-defined functions (UDFs).
    -User-defined aggregates (UDAs).
Operational Topics (Extra Cassandra-Specific Topics)
    -Compaction strategies.
    -Tombstones and their impact.
    -Repair, hinted handoff, and gossip protocol.

Do NOT include questions about SQL databases (MySQL, PostgreSQL), Python, Java, or other programming languages.
Use small CQL code snippets when useful.
"""

async def generate_cassandra_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="Cassandra",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=CASANDRA_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_cassandra_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__":
    asyncio.run(_test())
