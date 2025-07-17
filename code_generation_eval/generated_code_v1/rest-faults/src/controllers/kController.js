const prisma = require('../../config/db');

const getK = async (req, res) => {
  try {
    const kValue = await prisma.k.findMany();
    res.json(kValue);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const putK = async (req, res) => {
  try {
    const { i, b, s } = req.body;
    const updatedK = await prisma.k.update({
      where: { id: 1 },
      data: { i, b, s }
    });
    res.json(updatedK);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getK, putK };
