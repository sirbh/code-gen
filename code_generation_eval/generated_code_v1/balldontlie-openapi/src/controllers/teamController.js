const prisma = require('../../config/db');

const getAllTeams = async (req, res) => {
  try {
    const teams = await prisma.team.findMany();
    res.json(teams);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getTeamById = async (req, res) => {
  try {
    const { teamId } = req.params;
    const team = await prisma.team.findUnique({ where: { id: parseInt(teamId) } });
    if (team) {
      res.json(team);
    } else {
      res.status(404).json({ error: 'Team not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getAllTeams, getTeamById };
