import logging
from difflib import get_close_matches
from os import getenv
from pathlib import Path

import DiscordUtils
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv

from src.utils.bindings import AsyncErinDatabase
from src.utils.create_logger import create_logger
from src.utils.ErinCog import ErinCog

# Configure logger
logger = create_logger(name=__file__, level=logging.DEBUG)

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
logger.debug(f"Path to .env file is {env_path}")
assert env_path.exists() and env_path.is_file()
load_dotenv(dotenv_path=env_path)


def load_env_var(var_name: str) -> str:
    logger.debug(f"Loading environment variable {repr(var_name)}")
    var = getenv(var_name)
    if var is None or var == "":
        logger.error(f"Could not find {repr(var_name)} in environment "
                     f"variables!")
        raise ValueError(f"Could not find {repr(var_name)} in environment "
                         f"variables!")
    return var


db_uri = load_env_var("DATABASE_URI")

# Create connection to database
erin_db = AsyncErinDatabase(URI=db_uri)


class Help(ErinCog):
    """
    The help cog
    """

    async def make_error_embed(self, ctx: commands.Context, name: str):
        all_cogs = [c.lower() for c in self.bot.cogs]
        closest = get_close_matches(name.lower(), all_cogs, n=1)
        if len(closest) == 0:
            closest = ""
        else:
            closest = f" - did you mean `{closest[0].title()}`?"
        emb = Embed(
            title="lol, sadphroge \N{PENSIVE FACE}\N{PENSIVE FACE}"
                  "\N{PENSIVE FACE}",
            description=f"ERROR 404 couldn't find `{name}` module{closest}",
            color=0xFF0000,
        )
        return emb

    @commands.cooldown(3, 3, BucketType.user)
    @commands.command(hidden=True)
    async def help(self, ctx: commands.Context, sub_cmd: str = None):
        if "<@" in str(ctx.prefix) and ">" in str(ctx.prefix):
            ctx.prefix = f"@{str(self.bot.user).split('#')[0]} "
        if not sub_cmd:
            embed = Embed(color=ctx.message.author.color,
                          timestamp=ctx.message.created_at)
            embed.set_footer(text=ctx.message.author.display_name,
                             icon_url=ctx.message.author.avatar_url)
            embed.set_author(name=self.bot.user.display_name,
                             icon_url=self.bot.user.avatar_url)
            embed.title = "Commands and modules"
            embed.description = f"Use `{ctx.prefix}help <module>` to gain " \
                                f"more information about that module. " \
                                f"<:Kanna:822144873170731018>\nIf you need " \
                                f"further assistance then join our support " \
                                f"server https://www.discord.gg/F5ey2M5GTg " \
                                f"<:Kanna:822144873170731018>\n "
            embed.set_thumbnail(url=str(ctx.message.guild.icon_url))
            for cog in self.bot.cogs:
                commands = self.bot.get_cog(cog).get_commands()
                hidden_count = 0
                if len(commands) == 0:
                    continue
                for command in commands:
                    if command.hidden:
                        hidden_count += 1
                if hidden_count == len(commands):
                    continue
                embed.add_field(name=f"{cog}",
                                value=self.bot.cogs[cog].__doc__,
                                inline=False)
            commands_desc = ""
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f"{command.name} - {command.help}\n"
            if commands_desc:
                embed.add_field(name="Not belonging to a module",
                                value=commands_desc,
                                inline=False)
            await ctx.message.reply(embed=embed)
            return
        else:
            if sub_cmd.lower() == "nsfw":
                if not ctx.channel.is_nsfw():
                    return await ctx.send("Ehhhh this commands works in NSFW "
                                          "channels only "
                                          "<a:awkwardkid:843361776619618304>")

            def make_embed():
                embed = Embed(color=ctx.message.author.color,
                              timestamp=ctx.message.created_at)
                embed.set_footer(text=ctx.message.author.display_name,
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_author(name=self.bot.user.display_name,
                                 icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=str(ctx.message.guild.icon_url))
                return embed

            for cog in self.bot.cogs:
                if cog.lower() == sub_cmd.lower():
                    threshold = 10
                    commands = self.bot.get_cog(cog).get_commands()
                    command_chunk = [
                        commands[i: i + threshold]
                        for i in range(0, len(commands), threshold)
                    ]
                    i = 0
                    embeds = []
                    for chunk in command_chunk:
                        embed = make_embed()
                        for command in chunk:
                            embed.title = f"{command.cog_name} - Commands"
                            embed.description = self.bot.cogs[cog].__doc__
                            embed.set_footer(text="<> Denotes required "
                                                  "argument. [] Denotes "
                                                  "optional argument")
                            if command.hidden:
                                continue
                            i += 1

                            if len(command.aliases) != 0:
                                aliases = ", ".join(
                                    [alias for alias in command.aliases]
                                )
                            else:
                                aliases = "None"
                            description = command.description or "None"

                            command_list = f"{i}) `{ctx.prefix}" \
                                           f"{command.name}`\n "
                            embed.add_field(
                                inline=False,
                                name=f"{command_list}",
                                value=f"Aliases: **{aliases}**\n"
                                      f"Description: **{description}**\n"
                                      f"Usage: **{ctx.prefix + command.name} "
                                      f"{command.signature}**",
                            )

                        embeds.append(embed)

                    if i == 0:
                        embed = await self.make_error_embed(ctx, sub_cmd)
                        await ctx.send(embed=embed)
                        return
                    if len(embeds) == 1:
                        await ctx.send(embed=embeds[0])
                        return
                    else:
                        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(
                            ctx, remove_reactions=True
                        )
                        paginator.add_reaction(
                            "\N{Black Left-Pointing Double Triangle with Vertical Bar}",
                            "first",
                        )
                        paginator.add_reaction(
                            "\N{Black Left-Pointing Double Triangle}", "back"
                        )
                        paginator.add_reaction("\N{CROSS MARK}", "lock")
                        paginator.add_reaction(
                            "\N{Black Right-Pointing Double Triangle}", "next"
                        )
                        paginator.add_reaction(
                            "\N{Black Right-Pointing Double Triangle with Vertical Bar}",
                            "last",
                        )
                        return await paginator.run(embeds)
            else:
                embed = await self.make_error_embed(ctx, sub_cmd)
                await ctx.message.reply(embed=embed)
                return


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
