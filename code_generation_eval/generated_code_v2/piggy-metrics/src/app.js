const express = require('express');
const accountRoutes = require('./routes/accountRoutes');
const statisticsRoutes = require('./routes/statisticsRoutes');
const notificationRoutes = require('./routes/notificationRoutes');
const prisma = require('../config/db');

const app = express();
const PORT = process.env.PORT || 8000;

app.use(express.json());
app.use('/accounts', accountRoutes);
app.use('/statistics', statisticsRoutes);
app.use('/notifications', notificationRoutes);

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:' + PORT);
});

module.exports = { app };
