import os
import discord
from discord.ext import commands

# Your actual Discord bot token (ensure you keep this secure)
TOKEN = ''  # Replace this with your actual token
SERVER_NAME = ''  # Use the actual server name
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix='!', intents=intents)

def read_tasks_from_file():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            # Strip newline characters and return a clean list
            return [task.strip() for task in tasks if task.strip()]
    except FileNotFoundError:
        print("tasks.txt not found. Please ensure the file exists.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
tasks = read_tasks_from_file()
# Load tasks from the file
@client.event
async def on_ready():
    print(f'Logged in as: {client.user}')

@client.event
async def on_message(message):
    # Only respond to messages from other users, not from the bot itself
    if message.author == client.user:
        return

    # Check for the greeting and respond
    if "hi" in message.content.lower():
        await message.channel.send("Hi there! Ready to tackle some tasks? 🎉")

    # Check for a command to read tasks
    if "y" in message.content.lower():
        if tasks:
            task_list = "\n".join(f"✨ {task}" for task in tasks)
            await message.channel.send(f"Here are your tasks for today:\n{task_list}")
        else:
            await message.channel.send("You have no tasks on your list! 🎉 Feel free to add some!")

# Start the bot
client.run(TOKEN)
