const userModel = require('../models/user');

const getOrCreateUser = async (req, res) => {
    console.log("--- [DEBUG NODE] Reached getOrCreateUser ---");
    console.log("Incoming Body:", req.body);
    const { discordId, username } = req.body;

    if(!discordId || !username) {
        return res.status(400).json({ error: 'discordId and username are required'});
    }
    try {
        let user = await userModel.findOne({ discordId });

        // if user do not exist - create new one
        if (!user) {
            user = await userModel.create({ 
                discordId,
                username,
            });
            return res.status(201).json(user);
        }
        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

const addSongToUserHistory = async (req, res) => {
    const { discordId, song } = req.body;

    if (!discordId || !song) {
        return res.status(400).json({ error: 'discordId and song are required' });
    }
    try {
        const user = await userModel.findOneAndUpdate(
            { discordId },
            { $push: { requestedSongs: song } },
            { returnDocument: 'after' }
        );

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

module.exports = {
    getOrCreateUser,
    addSongToUserHistory
};