import discord
import report as rep
import data_management
import statistics as stat
import discord.ext as discordext
from GLOBAL import *
import os
import json


bot = discordext.commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


@bot.command(name="report")
async def report(ctx):
    report_name = str(ctx.message.content).replace("c!report", "").lstrip()
    await rep.report(ctx, report_name)


@bot.command(name="newcampaign")
async def newcampaign(ctx):
    campaign_name = str(ctx.message.content).replace("c!newcampaign", "").lstrip()
    await data_management.add_campaign(ctx, campaign_name)

@bot.command(name="stats")
async def stats(ctx):
    campaign_name = str(ctx.message.content).replace("c!stats", "").lstrip()
    await stat.stats(ctx, campaign_name)




@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)

    if ctx.author.bot:
        return

    if str(ctx.guild.id) in rep.current_servers.keys():
        await rep.check_sequence(ctx)

    if str(ctx.guild.id) in stat.current_servers.keys():
        await stat.check_sequence(ctx)

    await bot.process_commands(message)




