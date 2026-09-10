const express = require('express');
const router = express.Router();
const { getOrCreateUser, addSongToUserHistory } = require('../controllers/user');

router.post('/', getOrCreateUser);
router.post('/song', addSongToUserHistory);

module.exports = router;