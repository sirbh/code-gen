const prisma = require('../../config/db');

const getNotificationSettings = async (req, res) => {
  // Placeholder for getting notification settings logic
  res.json({ message: 'Notification settings data' });
};

const saveNotificationSettings = async (req, res) => {
  // Placeholder for saving notification settings logic
  res.json({ message: 'Notification settings saved' });
};

module.exports = { getNotificationSettings, saveNotificationSettings };
