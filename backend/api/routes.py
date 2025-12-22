from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Literal, Dict, Any
import json
import re
from agents.java_agent import generate_java_questions
from agents.python_agent import generate_python_questions
from agents.sql_agent import generate_sql_questions
from agents.r_agent import generate_r_questions
from agents.linux_agent import generate_linux_questions
from agents.analytics import generate_analytics_questions
from agents.cassandra_agent import generate_cassandra_questions
from agents.mongodb_agent import generate_mongodb_questions

router = APIRouter()

class QuestionRequest(BaseModel):
    subject: str
    difficulty: Literal["easy", "medium", "hard"]
    num_questions: int
    api_key: str | None = None
    fallback_api_key: str | None = None
    fallback_model: str = "gpt-3.5-turbo"

    @field_validator("num_questions")
    @classmethod
    def validate_num_questions(cls, v):
        if v < 1 or v > 40:
            raise ValueError("num_questions must be between 1 and 40")
        return v
    
def parse_llm_response(raw: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response robustly."""
    
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass
    
    json_match = re.search(r'``````', raw, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    start = raw.find("{")
    if start != -1:
        depth = 0
        for i, char in enumerate(raw[start:], start):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw[start:i+1])
                    except json.JSONDecodeError:
                        break
    
    raise ValueError("Could not parse valid JSON from LLM response")

@router.post("/generate-questions")
async def generate_questions_api(req:QuestionRequest):
    subject = req.subject.lower().strip()

    if subject == 'java':
        raw = await generate_java_questions(
            difficulty = req.difficulty,
            num_questions = req.num_questions,
            api_key = req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject == 'python':
        raw = await generate_python_questions(
           difficulty = req.difficulty,
            num_questions = req.num_questions,
            api_key = req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("sql", "dbms"):
        raw = await generate_sql_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("r"):
        raw = await generate_r_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("linux"):
        raw = await generate_linux_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("analytics"):
        raw = await generate_analytics_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("cassandra"):
        raw = await generate_cassandra_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    elif subject in ("mongodb"):
        raw = await generate_mongodb_questions(
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            api_key=req.api_key,
            fallback_api_key=req.fallback_api_key,
            fallback_model=req.fallback_model
        )
    else:
        raise HTTPException(status_code=400,detail=f'Unsupported subjects:{req.subject}')
    
    try:
        parsed = parse_llm_response(raw)
        questions = parsed.get("questions", [])
        normalized = {
            "subject": subject,
            "difficulty": req.difficulty,
            "num_questions": req.num_questions,
            "questions": questions,
        }
        return normalized
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {e}")