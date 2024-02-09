import discord
from discord.ext import commands
from google.cloud import compute_v1
from google.oauth2 import service_account
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Google Cloud credentials
# Update these
GCP_PROJECT = 'extreme-height-412800'
GCP_ZONE = 'australia-southeast1-b'
GCP_VM_NAME = 'palworld2'
GCP_CREDENTIALS_FILE = './credentials.json'

# Create a Google Cloud Compute Engine client
credentials = service_account.Credentials.from_service_account_file(GCP_CREDENTIALS_FILE)
compute_client = compute_v1.InstancesClient(credentials=credentials)

#Intents?
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='startvm')
async def start_vm(ctx):
    try:
        request   = compute_v1.StartInstanceRequest(instance=GCP_VM_NAME,
                                                   project=GCP_PROJECT, 
                                                   zone=GCP_ZONE,)
        response = compute_client.start(request=request)
        await ctx.send(f'Starting VM {GCP_VM_NAME}. Operation status: {response["status"]}')
    except Exception as e:
        await ctx.send(f'Error starting VM: {str(e)}')

@bot.command(name='stopvm')
async def stop_vm(ctx):
    try:
        request   = compute_v1.StopInstanceRequest(instance=GCP_VM_NAME,
                                                   project=GCP_PROJECT, 
                                                   zone=GCP_ZONE,)
        response = compute_client.stop(request=request)
        await ctx.send(f'Stopping VM {GCP_VM_NAME}. Operation status: {response["status"]}')
    except Exception as e:
        await ctx.send(f'Error stopping VM: {str(e)}')

bot.run(TOKEN)