const express = require('express');
const { getY, postY, deleteY } = require('../controllers/yController');

const router = express.Router();

router.get('/', getY);
router.post('/', postY);
router.delete('/', deleteY);

module.exports = router;
