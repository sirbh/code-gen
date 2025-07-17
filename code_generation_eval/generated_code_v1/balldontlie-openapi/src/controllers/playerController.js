const prisma = require('../../config/db');

const getAllPlayers = async (req, res) => {
  try {
    const { search } = req.query;
    const players = await prisma.player.findMany({
      where: {
        name: {
          contains: search,
          mode: 'insensitive'
        }
      }
    });
    res.json(players);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getPlayerById = async (req, res) => {
  try {
    const { playerId } = req.params;
    const player = await prisma.player.findUnique({ where: { id: parseInt(playerId) } });
    if (player) {
      res.json(player);
    } else {
      res.status(404).json({ error: 'Player not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getAllPlayers, getPlayerById };
