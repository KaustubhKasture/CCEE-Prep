// src/app/page.tsx
"use client";

import React, { useState } from "react";
import { MCQConfig } from "../components/mcq-config";
import { MCQTest } from "../components/mcq-test";
import { generateQuestions, GenerateQuestionsRequest, Question } from "../lib/api";
import { Button } from "../components/ui/button";

export default function HomePage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (params: {
    apiKey: string;
    fallbackApiKey: string;
    fallbackModel: string;
    subject: string;
    difficulty: string;
    numQuestions: number;
  }) => {
    setLoading(true);
    setError(null);
    setQuestions([]);
    try {
      const data: GenerateQuestionsRequest = {
        api_key: params.apiKey.trim(),
        fallback_api_key: params.fallbackApiKey.trim() || undefined,
        fallback_model: params.fallbackModel || undefined,
        subject: params.subject as "java" | "python" | "sql",
        difficulty: params.difficulty as "easy" | "medium" | "hard",
        num_questions: params.numQuestions,
      };
      const response = await generateQuestions(data);
      if (!response.questions || response.questions.length === 0) {
        setError("No questions returned from API.");
      } else {
        setQuestions(response.questions);
      }
    } catch (e: any) {
      setError(e?.message || "Failed to generate questions.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setQuestions([]);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-6">
      <h1 className="text-center text-3xl font-bold mb-8">AI-Powered MCQ Test Platform</h1>
      {questions.length === 0 && (
        <>
          <MCQConfig onGenerate={handleGenerate} loading={loading} />
          {error && (
            <div className="text-red-600 text-center mt-4 font-semibold">{error}</div>
          )}
        </>
      )}
      {questions.length > 0 && <MCQTest questions={questions} onReset={handleReset} />}
    </main>
  );
}
