import os
import discord
from discord.ext import commands
import random
import json

# Your actual Discord bot token (ensure you keep this secure)
TOKEN = ''  # Replace this with your actual token
SERVER_NAME = ''  # Use the actual server name
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix='!', intents=intents)



# Load intents from JSON file
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Initialize the Discord client
client = discord.Client()

def get_response(msg):
    """
    This function handles text responses based on the user's message.
    It matches the message with patterns from the intents file and returns a response.
    """
    msg = msg.lower()  # Convert message to lowercase for case-insensitive matching

    # Loop through each intent
    for intent in intents['intents']:
        # Check if the user's message matches any of the patterns for the tag
        for pattern in intent['patterns']:
            if pattern.lower() in msg:
                return random.choice(intent['responses'])

    return "Sorry, I didn't understand that."

# Event when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event when a message is received
@client.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == client.user:
        return

    # Process the user's message and get the response
    if message.content.startswith("!"):
        user_message = message.content[1:]  # Remove the '!' prefix for easy processing
        bot_response = get_response(user_message)
        await message.channel.send(bot_response)

# Start the bot
client.run(TOKEN)
