const express = require('express');
const { createMailSchedule, deleteMailSchedule, getMailSchedules, getMailScheduleById, updateMailSchedule } = require('../controllers/mailController');

const router = express.Router();

router.post('/create', createMailSchedule);
router.delete('/delete/:id', deleteMailSchedule);
router.get('/list', getMailSchedules);
router.get('/list/:id', getMailScheduleById);
router.post('/update/:id', updateMailSchedule);

module.exports = router;
