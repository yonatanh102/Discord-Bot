require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');

const userRoutes = require('./routes/user');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// routes:
app.use('/api/users', userRoutes);

// MONGO:
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log('✅ Successfully connected to MongoDB');
        app.listen(PORT, () => {
            console.log(`🚀 Server is running on port ${PORT}`);
        });
    })
    .catch((error) => {
        console.error('❌ Error connecting to MongoDB:', error.message);
    });

module.exports = app;