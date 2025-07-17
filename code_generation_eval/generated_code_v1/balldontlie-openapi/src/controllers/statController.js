const prisma = require('../../config/db');

const getAllStats = async (req, res) => {
  try {
    const { season, player_ids } = req.query;
    const stats = await prisma.stat.findMany({
      where: {
        season: {
          in: season
        },
        playerId: {
          in: player_ids.map(id => parseInt(id))
        }
      }
    });
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getAllStats };
