const express = require('express');
const breweryRoutes = require('./routes/breweryRoutes');
const prisma = require('../config/db');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/breweries', breweryRoutes);

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:' + PORT);
});

module.exports = { app };
