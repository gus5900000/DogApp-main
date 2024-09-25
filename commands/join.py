import discord
import asyncio
import random
import nacl


async def join_random_voice_channel(guild, ignored_channels):
        """Joins a random voice channel in the guild."""
        channels = [channel for channel in guild.voice_channels if channel.id not in ignored_channels]
        if channels:
            voice_channel = random.choice(channels)
            if not guild.voice_client:
                vc = await voice_channel.connect()
                print(f"Connected to {voice_channel.name}")
                return voice_channel
            elif guild.voice_client:
                await guild.voice_client.move_to(voice_channel)
                print(f"Moved to {voice_channel.name}")
                return voice_channel
        return None
