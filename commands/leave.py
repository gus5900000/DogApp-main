import discord
import asyncio

async def leave_voice_channel(guild):
    if guild.voice_client:
        await guild.voice_client.disconnect()
