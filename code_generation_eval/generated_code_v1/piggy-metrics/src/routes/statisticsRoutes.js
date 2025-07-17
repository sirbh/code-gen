const express = require('express');
const { getStatistics, updateStatistics, getCurrentStatistics, getDemoStatistics } = require('../controllers/statisticsController');

const router = express.Router();

router.get('/:account', getStatistics);
router.put('/:account', updateStatistics);
router.get('/current', getCurrentStatistics);
router.get('/demo', getDemoStatistics);

module.exports = router;
