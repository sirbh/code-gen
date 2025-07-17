const prisma = require('../../config/db');

const getZ = async (req, res) => {
  try {
    const zValue = await prisma.z.findMany();
    res.json(zValue);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const putZ = async (req, res) => {
  try {
    const { value } = req.body;
    const updatedZ = await prisma.z.update({
      where: { id: 1 },
      data: { value }
    });
    res.json(updatedZ);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getZ, putZ };
