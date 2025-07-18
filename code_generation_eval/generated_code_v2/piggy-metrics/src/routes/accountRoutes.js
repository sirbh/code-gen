const express = require('express');
const { getAccount, getCurrentAccount, saveCurrentAccount, getDemoAccount, registerAccount } = require('../controllers/accountController');

const router = express.Router();

router.get('/:account', getAccount);
router.get('/current', getCurrentAccount);
router.put('/current', saveCurrentAccount);
router.get('/demo', getDemoAccount);
router.post('/', registerAccount);

module.exports = router;
