const express = require('express');
const zRoutes = require('./routes/zRoutes');
const kRoutes = require('./routes/kRoutes');
const yRoutes = require('./routes/yRoutes');
const xRoutes = require('./routes/xRoutes');
const prisma = require('../config/db');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());
app.use('/z', zRoutes);
app.use('/k', kRoutes);
app.use('/y', yRoutes);
app.use('/x', xRoutes);

app.listen(PORT, () => {
  console.log('Server is running on http://localhost:' + PORT);
});

module.exports = { app };
