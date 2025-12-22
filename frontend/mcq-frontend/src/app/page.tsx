"use client";

import Image from "next/image";
import React, { useState, useEffect } from "react";
import { MCQConfig } from "../components/mcq-config";
import { MCQTest } from "../components/mcq-test";
import { generateQuestions, GenerateQuestionsRequest, Question } from "../lib/api";
import { FaGithub, FaLinkedin, FaTwitter } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import { Button } from "../components/ui/button";

export default function HomePage() {
  const [dark, setDark] = useState(true);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

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
        subject: params.subject as "java" | "python" | "sql" | "r" | "linux" | "analytics" | "cassandra" | "mongodb",
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
    //<main className="min-h-screen bg-gray-50 dark:bg-app-dark text-gray-900 dark:text-gray-100 p-6 relative">
    <main className="min-h-screen bg-gray-50 dark:bg-app-dark text-gray-900 dark:text-gray-100 p-6 relative">

    <header className="flex justify-between items-start mb-6">
  {/* left: avatar + Built by */}
  <div className="flex flex-col items-center gap-2">
    <div className="w-14 h-14 rounded-full border border-gray-400/60 overflow-hidden bg-white">
      <Image
        src="/images/me-avatar.png"
        alt="Your avatar"
        width={56}
        height={56}
        className="w-full h-full object-cover"
      />
    </div>

    <div className="text-xs text-black dark:text-gray-300">
      Built by <span className="font-semibold">Kaustubh Kasture</span>
    </div>
  </div>

  {/* right: toggle + icons */}
  <div className="flex items-center gap-4">
    <button
      onClick={() => setDark((d) => !d)}
      className="text-xs px-3 py-1 rounded-full border border-gray-400/50 dark:border-gray-500/60 text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
    >
      {dark ? "Light mode" : "Dark mode"}
    </button>

    <div className="flex gap-3 text-black dark:text-gray-300">
      <a
        href="mailto:kaustubh.kasture10@gmail.com"
        className="hover:text-gray-800 dark:hover:text-white transition"
        aria-label="Email"
      >
        <MdEmail size={22} />
      </a>
      <a
        href="https://x.com/armodrillo1000"
        target="_blank"
        rel="noreferrer"
        className="hover:text-gray-800 dark:hover:text-white transition"
        aria-label="Twitter"
      >
        <FaTwitter size={22} />
      </a>
      <a
        href="https://www.linkedin.com/in/kaustubh-kasture/"
        target="_blank"
        rel="noreferrer"
        className="hover:text-gray-800 dark:hover:text-white transition"
        aria-label="LinkedIn"
      >
        <FaLinkedin size={22} />
      </a>
      <a
        href="https://github.com/KaustubhKasture"
        target="_blank"
        rel="noreferrer"
        className="hover:text-gray-800 dark:hover:text-white transition"
        aria-label="GitHub"
      >
        <FaGithub size={22} />
      </a>
    </div>

  </div>
</header>


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
