"use client";

import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "./ui/select";
import { Slider } from "./ui/slider";

interface MCQConfigProps {
  onGenerate: (params: {
    apiKey: string;
    fallbackApiKey: string;
    fallbackModel: string;
    subject: string;
    difficulty: string;
    numQuestions: number;
  }) => void;
  loading: boolean;
}

const subjects = ["java", "python", "sql", "r", "linux","analytics","cassandra","mongodb"];
const difficulties = ["easy", "medium", "hard"];
const fallbackModels = ["gpt-3.5-turbo", "gpt-4"];

export function MCQConfig({ onGenerate, loading }: MCQConfigProps) {
  const [apiKey, setApiKey] = useState("");
  const [fallbackApiKey, setFallbackApiKey] = useState("");
  const [fallbackModel, setFallbackModel] = useState(fallbackModels[0]);
  const [subject, setSubject] = useState(subjects[0]);
  const [difficulty, setDifficulty] = useState(difficulties[0]);
  const [numQuestions, setNumQuestions] = useState(10);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKey) {
      alert("Please enter your Gemini API key.");
      return;
    }
    onGenerate({ apiKey, fallbackApiKey, fallbackModel, subject, difficulty, numQuestions });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 p-4 max-w-xl mx-auto">
      <div className="flex flex-col space-y-2">
        <Label htmlFor="api_key">Gemini API Key (required)</Label>
        <Input
          id="api_key"
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          required
          placeholder="Enter Gemini API key"
        />
      </div>

      <div className="flex flex-col space-y-2">
        <Label htmlFor="fallback_api_key">OpenAI API Key (Optional)</Label>
        <Input
          id="fallback_api_key"
          type="password"
          value={fallbackApiKey}
          onChange={(e) => setFallbackApiKey(e.target.value)}
          placeholder="Enter OpenAI API key"
        />
      </div>

      <div className="flex flex-col space-y-2">
        <Label htmlFor="fallback_model">Fallback Model (Optional)</Label>
        <Select value={fallbackModel} onValueChange={setFallbackModel}>
          <SelectTrigger id="fallback_model" className="w-full">
            <SelectValue placeholder="Select fallback model" />
          </SelectTrigger>
          <SelectContent>
            {fallbackModels.map((model) => (
              <SelectItem key={model} value={model}>
                {model}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex flex-col space-y-2">
        <Label htmlFor="subject">Subject</Label>
        <Select value={subject} onValueChange={setSubject}>
          <SelectTrigger id="subject" className="w-full">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {subjects.map((s) => (
              <SelectItem key={s} value={s}>
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex flex-col space-y-2">
        <Label>Difficulty</Label>
        <RadioGroup
          value={difficulty}
          onValueChange={(val) => setDifficulty(val)}
          className="flex space-x-6"
        >
          {difficulties.map((level) => (
            <div key={level} className="flex items-center space-x-2">
              <RadioGroupItem value={level} id={`difficulty-${level}`} />
              <Label htmlFor={`difficulty-${level}`}>{level.charAt(0).toUpperCase() + level.slice(1)}</Label>
            </div>
          ))}
        </RadioGroup>
      </div>

      <div className="flex flex-col space-y-2">
        <Label htmlFor="num_questions">Number of Questions: {numQuestions}</Label>
        <Slider
          id="num_questions"
          min={5}
          max={50}
          step={1}
          value={[numQuestions]}
          onValueChange={(val) => setNumQuestions(val[0])}
        />
      </div>

      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Generating..." : "Generate Test"}
      </Button>
    </form>
  );
}
