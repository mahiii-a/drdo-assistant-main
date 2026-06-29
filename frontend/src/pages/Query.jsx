import { useState } from "react";
import axios from "axios";
import MainLayout from "../layouts/MainLayout";

function Query() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    try {
      setLoading(true);

      const token = localStorage.getItem("token");

      const result = await axios.post(
        "http://localhost:5000/api/query",
        {
          question,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResponse(result.data.answer);

      setLoading(false);
    } catch (error) {
      console.error(error);

      alert("Failed to process query");

      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">
          Ask Query
        </h1>

        <div className="bg-white rounded-xl shadow-md p-6">
          <textarea
            className="w-full border p-3 rounded-lg"
            rows="5"
            placeholder="Enter your question..."
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
          />

          <button
            onClick={handleAsk}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            {loading ? "Generating..." : "Ask"}
          </button>
        </div>

        {response && (
          <div className="mt-6 bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold mb-3">
              Response
            </h2>

            <p>{response}</p>
          </div>
        )}
      </div>
    </MainLayout>
  );
}

export default Query;