const express = require('express');
const { getAllGames, getGameById } = require('../controllers/gameController');

const router = express.Router();

router.get('/', getAllGames);
router.get('/:gameId', getGameById);

module.exports = router;
