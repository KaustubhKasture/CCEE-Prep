// src/lib/api.ts
import axios from "axios";

export interface GenerateQuestionsRequest {
  api_key: string; // Gemini API key (required)
  fallback_api_key?: string; // optional OpenAI API key fallback
  fallback_model?: string; // optional fallback model, e.g. "gpt-3.5-turbo"
  subject: "java" | "python" | "sql" | "r" | "linux" | "analytics" | "cassandra" | "mongodb";
  difficulty: "easy" | "medium" | "hard";
  num_questions: number;
}

export interface Question {
  id: number;
  question: string;
  options: Record<string, string>; // e.g. { A: "foo", B: "bar" }
  correct_answer: string; // e.g. "A"
  explanation: string;
}

export interface GenerateQuestionsResponse {
  subject: string;
  difficulty: string;
  num_questions: number;
  questions: Question[];
}

const API_BASE_URL =  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function generateQuestions(
  data: GenerateQuestionsRequest
): Promise<GenerateQuestionsResponse> {
  const response = await axios.post(`${API_BASE_URL}/api/generate-questions`, data);
  return response.data;
}
