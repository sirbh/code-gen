const express = require('express');
const { getAllTeams, getTeamById } = require('../controllers/teamController');

const router = express.Router();

router.get('/', getAllTeams);
router.get('/:teamId', getTeamById);

module.exports = router;
