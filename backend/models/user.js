const mongoose = require ('mongoose');

const userSchema = new mongoose.Schema({
    discordId: { type: String, required: true, unique: true },
    username: { type: String, required: true },
    requestedSongs: [{ type: String }]
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema);