// src/components/mcq-test.tsx
"use client";

import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { Label } from "./ui/label";
import { Question } from "../types/mcq";

interface MCQTestProps {
  questions: Question[];
  onReset: () => void;
}

export function MCQTest({ questions, onReset }: MCQTestProps) {
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const handleAnswerChange = (questionId: number, optionKey: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionKey }));
  };

  const handleSubmit = () => {
    if (Object.keys(answers).length < questions.length) {
      alert("Please answer all questions before submitting.");
      return;
    }
    setSubmitted(true);
  };

  const correctCount = questions.reduce((count, q) => {
    return count + (answers[q.id] === q.correct_answer ? 1 : 0);
  }, 0);

  const scorePercent = (correctCount / questions.length) * 100;

  return (
    <div className="max-w-4xl mx-auto space-y-6 p-6">
      {!submitted ? (
        <>
          {questions.map((q, index) => (
            <Card key={q.id}>
              <CardContent className="p-6">
                <div className="mb-4 font-semibold text-lg">
                  Q{index + 1}:{" "}
                  <ReactMarkdown
                    components={{
                      code({ inline, className, children, ...props }: any) {
                        const match = /language-(\w+)/.exec(className || "");
                        if (!inline && match) {
                          return (
                            <SyntaxHighlighter
                              style={oneDark}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, "")}
                            </SyntaxHighlighter>
                          );
                        }
                        return (
                          <code className={className} {...props}>
                            {children}
                          </code>
                        );
                      },
                    }}
                  >
                    {q.question}
                  </ReactMarkdown>
                </div>
                <RadioGroup
                  value={answers[q.id] || ""}
                  onValueChange={(val) => handleAnswerChange(q.id, val)}
                  className="space-y-2"
                >
                  {Object.entries(q.options).map(([key, text]) => (
                    <div key={key} className="flex items-start space-x-3 p-2 hover:bg-gray-50 rounded-md">
                      <RadioGroupItem 
                        value={key} 
                        id={`q${q.id}-${key}`} 
                        className="mt-1 flex-shrink-0"
                      />
                      <Label htmlFor={`q${q.id}-${key}`} className="cursor-pointer flex-1">
                        <ReactMarkdown
                          components={{
                            code({ inline, className, children, ...props }: any) {
                              const match = /language-(\w+)/.exec(className || "");
                              if (!inline && match) {
                                return (
                                  <SyntaxHighlighter
                                    style={oneDark}
                                    language={match[1]}
                                    PreTag="div"
                                    {...props}
                                  >
                                    {String(children).replace(/\n$/, "")}
                                  </SyntaxHighlighter>
                                );
                              }
                              return (
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              );
                            },
                          }}
                        >
                          {text}
                        </ReactMarkdown>
                      </Label>
                    </div>
                  ))}
                </RadioGroup>
              </CardContent>
            </Card>
          ))}
          <div className="flex justify-center">
            <Button onClick={handleSubmit} className="px-8 py-2 text-lg">
              Submit Answers
            </Button>
          </div>
        </>
      ) : (
        <>
          <Card>
            <CardContent className="p-8 text-center">
              <h2 className="text-3xl font-bold mb-4">Test Results</h2>
              <div className="text-4xl font-bold text-green-600 mb-2">
                {correctCount} / {questions.length}
              </div>
              <div className="text-xl text-gray-600">
                {scorePercent.toFixed(1)}%
              </div>
            </CardContent>
          </Card>

          {questions.map((q, index) => {
            const userAnswer = answers[q.id];
            const isCorrect = userAnswer === q.correct_answer;
            return (
              <Card key={q.id} className={`border-4 ${isCorrect ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50'}`}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="font-semibold text-lg">
                      Q{index + 1}:{" "}
                      <ReactMarkdown
                        components={{
                          code({ inline, className, children, ...props }: any) {
                            const match = /language-(\w+)/.exec(className || "");
                            if (!inline && match) {
                              return (
                                <SyntaxHighlighter
                                  style={oneDark}
                                  language={match[1]}
                                  PreTag="div"
                                  {...props}
                                >
                                  {String(children).replace(/\n$/, "")}
                                </SyntaxHighlighter>
                              );
                            }
                            return (
                              <code className={className} {...props}>
                                {children}
                              </code>
                            );
                          },
                        }}
                      >
                        {q.question}
                      </ReactMarkdown>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-bold ${
                      isCorrect ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                    }`}>
                      {isCorrect ? '✅ Correct' : '❌ Incorrect'}
                    </div>
                  </div>
                  
                  <div className="mb-4 p-3 bg-gray-100 rounded-lg">
                    <strong>Your answer:</strong> <span className="font-mono bg-white px-2 py-1 rounded">{userAnswer}</span>
                    {" "} | <strong>Correct:</strong> <span className="font-mono bg-emerald-100 px-2 py-1 rounded text-emerald-800">{q.correct_answer}</span>
                  </div>

                  <div className="mt-6 pt-4 border-t">
                    <strong className="text-lg block mb-3">Explanation:</strong>
                    <ReactMarkdown
                      components={{
                        code({ inline, className, children, ...props }: any) {
                          const match = /language-(\w+)/.exec(className || "");
                          if (!inline && match) {
                            return (
                              <SyntaxHighlighter
                                style={oneDark}
                                language={match[1]}
                                PreTag="div"
                                {...props}
                              >
                                {String(children).replace(/\n$/, "")}
                              </SyntaxHighlighter>
                            );
                          }
                          return (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        },
                      }}
                    >
                      {q.explanation}
                    </ReactMarkdown>
                  </div>
                </CardContent>
              </Card>
            );
          })}

          <div className="flex justify-center mt-8">
            <Button variant="outline" className="px-8 py-2 text-lg" onClick={onReset}>
              Reset Test
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
