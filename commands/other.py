import discord
import asyncio

async def clear_messages(ctx, number):
    if number < 1 or number > 99:
        await ctx.send("Choisit un nombre entre 1 et 99.")
        return
    deleted = await ctx.channel.purge(limit=number + 1)
    confirmation = await ctx.send(f"{len(deleted) - 1} messages supprimés.")
    await asyncio.sleep(5)
    await confirmation.delete()