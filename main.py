import os
import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands
from dotenv import load_dotenv

from db import GmBotDb


load_dotenv()
db = GmBotDb(os.environ["DB_FILE"] or "gm-bot.db")
bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


def main():
    bot.run(os.environ["TOKEN"])


@bot.event
async def on_ready():
    print("gm.bot has started")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"using command too soon. try again in {round(error.retry_after)} seconds"
        )
        await ctx.message.add_reaction("❌")
    else:
        raise error


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=["Gm", "GM", "good morning", "Good morning", "Good Morning"])
async def gm(ctx):
    user_id, username, server_id, server_name = (
        str(ctx.author.id),
        str(ctx.author),
        str(ctx.guild.id),
        str(ctx.guild),
    )
    key = user_id + server_id
    streak_record = db.getStreak(key)
    utc = ZoneInfo("UTC")
    eastern = ZoneInfo("America/Toronto")
    now = datetime.now(utc)

    if not streak_record:
        db.newUser(
            (
                key,
                user_id,
                username,
                server_id,
                server_name,
                1,
                now.isoformat(),
                1,
                now.isoformat(),
                1,
                now.isoformat()
            )
        )
        await ctx.send(f"good morning ☀️ your gm count is **1**, current streak is 1 and longest streak is **1**")

        await ctx.message.add_reaction("✅")
        return

    last_gm_date_localized = (
        datetime.fromisoformat(streak_record[1]).astimezone(eastern).date()
    )
    yesterdays_date_localized = (now.astimezone(eastern) - timedelta(1)).date()
    todays_date_localized = now.astimezone(eastern).date()

    current_count = streak_record[0]
    last_gm_on = now.isoformat()
    longest_streak_count = streak_record[2]
    last_longest_streak_on = streak_record[3]
    current_streak_count = streak_record[7]

    if last_gm_date_localized == todays_date_localized:
        await ctx.send(f"once per day only. try again tomorrow")
        await ctx.message.add_reaction("❌")
        return
    elif last_gm_date_localized == yesterdays_date_localized:
        current_streak_count += 1
        current_count += 1
        longest_streak_count = max(current_streak_count, longest_streak_count)
        last_longest_streak_on = (
            now.isoformat()
            if longest_streak_count != streak_record[2]
            else last_longest_streak_on
        )
    else:
        current_streak_count = 1
        current_count += 1

    db.updateUser(
        (
            current_count,
            last_gm_on,
            longest_streak_count,
            last_longest_streak_on,
            username,
            server_name,
            current_streak_count,
            key,
        )
    )
    await ctx.send(
        f"good morning ☀️ your gm count is **{current_count}**, current streak is **{current_streak_count}**, and longest streak is **{longest_streak_count}**"
    )
    await ctx.message.add_reaction("✅")


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=["Gmself"])
async def gmself(ctx):
    key = str(ctx.author.id) + str(ctx.guild.id)
    streak_record = db.getStreak(key)
    eastern = ZoneInfo("America/Toronto")

    if not streak_record:
        await ctx.send(f"no record of you saying gm")
        await ctx.message.add_reaction("❌")
    else:
        await ctx.send(
            f'**Stats for `{str(ctx.author)}`**\nlast gm\'ed on `{datetime.fromisoformat(streak_record[1]).astimezone(eastern).strftime("%Y-%m-%d %I:%M %p")} ET`\ncount: **`{streak_record[0]}`**\ncurrent streak: **`{streak_record[7]}`**\nlongest streak: **`{streak_record[2]}`** set on `{datetime.fromisoformat(streak_record[3]).astimezone(eastern).strftime("%Y-%m-%d %I:%M %p")} ET`\nfirst gm\'ed on `{datetime.fromisoformat(streak_record[6]).astimezone(eastern).strftime("%Y-%m-%d %I:%M %p")} ET`'
        )
        await ctx.message.add_reaction("✅")


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=["Gmboard"])
async def gmboard(ctx):
    top_users = db.getTopUsers(ctx.guild.id)
    top_users_string = "no one gm'ed in this server"
    if top_users:
        top_users_string = "\n".join(
            [f"**`{line[0]}:`** {line[1]} / {line[2]} / {line[3]}" for line in top_users]
        )
    embed = discord.Embed(title="gm.bot leaderboard", color=0x87CEEB)
    embed.add_field(name="User: Count / Current Streak / Longest Streak", value=top_users_string, inline=False)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command(aliases=["Gmhelp"])
async def gmhelp(ctx):
    help_text = """
    **gm.bot help**
    **gm** - records daily gm
    **gmself** - stats about yourself
    **gmboard** - top 10 gm'ers by streak
    **gmhelp** - shows this menu

`Version 7.0-beta3`
<https://github.com/jerry70450/gm.bot>
    """
    await ctx.send(help_text)
    await ctx.message.add_reaction("✅")


if __name__ == "__main__":
    main()
