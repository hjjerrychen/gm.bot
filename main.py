import os
import discord
import db_utils as dbu
from discord.ext import commands
from auxiliary import top_users
from dotenv import load_dotenv
import sqlite3

con = sqlite3.connect(os.environ['DB_FILE'] or "gm-bot.db")

load_dotenv() 

bot = commands.Bot(command_prefix='', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print('gm - bot has been activated')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'using command too soon. try again in {round(error.retry_after)} seconds')
        await ctx.message.add_reaction('❌')
    else:
        raise error


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=['Gm', 'GM'])
async def gm(ctx):
    user_id, guild_id, discord_name = ctx.author.id, ctx.guild.id, ctx.author.name
    key = str((user_id, guild_id))

    if not dbu.user_exists(key):
        dbu.add_user(key)

    error = dbu.update_user(key)

    if error:
        await ctx.send(f'once per day only. try again tomorrow')
        await ctx.message.add_reaction('❌')
    else:
        await ctx.send(f'thank you for your patronage. your gm count is **{db[key][dbu.Db.COUNT.value]}** and streak is **{db[key][dbu.Db.STREAK.value]}**')
        await ctx.message.add_reaction('✅')


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=['Gmself'])
async def gmself(ctx):
    user_id, guild_id = ctx.author.id, ctx.guild.id
    key = str((user_id, guild_id))

    if not dbu.user_exists(key):
        await ctx.send(f'no record of you saying gm')
        await ctx.message.add_reaction('❌')
    else:
        await ctx.send(f'count: **{db[key][dbu.Db.COUNT.value]}** \nstreak: **{db[key][dbu.Db.STREAK.value]}**')
        await ctx.message.add_reaction('✅')


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=['Gmboard'])
async def gmboard(ctx):
    await ctx.send(embed = await top_users(bot, ctx))
    await ctx.message.add_reaction('✅')


# @bot.command()
# async def force(ctx, *args):
#     if ctx.author.id != 190276271488499713:
#         await ctx.send('no')
#         await ctx.message.add_reaction('❌')
#     else:
#         guild_id, target_id, count, streak = ctx.guild.id, int(args[0]), int(args[1]), int(args[2])
#         key = str((target_id, guild_id))

#         if not dbu.user_exists(key):
#             await ctx.send(f'no key in database for user {target_id} and guild {guild_id}')
#             await ctx.message.add_reaction('❌')
#         else:
#             curr_count, curr_streak, curr_day = db[key]  # grab current values
#             db[key] = [count, streak, curr_day]  # then update
#             await ctx.send(f'updated user successfully')
#             await ctx.message.add_reaction('✅')

bot.run(os.environ['TOKEN'])
