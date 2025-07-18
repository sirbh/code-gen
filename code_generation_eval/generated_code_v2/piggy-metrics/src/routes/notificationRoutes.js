const express = require('express');
const { getNotificationSettings, saveNotificationSettings } = require('../controllers/notificationController');

const router = express.Router();

router.get('/settings/current', getNotificationSettings);
router.put('/settings/current', saveNotificationSettings);

module.exports = router;
