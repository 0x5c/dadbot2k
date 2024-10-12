"""
DadBot2000
---

Copyright (c) 2021 0x5c
Released under the terms of the BSD 3-Clause Licence
"""


import json
import random
import re
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands

import data.keys as keys
import data.options as opt


intents = discord.Intents.none()
intents.guilds = True
intents.messages = True
intents.message_content = True


bot = commands.Bot(
    command_prefix=opt.command_prefix,
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions().none(),
    member_cache_flags=discord.MemberCacheFlags().none(),
    intents=intents
)


class ChanceManager:
    def __init__(self, path: Path):
        self._path = path / "risk.json"
        self._chance: dict[str, float] = {}
        self.__load()

    def __load(self):
        chancefile = self._path
        if not chancefile.exists():
            with chancefile.open("w") as file:
                json.dump({}, file)
            self._chance = {}
            return
        with chancefile.open("r") as file:
            self._chance = json.load(file)

    def __dump(self):
        with self._path.open("w") as file:
            json.dump(self._chance, file)

    def get(self, guild: Optional[int]) -> float:
        if not guild:
            return opt.default_chance
        return self._chance.get(str(guild), opt.default_chance)

    def set(self, guild: int, value: float):
        if not (0 <= value <= 1):
            raise ValueError("Chance must be a value between 0 and 1")
        self._chance[str(guild)] = value
        self.__dump()


joke_chance = ChanceManager(Path(opt.chance_dir))

joke_prefix = r"(?:i(?:['`´]| a)?|a)m "


@bot.command()  # type: ignore
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())  # type: ignore
@commands.guild_only()
async def chance(ctx: commands.Context, risk: Optional[float]):
    """Sets or display the dadjoking risk."""
    gid = ctx.guild.id
    if risk is None:
        await ctx.send(f"ℹ️  Current risk of dadjoking is `~{joke_chance.get(gid):.2%}`.")
        return
    try:
        joke_chance.set(gid, risk)
        await ctx.send(f"✅  Successfully set the new dadjoking risk to `~{risk:.2%}`.")
    except ValueError as e:
        await ctx.send(f"⚠️  **Error!** {e}.")


@bot.listen("on_message")
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    guild = msg.guild
    nick, gid = (guild.me.nick, guild.id) if guild else (None, None)
    if (m := re.match(joke_prefix, msg.content, flags=re.I)) and random.random() <= joke_chance.get(gid):
        dadname = nick if nick else "Dad!"
        victim_name = msg.content.removeprefix(m.group(0))
        await msg.channel.send(f"Hi {victim_name}, I'm {dadname}")
        if guild:
            print(f"* Gottem! in {guild} [{guild.id}]")
        else:
            print(f"* Gottem in DMs??? {msg.channel} [{msg.channel.id}]")


@bot.event
async def on_ready():
    print(f"> We are {bot.user} {bot.user.id}")


try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    raise SystemExit("ConnectionResetError: {}".format(ex))


# --- Exit ---
# Codes for the wrapper shell script:
# 0 - Clean exit, don't restart
# 1 - Error exit, [restarting is up to the shell script]
# 42 - Clean exit, do restart

raise SystemExit(0)
