import os
import json
import random
import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN", "")  # Set via environment variable
SERVER_NAME = os.environ.get("SERVER_NAME", "")  # Use the actual server name

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix="!", intents=intents)


def load_intents(path="intents.json"):
    with open(path, "r", encoding="utf-8") as json_data:
        return json.load(json_data)


intents_data = load_intents()


def get_response(msg):
    """Match a message against the intents file and return a response."""
    msg = msg.lower()  # Convert message to lowercase for case-insensitive matching

    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in msg:
                return random.choice(intent["responses"])

    return "Sorry, I didn't understand that."


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


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


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is not set. Create a .env file or export the variable.")
    client.run(TOKEN)