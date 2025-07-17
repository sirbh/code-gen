const express = require('express');
const { getX } = require('../controllers/xController');

const router = express.Router();

router.get('/', getX);

module.exports = router;
