const axios = require("axios");
const pool = require("../config/db");

const askQuery = async (req, res) => {
  try {
    const { question } = req.body;

    // const dummyResponse =
    //   "This is a sample response. RAG integration will be added later.";
    const response=await axios.post("http://localhost:8000/rag/query", {
      question: question
    })

    const dummyResponse=response.data.answer

    const result = await pool.query(
      `
      INSERT INTO chat_history
      (user_id, query, response)
      VALUES ($1, $2, $3)
      RETURNING *
      `,
      [
        req.user.id,
        question,
        dummyResponse,
      ]
    );

    res.status(200).json({
      answer: dummyResponse,
      chat: result.rows[0],
    });

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Query failed",
    });
  }
};

const getQueryHistory = async (req, res) => {
  try {
    const result = await pool.query(
      `
      SELECT *
      FROM chat_history
      WHERE user_id = $1
      ORDER BY created_at DESC
      `,
      [req.user.id]
    );

    res.json(result.rows);

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Failed to fetch history",
    });
  }
};

module.exports = {
  askQuery,
  getQueryHistory,
};