import discord
from settings import token , bot
from cogs.voice_commands import VoiceCommands
from cogs.other_commands import OtherCommands

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await bot.add_cog(VoiceCommands(bot))
    await bot.add_cog(OtherCommands(bot))

bot.run(token)