Campaigner is a project designed to track your progress in games with friends! 
Concept is simple - you can add new Campaign to your discord server and report your progress as a number of games won/lost

Discord commands:
c!newcampaign [campaign_name] -> creates new campaign assigned to your server
c!report [campaign_name] -> starts report sequence where bot will ask you about number of won and lost games.
c!stats [campaign_name] -> provides you some statistics about your campaign


Campaigner is open source project and isn't currently hosted online - if you want use it on your server feel free to fork project and use it as your local discord bot.


--------------TECHNICAL INFORMATIONS------------------------

1. files:
   commands.py - contains all commands used by campaigner - it is not reccomended to put
   in this file other functionalities than defining command and calling appropriate functions in other files

   data_management.py - campainer uses data stored as .json file. This file provides simple functionalities
   to managing this file for example functions like get_data(), add_campaign(ctx: discordext.commands.Context, name: str),
   add_report(ctx: discordext.commands.Context, report: dict)

   report.py - functionality of c!report command

   statistics.py - functionality of c!stats command. This file contains also plotting operations of statistics in matplotlib

2. Running bot
   if you want to run bot on your local discord bot you have to ad discord bot token as an environmental variable in python
   using "TOKEN" as a name of variable
