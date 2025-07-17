const express = require('express');
const { getAllStats } = require('../controllers/statController');

const router = express.Router();

router.get('/', getAllStats);

module.exports = router;
