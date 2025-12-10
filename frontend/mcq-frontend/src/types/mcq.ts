// src/types/mcq.ts

export interface Question {
  id: number;
  question: string;
  options: Record<string, string>;
  correct_answer: string;
  explanation: string;
}

export interface GeneratedTest {
  subject: string;
  difficulty: string;
  num_questions: number;
  questions: Question[];
}
