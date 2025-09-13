'use client';
import { useState, type ChangeEvent } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:5000';

type QuizResponse = {
  result: {
    feedback: string;
    score: number;
    sentiment: 'POSITIVE' | 'NEGATIVE';
  };
};

export default function QuizApp() {
  const [a, setA] = useState(1);
  const [b, setB] = useState(2);
  const [answer, setAnswer] = useState(0);
  const [explanation, setExplanation] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResult('');
    try {
      const encryptedA = a;
      const encryptedB = b;
      const encryptedAnswer = answer;
      const encryptedExplanation = explanation;

      const response = await fetch(`${API_URL}/api/quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          a: encryptedA,
          b: encryptedB,
          user_answer: encryptedAnswer,
          explanation: encryptedExplanation,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: QuizResponse = await response.json();
      setResult(data.result.feedback);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setResult(`Backend connection error! ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-extrabold text-blue-800 mb-4 text-center">
          Secret Quiz Fun!
        </h1>

        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              value={a}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setA(Number(e.target.value) || 0)
              }
              className="border-4 border-gray-700 p-4 rounded-lg font-extrabold text-xl bg-white text-gray-900 focus:ring-4 focus:ring-blue-600 focus:border-transparent"
              placeholder="Number A"
            />

            <input
              type="number"
              value={b}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setB(Number(e.target.value) || 0)
              }
              className="border-4 border-gray-700 p-4 rounded-lg font-extrabold text-xl bg-white text-gray-900 focus:ring-4 focus:ring-blue-600 focus:border-transparent"
              placeholder="Number B"
            />
          </div>

          <p className="text-center text-2xl font-extrabold text-gray-900">
            Calculate {a} + {b} = ?
          </p>

          <input
            type="number"
            value={answer}
            onChange={(e: ChangeEvent<HTMLInputElement>) =>
              setAnswer(Number(e.target.value) || 0)
            }
            className="border-4 border-gray-700 p-4 rounded-lg w-full font-extrabold text-xl bg-white text-gray-900 focus:ring-4 focus:ring-blue-600 focus:border-transparent"
            placeholder="Your Answer"
          />

          <textarea
            value={explanation}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
              setExplanation(e.target.value)
            }
            className="border-4 border-gray-700 p-4 rounded-lg w-full font-extrabold text-xl bg-white text-gray-900 focus:ring-4 focus:ring-blue-600 focus:border-transparent resize-none"
            placeholder="Your Sentiment (e.g., Super cool! or Keep trying...)"
            rows={4}
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-blue-800 text-white p-4 w-full rounded-lg font-extrabold text-xl hover:bg-blue-900 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Processing Secretly...' : 'Submit Quiz & See Result!'}
          </button>
        </div>

        {result && (
          <p className="mt-4 text-2xl font-extrabold text-green-800">{result}</p>
        )}

        <div className="text-sm text-gray-700 text-center mt-4">
          <p>Tech: Zama FHE + Concrete ML (Encrypted ML)</p>
        </div>
      </div>
    </div>
  );
}
