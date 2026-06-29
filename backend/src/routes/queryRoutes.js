const express = require("express");

const router = express.Router();

const {
  askQuery,
  getQueryHistory,
} = require("../controllers/queryController");

const authMiddleware =
  require("../middleware/authMiddleware");

router.post(
  "/",
  authMiddleware,
  askQuery
);

router.get(
  "/history",
  authMiddleware,
  getQueryHistory
);

module.exports = router;