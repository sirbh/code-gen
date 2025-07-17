const express = require('express');
const mailRoutes = require('./routes/mailRoutes');
const prisma = require('../config/db');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());
app.use('/quartz/mail', mailRoutes);

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:' + PORT);
});

module.exports = { app };
