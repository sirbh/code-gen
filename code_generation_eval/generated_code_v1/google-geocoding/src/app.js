const express = require('express');
const geocodeRoutes = require('./routes/geocodeRoutes');
const prisma = require('../config/db');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/maps/api/geocode', geocodeRoutes);

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:' + PORT);
});

module.exports = { app };
