const prisma = require('../../config/db');

const createMailSchedule = async (req, res) => {
  try {
    const { message, scheduledTime, subject, toEmail, username, zoneId } = req.body;
    const newSchedule = await prisma.mailSchedule.create({
      data: { message, scheduledTime, subject, toEmail, username, zoneId }
    });
    res.status(201).json(newSchedule);
  } catch (error) {
    console.error('Error creating mail schedule:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const deleteMailSchedule = async (req, res) => {
  try {
    const { id } = req.params;
    await prisma.mailSchedule.delete({ where: { id } });
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting mail schedule:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getMailSchedules = async (req, res) => {
  try {
    const { username } = req.query;
    const schedules = await prisma.mailSchedule.findMany({ where: { username } });
    res.json(schedules);
  } catch (error) {
    console.error('Error fetching mail schedules:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getMailScheduleById = async (req, res) => {
  try {
    const { id } = req.params;
    const schedule = await prisma.mailSchedule.findUnique({ where: { id } });
    if (schedule) {
      res.json(schedule);
    } else {
      res.status(404).json({ error: 'Mail schedule not found' });
    }
  } catch (error) {
    console.error('Error fetching mail schedule:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const updateMailSchedule = async (req, res) => {
  try {
    const { id } = req.params;
    const { message, scheduledTime, subject, toEmail, username, zoneId } = req.body;
    const updatedSchedule = await prisma.mailSchedule.update({
      where: { id },
      data: { message, scheduledTime, subject, toEmail, username, zoneId }
    });
    res.json(updatedSchedule);
  } catch (error) {
    console.error('Error updating mail schedule:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { createMailSchedule, deleteMailSchedule, getMailSchedules, getMailScheduleById, updateMailSchedule };
