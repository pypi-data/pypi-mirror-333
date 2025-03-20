from esycord import *

bot = Bot('!', Intents.all()) #This statement may vary according to your need.

@bot.command
async def ping(ctx):
    await ctx.send('Pong!')

bot.run('') # This function treats '' and None as the same