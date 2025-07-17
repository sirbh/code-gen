const prisma = require('../../config/db');

const getX = async (req, res) => {
  try {
    const xValue = await prisma.x.findMany();
    res.json(xValue);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getX };
