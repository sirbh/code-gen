const prisma = require('../../config/db');

const getY = async (req, res) => {
  try {
    const yValue = await prisma.y.findMany();
    res.json(yValue);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const postY = async (req, res) => {
  try {
    const { i, b, s } = req.body;
    const newY = await prisma.y.create({
      data: { i, b, s }
    });
    res.status(201).json(newY);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const deleteY = async (req, res) => {
  try {
    await prisma.y.delete({ where: { id: 1 } });
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getY, postY, deleteY };
