const express = require("express");

const router = express.Router();

const upload = require("../middleware/uploadMiddleware");
const authMiddleware = require("../middleware/authMiddleware");

const {
  uploadDocument,
  getDocuments,
  deleteDocument,
} = require("../controllers/documentController");

const adminMiddleware = require(
  "../middleware/adminMiddleware"
);

router.post(
  "/upload",
  authMiddleware,
  adminMiddleware,
  upload.single("document"),
  uploadDocument
);

router.get(
  "/",
  authMiddleware,
  getDocuments
);

router.delete(
  "/:id",
  authMiddleware,
  deleteDocument
);

module.exports = router;