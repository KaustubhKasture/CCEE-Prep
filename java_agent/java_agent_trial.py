import asyncio
from dotenv import load_dotenv
import os
from google.genai import types
from google.adk.agents import Agent as LlmAgent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

load_dotenv()

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 502, 503, 504]
)

root_agent = LlmAgent(
    model=Gemini(
        model='gemini-2.5-flash-lite',
        retry_options=retry_config
    ),
    name="java_mcq_agent",
    instruction="""You are a Java programming expert that generates MCQ questions.

Output MUST be valid JSON in this exact format:
{
  "questions": [
    {
      "id": 1,
      "question": "What is the output of System.out.println(5/2)?",
      "options": {
        "A": "2.5",
        "B": "2",
        "C": "3",
        "D": "Compilation error"
      },
      "correct_answer": "B",
      "explanation": "Integer division in Java truncates the decimal part, so 5/2 = 2, not 2.5"
    }
  ]
}

Rules:
- Generate exactly the number of questions requested
- Each question tests ONE Java concept clearly
- All 4 options must be plausible but only one correct
- Explanation must be educational and concise (1-2 sentences)
- Include code snippets in questions when relevant
"""
)

async def main():
    session_service = InMemorySessionService()
    app_name = "agents"
    user_id = "user1"
    session_id = "java_questions_session"
    
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)
    
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)
    
    content = types.Content(role="user", parts=[types.Part(text="Generate 5 questions to test understanding of basic java topics")])
    
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        if hasattr(event, 'is_final_response') and event.is_final_response() and hasattr(event, 'content') and event.content:
            print(event.content.parts[0].text)
            break

if __name__ == "__main__":
    asyncio.run(main())
