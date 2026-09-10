import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
import aiohttp

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
    'default_search': 'ytsearch'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 48000 -ac 2 -b:a 192k -bufsize 3000k -threads 1'
}

API_BASE_URL = "http://127.0.0.1:3000/api/users"

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    async def check_permissions_and_log(self, user: discord.Member, song: str):
        role_names = [role.name.lower() for role in user.roles]
        if 'music' not in role_names and 'admin' not in role_names:
            return False, "❌ Access denied: You need the 'music' role in this server to request songs."
        try:
            async with aiohttp.ClientSession() as session:
                user_payload = {"discordId": str(user.id), "username": str(user.name)}
                await session.post(f"{API_BASE_URL}/", json=user_payload)
                
                song_payload = {"discordId": str(user.id), "song": song}
                await session.post(f"{API_BASE_URL}/song", json=song_payload)
                
            return True, None
        except Exception as e:
            print(f"API Error (Logging bypassed): {e}")
            return True, None

    async def play_next(self, interaction: discord.Interaction):
        print("--- [DEBUG] 8. Inside play_next ---")
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if self.queue:
            url, title = self.queue.pop(0)
            print(f"--- [DEBUG] 9. Loading audio for: {title} ---")
            try:
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                print("--- [DEBUG] 10. Audio loaded successfully, starting playback ---")
                vc.play(source, after=lambda _: self.bot.loop.create_task(self.play_next(interaction)))
                await interaction.followup.send(f"▶️ Now playing: **{title}**")
            except Exception as e:
                print(f"--- [ERROR] Failed in play_next: {e} ---")
        else:
            await interaction.followup.send("📭 The queue is currently empty.")

    @app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, query: str):
        print("\n--- [DEBUG] 1. Command /play started ---")
        await interaction.response.defer()
        print("--- [DEBUG] 2. Response deferred ---")

        user = interaction.user
        if not isinstance(user, discord.Member):
            return await interaction.followup.send("❌ You need to be in a server to use this command.")

        voice_channel = user.voice.channel if user.voice else None
        if not voice_channel:
            return await interaction.followup.send("❌ You need to join a voice channel first.")

        print("--- [DEBUG] 3. Checking permissions via API... ---")
        is_allowed, error_msg = await self.check_permissions_and_log(user, query)
        print(f"--- [DEBUG] 4. API Response received. Allowed: {is_allowed} ---")
        
        if not is_allowed:
            return await interaction.followup.send(error_msg)
        
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if not vc:
            print("--- [DEBUG] 5. Connecting to voice channel... ---")
            try:
                vc = await voice_channel.connect(timeout=10.0)
                print("--- [DEBUG] 5.5. Connected successfully! ---")
            except Exception as e:
                print(f"--- [ERROR] Connection failed: {repr(e)} ---")
                return await interaction.followup.send(f"❌ Could not connect to the voice channel: {e}")

        def extract_info_sync():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                return ydl.extract_info(f"ytsearch:{query}", download=False)
        
        try:
            print("--- [DEBUG] 6. Extracting YouTube info... ---")
            info = await asyncio.to_thread(extract_info_sync)
            print("--- [DEBUG] 7. YouTube info extracted ---")
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            self.queue.append((url, title))
            await interaction.followup.send(f'🎵 Added to queue: **{title}**')
        except Exception as e:
            print(f"--- [ERROR] Failed to fetch song details: {e} ---")
            return await interaction.followup.send(f"❌ Failed to fetch song details.")

        if not vc.is_playing():
            await self.play_next(interaction)

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if vc and vc.is_playing():
            vc.stop()
            await interaction.followup.send("⏭️ Skipped the current song.")
        else:
            await interaction.followup.send("❌ There is no song currently playing.")

    @app_commands.command(name="pause", description="Pause the current song")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if vc and vc.is_playing():
            vc.pause()
            await interaction.followup.send("⏸️ Paused the music.")
        else:
            await interaction.followup.send("❌ There is no song playing to pause.")

    @app_commands.command(name="resume", description="Resume the paused song")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if vc and vc.is_paused():
            vc.resume()
            await interaction.followup.send("▶️ Resumed the music.")
        else:
            await interaction.followup.send("❌ The music is not paused.")

    @app_commands.command(name="queue", description="Show songs in the queue")
    async def show_queue(self, interaction: discord.Interaction):
        if not self.queue:
            await interaction.response.send_message("📭 The queue is empty.")
            return

        queue_list = "\n".join(f"{i + 1}. {title}" for i, (_, title) in enumerate(self.queue))
        await interaction.response.send_message(f"🎶 Current queue:\n{queue_list}")

    @app_commands.command(name="remove", description="Remove a song from the queue")
    async def remove(self, interaction: discord.Interaction, index: int):
        await interaction.response.defer()
        if 0 < index <= len(self.queue):
            removed = self.queue.pop(index - 1)
            await interaction.followup.send(f"🗑️ Removed **{removed[1]}** from the queue.")
        else:
            await interaction.followup.send("❌ Invalid song number. Please check the queue and try again.")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: discord.VoiceClient = interaction.guild.voice_client  # type: ignore

        if vc:
            self.queue.clear()
            await vc.disconnect()
            await interaction.followup.send("👋 Disconnected from the voice channel and cleared the queue.")
        else:
            await interaction.followup.send("❌ I am not currently in a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))