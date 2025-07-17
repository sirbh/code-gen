const express = require('express');
const { getK, putK } = require('../controllers/kController');

const router = express.Router();

router.get('/', getK);
router.put('/', putK);

module.exports = router;
