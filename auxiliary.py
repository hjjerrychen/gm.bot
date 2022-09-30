import discord
import heapq
from replit import db

async def top_users(bot, ctx):
    guild_users = []
    guild = str(ctx.guild.id)

    for key in db:  # first, get all users that are in this guild
        k = key.split(',')
        user_id, guild_id = k[0][1:], k[1][1:-1]

        if guild == guild_id:
            obj = (db[key][0], db[key][1], int(user_id))  # count, day, user_id
            guild_users.append(obj)
    
    message = ''
    min_heap = []

    for key in guild_users:  # then go through them and find the top users
        heapq.heappush(min_heap, key)

        if len(min_heap) > 10:
            heapq.heappop(min_heap)

    i = len(min_heap)
    while min_heap:
        count, streak, user_id = heapq.heappop(min_heap)
        message = f'{i}. {await bot.fetch_user(user_id)} count {count}, streak {streak}\n' + message
        i -= 1

    embed = discord.Embed(title='gm.bot leaderboard', color=0x87CEEB)
    embed.add_field(name='Users', value=message, inline=False)
    return embed
