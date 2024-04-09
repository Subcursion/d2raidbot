# This example requires the 'message_content' intent.

import logging
import os
import re
from typing import Literal, Optional

import discord
from discord.ext import commands

from . import converters

handler = logging.FileHandler(
    filename=f"{os.getenv('LOG_FOLDER')}/discord.log", encoding="utf-8", mode="w"
)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.guild_reactions = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.playing, name="Season of the Witch!", state="Dying"
    ),
)

hand_raised_uni = "\U0000270b"
hand_raised = "✋"
question_mark_uni = "\U00002754"
question_mark = "❔"


@bot.event
async def on_ready():
    logger.info("Logged in!")


@bot.hybrid_command(name="newraid", description="Creates a new raid")
async def newRaid(
    ctx: commands.Context, raid: converters.RaidConverter, time: converters.DateTime
):
    embed = discord.Embed(
        color=raid.color, title=raid.name, description=raid.description, timestamp=time
    )
    # embed.set_thumbnail(url=raid.logo_url)
    embed.add_field(
        name="Join us for a Destiny 2 raid!",
        value=(
            "Starting at"
            f" {time.strftime('%I:%M%p %Z %a, %b. %d, %Y')} (<t:{int(time.timestamp())}:R>) 6"
            f" players will attempt the {raid.name} raid!"
        ),
        inline=False,
    )
    embed.add_field(name=":raised_hand: Raiders", value="1.\n2.\n3.\n4.\n5.\n6.")
    embed.add_field(name=":grey_question: Alternates", value="None", inline=True)
    embed.set_image(url=raid.logo_url)
    message = await ctx.send(embed=embed)
    await message.add_reaction(hand_raised_uni)
    await message.add_reaction(question_mark_uni)


@newRaid.error
async def newRaid_error(ctx, error: commands.ConversionError):
    await ctx.send(f"Error: {error.original}", ephemeral=True)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.author != bot.user or payload.user_id == bot.user.id:
        return
    embed = msg.embeds[0]

    if payload.emoji.name == hand_raised:
        # get first field of raiders
        raidersField = embed.fields[1]
        # get raiders
        raidersStr = [
            re.sub(r"^\d\.\s*", "", m) for m in raidersField.value.split("\n")
        ]
        raiders = [m for m in raidersStr if len(m) > 0]
        # just in case this ever happens, check if they are already a member
        if f"<@{payload.user_id}>" in raiders:
            return
        if len(raiders) == 6:
            # full team, remove reaction
            await msg.remove_reaction(payload.emoji, payload.member)
        else:
            # add them to the list
            raiders.append(f"<@{payload.user_id}>")
            valueStr = ""
            for i in range(6):
                valueStr += f'{i+1}. {raiders[i] if i < len(raiders) else ""}\n'
            embed.set_field_at(
                1, name=embed.fields[1].name, value=valueStr, inline=True
            )
            await msg.edit(embed=embed)
            # remove their reaction from alternates
            await msg.remove_reaction(
                question_mark_uni, await bot.fetch_user(payload.user_id)
            )

    if payload.emoji.name == question_mark:
        alternatesField = embed.fields[2]
        alternates = alternatesField.value.split("\n")
        # just in case this ever happens, check if they are already a member
        if f"<@{payload.user_id}>" in alternates:
            return
        if "".join(alternates) == "None":
            alternates = []
        alternates.append(f"<@{payload.user_id}>")
        embed.set_field_at(
            2, name=embed.fields[2].name, value="\n".join(alternates), inline=True
        )
        await msg.edit(embed=embed)
        # remove from raiders
        await msg.remove_reaction(
            hand_raised_uni, await bot.fetch_user(payload.user_id)
        )


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.author != bot.user:
        return

    reaction = discord.utils.get(msg.reactions, emoji=payload.emoji.name)
    if payload.emoji.name == hand_raised:
        if reaction is None:
            await msg.add_reaction(hand_raised_uni)
        else:
            # remove user from raiders
            embed = msg.embeds[0]
            embedField = embed.fields[1]
            raidersStr = [
                re.sub(r"^\d\.\s*", "", m) for m in embedField.value.split("\n")
            ]
            members = [m for m in raidersStr if len(m) > 0]
            members.remove(f"<@{payload.user_id}>")
            valueStr = ""
            for i in range(6):
                valueStr += f'{i+1}. {members[i] if i < len(members) else ""}\n'
            embed.set_field_at(
                1, name=embed.fields[1].name, value=valueStr, inline=True
            )
            await msg.edit(embed=embed)

    if payload.emoji.name == question_mark:
        if reaction is None:
            await msg.add_reaction(question_mark_uni)
        else:
            # remove user from alternates
            embed = msg.embeds[0]
            embedField = embed.fields[2]
            members = [m for m in embedField.value.split("\n") if len(m) > 0]
            members.remove(f"<@{payload.user_id}>")
            if len(members) == 0:
                members = ["None"]
            embed.set_field_at(
                2, name=embed.fields[2].name, value="\n".join(members), inline=True
            )
            await msg.edit(embed=embed)


@bot.event
async def on_raw_reaction_clear(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.author != bot.user:
        return
    # add ours back on and clear the raiders/alternates
    embed = msg.embeds[0]
    raidersField = embed.fields[1]
    alternatesField = embed.fields[2]
    embed.set_field_at(
        1,
        name=raidersField.name,
        value="\n".join([f"{i}." for i in range(1, 7)]),
        inline=True,
    )
    embed.set_field_at(2, name=alternatesField.name, value="None", inline=True)
    await msg.edit(embed=embed)
    await msg.add_reaction(hand_raised_uni)
    await msg.add_reaction(question_mark_uni)


@bot.event
async def on_raw_reaction_clear_emoji(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.author != bot.user or (
        payload.emoji.name != hand_raised and payload.emoji.name != question_mark
    ):
        return
    # add ours back on and clear the raiders/alternates
    embed = msg.embeds[0]
    raidersField = embed.fields[1]
    alternatesField = embed.fields[2]
    if payload.emoji.name == hand_raised:
        embed.set_field_at(
            1,
            name=raidersField.name,
            value="\n".join([f"{i}." for i in range(1, 7)]),
            inline=True,
        )
    if payload.emoji.name == question_mark:
        embed.set_field_at(2, name=alternatesField.name, value="None", inline=True)
    await msg.edit(embed=embed)
    await msg.add_reaction(hand_raised_uni)
    await msg.add_reaction(question_mark_uni)


@bot.hybrid_command(name="editraid", description="Edits a new raid")
async def editRaid(
    ctx: commands.Context,
    msg: discord.Message,
    raid: converters.RaidConverter,
    time: converters.DateTime,
):
    embed = msg.embeds[0]
    embed.title = raid.name
    embed.description = raid.description
    embed.set_field_at(
        0,
        name="Join us for a Destiny 2 raid!",
        value=(
            "Starting at"
            f" {time.strftime('%I:%M%p %Z %a, %b. %d, %Y')} (<t:{int(time.timestamp())}:R>) 6"
            f" players will attempt the {raid.name} raid!"
        ),
        inline=False,
    )
    embed.set_image(url=raid.logo_url)
    embed.color = raid.color
    embed.timestamp = time
    await msg.edit(embed=embed)
    await ctx.send("The raid has been updated!", ephemeral=True)


@editRaid.error
async def editRaid_error(ctx, error):
    await ctx.send(f"Error: {error.original}", ephemeral=True)


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands"
            f" {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
