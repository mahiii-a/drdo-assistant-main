const pool = require("../config/db");

const uploadDocument = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        message: "No file uploaded",
      });
    }

    const result = await pool.query(
      `
      INSERT INTO documents
      (
        filename,
        filetype,
        filepath,
        uploaded_by
      )
      VALUES ($1,$2,$3,$4)
      RETURNING *
      `,
      [
        req.file.originalname,
        req.file.mimetype,
        req.file.path,
        req.user.id,
      ]
    );

    res.status(201).json({
      message: "File uploaded successfully",
      document: result.rows[0],
    });

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Upload failed",
    });
  }
};

const getDocuments = async (req, res) => {
  try {
    const result = await pool.query(
      `
      SELECT *
      FROM documents
      ORDER BY upload_date DESC
      `
    );

    res.status(200).json(result.rows);

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Failed to fetch documents",
    });
  }
};



const fs = require("fs");

const deleteDocument = async (req, res) => {
  try {
    const { id } = req.params;

    const document = await pool.query(
      `
      SELECT *
      FROM documents
      WHERE id = $1
      AND uploaded_by = $2
      `,
      [id, req.user.id]
    );

    if (document.rows.length === 0) {
      return res.status(404).json({
        message: "Document not found",
      });
    }

    const filePath = document.rows[0].filepath;

    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }

    await pool.query(
      `
      DELETE FROM documents
      WHERE id = $1
      `,
      [id]
    );

    res.status(200).json({
      message: "Document deleted successfully",
    });

  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Delete failed",
    });
  }
};

module.exports = {
  uploadDocument,
  getDocuments,
  deleteDocument,
};