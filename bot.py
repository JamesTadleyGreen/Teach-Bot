# bot.py
import os
import random
from dotenv import load_dotenv
import discord
import contextlib
import io
import ast

import database_functions as df

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='|')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

def in_channel(channel_id):
    def predicate(ctx):
        return ctx.message.channel.id == 824726238722916390
    return commands.check(predicate)

@bot.command(name='problem', help='Displays the problem of the respective number')
@in_channel('CHANNEL_ID')
async def problem(ctx, number: int):
    problem = df.get_problem_list()['problems'][number-1]
    embedVar = discord.Embed(title=f"Problem: {number}", description=problem['desc'], color=0x00ff00)
    for i, sample_result in enumerate(problem['data']['visible']):
        embedVar.add_field(name=f"Test: {i+1}", value=f"Input: Output\n{sample_result['input']}: {sample_result['output']}", inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name='check', help='Checks your code for a given solution, your solution should look like problem_number|code\n e.g. |check 1|5+5')
async def eval(ctx, *, user_input):
    if message.channel.name == 'submissions':
        number, code = user_input.split('|')
        
        problem = df.get_problem_list()['problems'][int(number)-1]
        
        str_obj = io.StringIO() #Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                sample_value_list = [f'solution({i["input"]})' for i in problem['data']['visible']] + [f'solution({i["input"]})' for i in problem['data']['hidden']]
                vis_list = str(sample_value_list).replace("'", "")
                exec(code + f"\nprint({vis_list})") #! Hacky solution might be a better way
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        user_solutions = ast.literal_eval(str_obj.getvalue())
        string_user_solutions = list(map(str, user_solutions))
        string_solutions = [i["output"] for i in problem['data']['visible']] + [i["output"] for i in problem['data']['hidden']]

        embedVar = discord.Embed(title=f"Problem: {number}", description="Number of tests passed", color=0x00ff00)
        for i, sample_result in enumerate(string_user_solutions):
            embedVar.add_field(name=f"Test: {i+1}", value=f"{':green_heart:' if string_user_solutions[i]==string_solutions[i] else ':heart:'}", inline=False)
        
        await ctx.send(embed=embedVar)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Not a command *mate*.")



bot.run(TOKEN)