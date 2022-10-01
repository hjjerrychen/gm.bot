"""
current schema

{
    (user_id, guild_id) : [count, streak, last_day]
}
"""

import time
from enum import Enum


class Db(Enum):
    COUNT = 0
    STREAK = 1
    LAST_DAY = 2


def user_exists(key):
    return key in db.keys()


def add_user(key):
    db[key] = [0, 0, 0]


def update_user(key):
    curr_time = round(time.time()) - (3600 * 5)  # GMT to EST, subtract 5 hours
    day_num = curr_time // 86_400  # number of days since epoch; don't have to worry about months rolling over

    if day_num == db[key][Db.LAST_DAY.value]:
        return -1
    else:
        db[key][Db.COUNT.value] += 1  # increment count

        if day_num == db[key][Db.LAST_DAY.value] + 1:  # if today == last_day + 1, increment streak
            db[key][Db.STREAK.value] += 1
        else:
            db[key][Db.STREAK.value] = 1

        db[key][Db.LAST_DAY.value] = day_num  # set new last successful invocation


def migrate(ctx):  # from user : [] -> (user, guild) : []
    current_users = []
    curr_time = round(time.time()) - (3600 * 5)
    day_num = curr_time // 86_400

    for user in db:
        count, streak, last_day = db[user][0], db[user][1], db[user][2]
        current_users.append((user, count, streak, last_day))

    for user in db:
        del db[user]

    for user_id, count, streak, last_day in current_users:
        key = (user_id, str(ctx.guild.id))
        db[key] = [count, streak, day_num]

    for key in db:
        print(f'{key} - {db[key]}')


def wipe():
    for key in db:
        del db[key]
