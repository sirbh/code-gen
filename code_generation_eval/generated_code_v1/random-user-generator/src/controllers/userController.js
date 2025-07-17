const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const getUserData = async (req, res) => {
  try {
    console.log('Fetching random user data');
    const users = await prisma.user.findMany();
    res.json(users);
  } catch (error) {
    console.error('Error fetching user data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getUserData };
