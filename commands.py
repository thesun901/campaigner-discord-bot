import pycord
import discord
import report as rep
import data_management
import statistics
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
    await statistics.showstats(ctx, campaign_name)




@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)

    if ctx.author.bot:
        return
#this below is connected with wins/loses/draws seqence - I should do separate method for it... yea maybe some day
    if str(ctx.guild.id) in rep.current_servers.keys():
        if str(ctx.message.channel) in rep.current_servers[str(ctx.guild.id)].keys():
            if rep.current_servers[str(ctx.guild.id)][str(ctx.channel)]["mode"] != "start":
                if ctx.message.content.isdigit() and not ctx.author.bot:
                    await rep.sequence(ctx, int(message.content))
                else:
                    await ctx.channel.send(f"Wrong input! Type a number!")
                    rep.current_servers[str(ctx.guild.id)][str(ctx.channel)]['delete'] += 2

    await bot.process_commands(message)


