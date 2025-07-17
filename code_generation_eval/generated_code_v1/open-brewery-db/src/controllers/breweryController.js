const prisma = require('../../config/db');

const listBreweries = async (req, res) => {
  try {
    const breweries = await prisma.brewery.findMany();
    res.json(breweries);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const getBrewery = async (req, res) => {
  try {
    const { id } = req.params;
    const brewery = await prisma.brewery.findUnique({ where: { id } });
    if (brewery) {
      res.json(brewery);
    } else {
      res.status(404).json({ error: 'Brewery not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const searchBreweries = async (req, res) => {
  try {
    const { query } = req.query;
    const breweries = await prisma.brewery.findMany({
      where: {
        name: {
          contains: query,
          mode: 'insensitive'
        }
      }
    });
    res.json(breweries);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const autocompleteBreweries = async (req, res) => {
  try {
    const { query } = req.query;
    const breweries = await prisma.brewery.findMany({
      where: {
        name: {
          startsWith: query,
          mode: 'insensitive'
        }
      },
      select: { id: true, name: true }
    });
    res.json(breweries);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

const randomBrewery = async (req, res) => {
  try {
    const breweries = await prisma.brewery.findMany();
    const randomIndex = Math.floor(Math.random() * breweries.length);
    res.json(breweries[randomIndex]);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { listBreweries, getBrewery, searchBreweries, autocompleteBreweries, randomBrewery };
