# Discord Multi-Purpose Bot & API Architecture

A feature-rich, full-stack Discord bot built with a decoupled architecture: a **Python/discord.py** client and a **Node.js/Express** REST API connected to **MongoDB**. 

This bot provides music playback functionality, meme generation, role management, and interactive utility commands to enhance any Discord server, while securely logging user interactions via a dedicated backend service.

## 🚀 Features

* **Decoupled Architecture:** The Discord bot acts as a client that communicates with an independent Node.js REST API for data persistence.
* **Advanced Music Player:** Stream music directly from YouTube using `yt-dlp` and `FFmpeg`. Includes slash commands for playing, pausing, resuming, skipping, and managing a song queue.
* **Role-Based Access Control (RBAC):** Checks for specific Discord native roles before allowing access to premium features (like music streaming).
* **Automated Welcome Messages:** Greets new users joining the server with randomized, custom welcome messages.
* **Meme Generator:** Fetches random memes via an external API (`meme-api.com`) and sends them to the chat.
* **Server Utility:** 
  * Easy polling system with automated reactions (👍/👎).
  * Direct Messaging (DM) capabilities through the bot.
  * Role assignment commands.
* **Automated Testing:** Backend API is fully tested using `Jest` and `Supertest` with an in-memory MongoDB server.

## 🛠️ Tech Stack

**Bot (Client-Side)**
* **Language:** Python 3
* **Libraries:** `discord.py`, `yt-dlp`, `requests`, `python-dotenv`, `PyNaCl`, `davey`
* **Audio Processing:** `FFmpeg`

**Backend API (Server-Side)**
* **Runtime:** Node.js
* **Framework:** Express.js
* **Database:** MongoDB Atlas & Mongoose
* **Testing:** Jest, Supertest

## ⚙️ Installation & Setup (Local Development)

### 1. Backend API Setup
1. Open a terminal in the `backend` folder and install dependencies:
   
   npm install

2. Create a .env file in the backend directory:

    PORT=3000
    MONGO_URI=your_mongodb_atlas_connection_string

3. Start the API server:

    npm start

### 2. Python Bot Setup
1. Ensure the backend is running.

2. Open a new terminal in the Bot folder and install dependencies:

    pip install discord.py yt-dlp requests python-dotenv PyNaCl davey
    (Note: You also need to install FFmpeg on your system and add it to your system's PATH)

3. Create a .env file in the Bot directory:

    DISCORD_TOKEN=your_bot_token_here
    API_BASE_URL=[http://127.0.0.1:3000/api/users](http://127.0.0.1:3000/api/users)

4. Update welcome_channel_id in cogs/welcome.py with your server's welcome channel ID

5. Run the bot:

    python Bot.py

### 3. ☁️ Deployment (Running 24/7)
Since this project has a decoupled architecture, you need to deploy both the Backend API and the Python Bot.

### Step 1: Deploying the Backend API (Node.js)
The easiest way to host the Express API is via a PaaS (Platform as a Service).

- Push your code to GitHub.

- Create a free account on Render.com or Railway.app.

- Create a new Web Service and connect your GitHub repository.

- Set the Root Directory to backend and the start command to npm start.

- Add your MONGO_URI in the platform's Environment Variables section.

- Once deployed, copy the provided public URL (e.g., https://your-api.onrender.com).

### Step 2: Deploying the Python Bot
The bot requires continuous background execution.

- Create a new Background Worker (Render) or a New Service (Railway).

- Connect the same GitHub repository, but set the Root Directory to Bot.

- Set the start command to python Bot.py.

- In the Environment Variables, add your DISCORD_TOKEN and update the API_BASE_URL to the public URL you got from Step 1 (e.g., API_BASE_URL=https://your-api.onrender.com/api/users).

Note regarding FFmpeg: If deploying to Render, you must add a "Buildpack" for FFmpeg so the server can process audio.

### Alternative (VPS Deployment):
If you have a Linux VPS (like DigitalOcean, AWS EC2, or Linode), you can run both services using pm2 to keep them alive after closing the terminal:

* Start the Backend:
npm install -g pm2
pm2 start server.js --name "DiscordAPI"

* Start the Bot:
pm2 start Bot.py --interpreter python3 --name "PiccoBot"
