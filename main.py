import discord
from discord.ext import commands
import dotenv
import os
import csv
import random
### get discord token ###
dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')


### global variables ###

parameter_type = None #selected food type
parameter_location = None #selected location

list_type = ['한식', '중식', '일식', '양식', '간식', '기타']
list_location = ['신촌', '홍대', '합정', '마포', '서강']
prefix = '미식봇! '


### setup bot ###
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


### setup data ###

#TODO : integrate with Google Sheets for a more seamless experience,
#       i.e. when you need to update the restaurant database

file_name = os.getenv('DATA')
with open(file_name, mode='r') as file:
    data = list(csv.reader(file, delimiter=','))

######### Select components #########

# food type selection

# TODO
# 1. add functionalit to check for duplicate selections
# 2. improve loop to reduce memory usage (only append indexes instead of entire rows)
def random_select(type : str, location : str):
    candidates = []
    for row in data:
        if (row[1] == type and row[2] == location):
            candidates.append(row)
    num = random.randint(0, len(candidates) - 1)
    return candidates[num]
    

class SelectType(discord.ui.Select):
    def __init__(self):
        options = []
        for type in list_type:
            options.append(discord.SelectOption(label=type, description=type))
        super().__init__(placeholder="음식 분류를 선택해 주세요",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        global parameter_type
        parameter_type = self.values[0]
        await interaction.response.send_message(content=f"{parameter_type}을 선택하셨습니다.")
        if (parameter_type != None and parameter_location != None):
            #print(f"Both parameters entered : {parameter_type} and {parameter_location}") -> currently here for testing purposes
            ans = random_select(parameter_type, parameter_location)
            await interaction.followup.send(ans[0] + ' | ' + ans[6])


#location selection
class SelectLocation(discord.ui.Select):
    def __init__(self):
        options = []
        for location in list_location:
            options.append(discord.SelectOption(label=location, description=location))
        super().__init__(placeholder="식당 위치를 선택해 주세요",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        global parameter_location
        parameter_location = self.values[0]
        await interaction.response.send_message(content=f"{parameter_location}을 선택하셨습니다.")
        if (parameter_type != None and parameter_location != None):
            #print(f"Both parameters entered : {parameter_type} and {parameter_location}") -> currently here for testing purposes
            ans = random_select(parameter_type, parameter_location)
            await interaction.followup.send(ans[0] + ' | ' + ans[6])

# view object for the two select dropdowns
class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(SelectType())
        self.add_item(SelectLocation())


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='뭐먹지?')
async def what_to_eat(ctx):
    global parameter_type, parameter_location
    parameter_type = None
    parameter_location = None
    await ctx.send(view=SelectView())

bot.run(TOKEN)
