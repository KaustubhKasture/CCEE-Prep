import os
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import Agent as LlmAgent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from litellm import acompletion

if os.getenv('RENDER') is None:
    load_dotenv()

# Retry config
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 502, 503, 504],
)

# Base instruction
BASE_INSTRUCTION = """
You are an expert computer science MCQ generator.

Your job:
- Generate high-quality multiple-choice questions for the requested CS subject.
- Each question must have exactly 4 options: A, B, C, D.
- Exactly ONE option must be correct.
- Explanations must clearly justify the correct answer.

Output format (strict JSON):
{
  "questions": [
    {
      "id": 1,
      "question": "Question text...",
      "options": {
        "A": "Option text",
        "B": "Option text",
        "C": "Option text",
        "D": "Option text"
      },
      "correct_answer": "A",
      "explanation": "Short explanation..."
    }
  ]
}
"""

def build_agent(extra_instruction: str | None = None, api_key: str | None = None) -> LlmAgent:
    """Create a Gemini-based MCQ agent. Optionally extended with subject-specific instructions."""
    instruction = BASE_INSTRUCTION
    if extra_instruction:
        instruction = BASE_INSTRUCTION + "\n\n" + extra_instruction
    return LlmAgent(
        model=Gemini(
            model="gemini-2.5-flash",
            retry_options=retry_config,
            api_key=api_key or os.getenv("GEMINI_API_KEY"),
        ),
        name="mcq_agent",
        instruction=instruction,
    )

async def fallback_generate(
        prompt: str,
        instruction: str,
        fallback_api_key:str,
        fallback_model:str = "gpt-3.5-turbo"
) -> str:
    """LiteLLM fallback when Gemini quota is exhausted."""
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": prompt}
    ]
    response = await acompletion(
        model=fallback_model,
        messages=messages,
        api_key=fallback_api_key
    )
    return response.choices[0].message.content
     

async def generate_questions(
    subject: str,
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo",
    extra_instruction: str | None = None,
) -> str:
    """
    Main function your API/frontend will call.
    Returns the raw text from Gemini (later you will parse JSON from it).
    """
    effective_api_key = api_key or os.getenv("GEMINI_API_KEY")

    if not effective_api_key:
        raise Exception("No Gemini API key provided")
    prompt = (
        f"Generate {num_questions} {difficulty} difficulty MCQ questions on {subject}. "
        "Follow the JSON format described in your instructions."
    )

    instruction = BASE_INSTRUCTION
    if extra_instruction:
        instruction = BASE_INSTRUCTION + "\n\n" + extra_instruction

    #Gemini
    try:
        session_service = InMemorySessionService()
        app_name = "agents"
        user_id = "user1"
        session_id = "mcq_session"

        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )

        agent = build_agent(extra_instruction=extra_instruction, api_key=effective_api_key)
        runner = Runner(agent=agent, app_name=app_name, session_service=session_service)
        content = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )

        final_text = ""
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if (
                hasattr(event, "is_final_response")
                and event.is_final_response()
                and hasattr(event, "content")
                and event.content
            ):
                final_text = event.content.parts[0].text
                break

        return final_text

    #LiteLLM fallback
    except Exception as e:
        if not fallback_api_key:
            raise Exception(f"Gemini failed: {e}. No fallback API key provided.")
        
        print(f"Gemini failed ({e}), falling back to LiteLLM...")
        return await fallback_generate(
            prompt=prompt,
            instruction=instruction,
            fallback_api_key=fallback_api_key,
            fallback_model=fallback_model
        )

# Optional: keep a local test entry point
async def _test():
    text = await generate_questions(
        subject="basic CS topics",
        difficulty="easy",
        num_questions=5,
    )
    print(text)

if __name__ == "__main__" and os.getenv("ENV") == "local":
    asyncio.run(_test())
