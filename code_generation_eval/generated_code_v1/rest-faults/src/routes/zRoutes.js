const express = require('express');
const { getZ, putZ } = require('../controllers/zController');

const router = express.Router();

router.get('/', getZ);
router.put('/', putZ);

module.exports = router;
