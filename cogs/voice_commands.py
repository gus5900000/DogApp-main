import discord
import asyncio
from discord.ext import commands, tasks
from commands.join import join_random_voice_channel
from commands.leave import leave_voice_channel

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_audio = False
        self.keep_changing_channels = {}
        self.current_sound_file = 'wouaf.wav'  
        self.change_channel_periodically.start()
        self.ignored_channels = set() 


    @tasks.loop(seconds=1)
    async def change_channel_periodically(self):
        for guild_id, should_change in self.keep_changing_channels.items():
            if should_change:
                guild = self.bot.get_guild(guild_id)
                if guild:
                    new_voice_channel = await join_random_voice_channel(guild, self.ignored_channels)
                    if guild.voice_client:
                        # Arrêtez toute musique en cours avant de changer de canal ou de jouer du nouveau son
                        if guild.voice_client.is_playing():
                            guild.voice_client.stop()

                        # Déplacez le client vocal seulement si ce n'est pas le même canal
                        if guild.voice_client.channel != new_voice_channel:
                            await guild.voice_client.move_to(new_voice_channel)

                        # Attendez un moment avant de jouer à nouveau pour éviter des problèmes de synchronisation
                        await asyncio.sleep(1)

                        # Vérifiez si la lecture audio est activée avant de jouer le son
                        if self.play_audio:
                            await self.play_sound(new_voice_channel, self.current_sound_file)
                    else:
                        # Connectez le client vocal s'il n'est pas déjà connecté et jouez le son si autorisé
                        await new_voice_channel.connect()
                        if self.play_audio:
                            await self.play_sound(new_voice_channel, self.current_sound_file)

    @commands.command(name="unignore", help="Enlève un salon vocal de la liste des salons à ignorer.")
    @commands.has_permissions(administrator=True)
    async def unignore_channel(self, ctx, channel_id: int):
        if channel_id in self.ignored_channels:
            self.ignored_channels.remove(channel_id)  
            await ctx.send(f"Salon {channel_id} retiré de la liste des salons à ignorer.")
        else:
            await ctx.send(f"Salon {channel_id} n'est pas dans la liste des salons à ignorer.")

    @commands.command(name="ignore", help="Ajoute un salon vocal à la liste des salons à ignorer.")
    @commands.has_permissions(administrator=True)
    async def ignore_channel(self, ctx, channel_id: int):
        self.ignored_channels.add(channel_id)
        await ctx.send(f"Salon {channel_id} ajouté à la liste des salons à ignorer.")

    @commands.command(name="ronde", help="Permet au chien de faire une ronde.")
    @commands.has_permissions(administrator=True)
    async def join(self, ctx):
        guild_id = ctx.guild.id
        self.keep_changing_channels[guild_id] = True
        voice_channel = await join_random_voice_channel(ctx.guild)
        if voice_channel:
            await self.play_sound(voice_channel, self.current_sound_file)
            await ctx.send("Le chien tourne !")
        else:
            await ctx.send("No voice channel found.")

    @commands.command(name="maison", help="Permets au chien de rentrer à la maison.")
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        guild_id = ctx.guild.id
        self.keep_changing_channels[guild_id] = False
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
        await ctx.send("Le chien est parti !")

    @commands.command(name="aboieon", help="Active la lecture de l'audio.")
    @commands.has_permissions(administrator=True)
    async def aboieon(self, ctx):
        self.play_audio = True
        await ctx.send("Ok j'aboye.")

    @commands.command(name="aboieoff", help="Désactive la lecture de l'audio.")
    @commands.has_permissions(administrator=True)
    async def aboieoff(self, ctx):
        self.play_audio = False
        await ctx.send("Ok j'arrête d'aboyer.")

    @join.error
    @leave.error
    @aboieoff.error
    @aboieon.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("C'est pas toi le maître du chiens.")
        else:
            raise error

    async def play_sound(self, voice_channel, sound_file):
        if voice_channel.guild.voice_client:  # Vérifiez si le client vocal existe
            if voice_channel.guild.voice_client.is_connected():  # Vérifiez si le client vocal est connecté
                source = discord.FFmpegPCMAudio(f'sounds/{sound_file}')
                voice_channel.guild.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            else:
                print("Le bot n'est pas connecté au canal vocal. Tentative de reconnexion...")
                await voice_channel.connect()  # Tentative de reconnexion
                source = discord.FFmpegPCMAudio(f'sounds/{sound_file}')
                voice_channel.guild.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        else:
            print("Le bot n'est pas attaché à un client vocal. Connexion...")
            await voice_channel.connect()  # Connexion si pas déjà connecté
            source = discord.FFmpegPCMAudio(f'sounds/{sound_file}')
            voice_channel.guild.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


    @commands.command(name="play",help="Joue de la musiques")
    async def play(self, ctx, sound_name: str):
        if not ctx.guild.voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                vc = await channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                return
        else:
            vc = ctx.guild.voice_client
        audio_source = discord.FFmpegPCMAudio(f'sounds/{sound_name}.wav')
        if not vc.is_playing():
            vc.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send(f'{sound_name} au platine!')
        else:
            await ctx.send("Son déjà au platine.")

    @commands.command(name="stop",help="Stop la musique.")
    async def stop(self, ctx):
        if ctx.guild.voice_client:
            ctx.guild.voice_client.stop()
            await ctx.send("Son stoppé.")
