import discord , datetime , asyncio
from discord.ext import commands, tasks
from commands.other import clear_messages

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="whoaf",help="Aboie.")
    async def ping(self, ctx):
        await ctx.send("Whoaf Whoaf!")

    @commands.command(name="clear",help="Supprimer x messages.")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, number: int):  
        await clear_messages(ctx, number)
    
    @commands.command(name="help",help="T'es bête t'es dedans.")
    async def help_command(self, ctx):
        embed = discord.Embed(title="Help Spunky", description="Liste des commandes:", color=discord.Color.blue())
        for command in self.bot.commands:
            if not command.hidden:
                embed.add_field(name=command.name, value=command.help or "No description", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="clearbot",help="Clear tout les messages mais uniquement du bot.")
    @commands.has_permissions(administrator=True) 
    async def clearbot(self, ctx):
        limit = 100  
        count = 0 
        for channel in ctx.guild.text_channels:
            try:
                async for message in channel.history(limit=limit):
                    if message.author == self.bot.user:
                        await message.delete()
                        count += 1
            except discord.Forbidden:
                await ctx.send(f"Je n'ai pas la permission de supprimer des messages dans {channel.mention}.")
                continue

        await ctx.send(f"{count} messages du bot ont été supprimés dans tous les canaux.")
    
    @clear.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Tu n'as pas la permission.")
        else:
            raise error