const prisma = require('../../config/db');

const getAllGames = async (req, res) => {
  try {
    const { seasons, team_ids } = req.query;
    const games = await prisma.game.findMany({
      where: {
        season: {
          in: seasons
        },
        teamId: {
          in: team_ids.map(id => parseInt(id))
        }
      }
    });
    res.json(games);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getGameById = async (req, res) => {
  try {
    const { gameId } = req.params;
    const game = await prisma.game.findUnique({ where: { id: parseInt(gameId) } });
    if (game) {
      res.json(game);
    } else {
      res.status(404).json({ error: 'Game not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getAllGames, getGameById };
