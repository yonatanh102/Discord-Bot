# Discord Multi-Purpose Bot

A feature-rich Discord bot built with Python and `discord.py`. This bot provides music playback functionality, meme generation, role management, and interactive utility commands to enhance any Discord server.

## 🚀 Features

* **Advanced Music Player:** Stream music directly from YouTube using `yt-dlp` and `FFmpeg`. Includes slash commands for playing, pausing, resuming, skipping, and managing a song queue.
* **Automated Welcome Messages:** Greets new users joining the server with randomized, custom welcome messages.
* **Meme Generator:** Fetches random memes via an external API (`meme-api.com`) and sends them to the chat.
* **Server Utility:** 
  * Easy polling system with automated reactions (👍/👎).
  * Direct Messaging (DM) capabilities through the bot.
  * Role assignment commands.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Libraries:** `discord.py`, `yt-dlp`, `requests`, `python-dotenv`
* **Audio Processing:** `FFmpeg`

## ⚙️ Installation & Setup

1. **Clone the repository:**

   git clone ...
   cd YourRepoName

2. **Install the dependencies:**
    
    Make sure you have Python installed, then run:
    pip install discord.py yt-dlp requests python-dotenv PyNaCl

Note: You also need to install FFmpeg on your system and add it to your system's PATH.

3. **Configure Environment Variables:**

    Create a .env file in the root directory and add your Discord bot token:
    DISCORD_TOKEN=your_bot_token_here

4. **Update Channel IDs:**

    In cogs/welcome.py, update welcome_channel_id with the ID of your server's welcome channel.

5. **Run the bot:**

    python Bot.py