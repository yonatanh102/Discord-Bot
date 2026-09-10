const request = require('supertest');
const express = require('express');
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const userRoutes = require('../routes/user');

const app = express();
app.use(express.json());
app.use('/api/users', userRoutes);

let mongoServer;

beforeAll(async () => {
    mongoServer = await MongoMemoryServer.create();
    await mongoose.connect(mongoServer.getUri());
});

afterAll(async () => {
    await mongoose.disconnect();
    await mongoServer.stop();
});

afterEach(async () => {
    const collections = mongoose.connection.collections;
    for (const key in collections) {
        await collections[key].deleteMany();
    }
});

describe('User API Endpoints', () => {
    // 1. default true test
    it('should create a new user on POST /api/users', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ discordId: '123', username: 'TestUser' });
        
        expect(res.statusCode).toBe(201);
        expect(res.body.discordId).toBe('123');
        expect(res.body.requestedSongs).toEqual([]);
    });

    // 2. missing discordId 
    it('should return error 400 if discordId is missing on POST /api/users', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ username: 'TestUser' });
        
        expect(res.statusCode).toBe(400);
    });

    // 3. edge case: creating the same user 
    it('should return existing user without duplicating on POST /api/users', async () => {
        // first creation
        await request(app).post('/api/users').send({ discordId: '999', username: 'Original' });
        // trying using same id 
        const res = await request(app).post('/api/users').send({ discordId: '999', username: 'Original' });
        
        expect(res.statusCode).toBe(200);
        expect(res.body.discordId).toBe('999');
    });

    // 4. default true add song test
    it('should add a song to user history on POST /api/users/song', async () => {
        await request(app).post('/api/users').send({ discordId: '456', username: 'MusicFan' });
        
        const res = await request(app)
            .post('/api/users/song')
            .send({ discordId: '456', song: 'Never Gonna Give You Up' });
        
        expect(res.statusCode).toBe(200);
        expect(res.body.requestedSongs).toContain('Never Gonna Give You Up');
    });

    // 5. trying a few add commands
    it('should append multiple songs correctly to the user history', async () => {
        await request(app).post('/api/users').send({ discordId: '777', username: 'DJ' });
        
        await request(app).post('/api/users/song').send({ discordId: '777', song: 'Song 1' });
        const res = await request(app).post('/api/users/song').send({ discordId: '777', song: 'Song 2' });
        
        expect(res.statusCode).toBe(200);
        expect(res.body.requestedSongs.length).toBe(2);
        expect(res.body.requestedSongs[1]).toBe('Song 2');
    });

    // 6. edge case: missing song name
    it('should return error 400 if song name is missing on POST /api/users/song', async () => {
        const res = await request(app)
            .post('/api/users/song')
            .send({ discordId: '456' });
        
        expect(res.statusCode).toBe(400);
    });

    // 7. edge case: add song to ghost user
    it('should handle adding a song to a non-existent user appropriately', async () => {
        const res = await request(app)
            .post('/api/users/song')
            .send({ discordId: '0000', song: 'Ghost Track' });
        
        expect(res.statusCode).toBe(404); 
    });
});