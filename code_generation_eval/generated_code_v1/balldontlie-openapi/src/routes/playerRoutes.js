const express = require('express');
const { getAllPlayers, getPlayerById } = require('../controllers/playerController');

const router = express.Router();

router.get('/', getAllPlayers);
router.get('/:playerId', getPlayerById);

module.exports = router;
