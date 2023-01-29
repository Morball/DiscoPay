import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime,timedelta
import requests
import json
from dateutil import parser
TOKEN="MTA2OTA1OTUxMDA3NDg3MTg2MA.G42DHA.azLYaSXwdZ1ZoWv8UJLkp-Pxdo4hriupJb--5g"

client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

def check_license_status(username):
    r=requests.get("http://127.0.0.1:5000/api/v1/subscriptions/", headers={"Content-Type": "application/json"},data=json.dumps({'username':username})).text
    if datetime.strptime(json.loads(r)["expiration_date"],"%Y-%m-%d %H:%M:%S")<datetime.now():
        return False
    else:
        return True


'''
basic plan

check if user has active subscription using api
if yes add role if not ignore

on every message check if the user has sub role and check expiration date from api, if exp date<datetime.now remove role else do nothing

        if "role_name" in [role.name for role in message.author.roles]:



'''


@client.event
async def on_message(message):
    
    if message.channel.name == "claim-ur-license" and message.content == "!claim":
        auth=str(message.author)
        if check_license_status(auth):
            # Find the role "licensed"
            role = discord.utils.get(message.guild.roles, name="muie")
            # Add the role to the user
            await message.author.add_roles(role)
            await message.channel.send(f"Claimed license for user {message.author.mention}")
        else:
            await message.channel.send("You don't have an active license to claim.")
            print(message.author)
    
    if "muie" in [role.name for role in message.author.roles]:
        if check_license_status(str(message.author)):
            pass
        else:
            role = discord.utils.get(message.guild.roles, name="muie")
            await message.author.remove_roles(role)
            await message.channel.send(f"Removed license for user {message.author.mention}")

client.run(TOKEN)


