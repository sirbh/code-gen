const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const getGeocode = async (req, res) => {
  try {
    console.log('Fetching geocode data');
    const geocodeData = await prisma.geocode.findMany();
    console.log('Geocode data fetched successfully:', geocodeData);
    res.json(geocodeData);
  } catch (error) {
    console.error('Error fetching geocode data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
};

module.exports = { getGeocode };
