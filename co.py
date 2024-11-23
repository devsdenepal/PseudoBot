import pyttsx3
import os
import discord
from discord.ext import commands
import requests
from chatbot import *   # Import chatbot and its decorators for response handling
import wikipedia
import logging
import torch
import json
import asyncio
import re
import random
# Set up logging for debugging and monito
# Your actual Discord bot token (ensure you keep this secure)
TOKEN = 'MTMwMzM2ODU4MDA1Nzc5NjYxOA.G5BZE2.gUv9A2EFjMT3KhoOl6rdldBcYKtQMk9K1MbtSc'  # Replace this with your actual token
SERVER_NAME = 'DevServer'  # Use the actual server name
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix='!', intents=intents)
API_NINJAS_KEY = "u2WUNGAW0Y0VCgkqM7uKaA==f2GmRvZntpTgyhIk"  # Your API Ninjas key
human = "Dev"
engine = pyttsx3.init('sapi5')
# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
#engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
# Load intents from intents.json
with open("intents.json", "r") as file:
    intents_data = json.load(file)
# Google API credentials
GOOGLE_API_KEY = "AIzaSyAhplEs2-F-n0bD5sUi2PP_lAYhjyQ-PI4"
GOOGLE_CSE_ID = "51ec8274217dc4d8c"
print("new")
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if "items" in data:
            # Grab the first result
            first_result = data["items"][0]
            title = first_result["title"]
            snippet = first_result["snippet"]
            link = first_result["link"]
            second_result = data["items"][1]
            title2 = second_result["title"]
            snippet2 = second_result["snippet"]
            link2 = second_result["link"]
            return f"**{title}**\n{snippet}\nLink: {link}\n**{title2}**\n{snippet2}\nLink: {link2}"
        else:
            return "No results found on Google."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
def get_random_male():
    """Generates a random male dummy account using a free random user API."""
    try:
        response = requests.get("https://randomuser.me/api/?gender=male")
        if response.status_code == 200:
            user = response.json()["results"][0]
            return (
                f"Name: {user['name']['first']} {user['name']['last']}\n"
                f"Username: {user['login']['username']}\n"
                f"Email: {user['email']}\n"
                f"Location: {user['location']['city']}, {user['location']['country']}\n"
            )
        else:
            return "Couldn't generate a male dummy account."
    except Exception as e:
        return f"Error: {e}"

def get_random_female():
    """Generates a random female dummy account using a free random user API."""
    try:
        response = requests.get("https://randomuser.me/api/?gender=female")
        if response.status_code == 200:
            user = response.json()["results"][0]
            return (
                f"Name: {user['name']['first']} {user['name']['last']}\n"
                f"Username: {user['login']['username']}\n"
                f"Email: {user['email']}\n"
                f"Location: {user['location']['city']}, {user['location']['country']}\n"
            )
        else:
            return "Couldn't generate a female dummy account."
    except Exception as e:
        return f"Error: {e}"
# OSINT Function: Get Domain Information with API Ninjas
def get_domain_info(domain):
    domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not domain_pattern.match(domain):
        return "Invalid domain format. Please enter a valid domain (e.g., example.com)."

    try:
        headers = {'X-Api-Key': API_NINJAS_KEY}
        response = requests.get("https://api.api-ninjas.com/v1/whois?domain={}".format(domain), headers=headers)
        if response.status_code == 200:
            data = response.json()
            info = (
                f"**Domain Information:**\n"
                f"- Domain: {data.get('domain_name', 'N/A')}\n"
                f"- Registrar: {data.get('registrar', 'N/A')}\n"
                f"- Creation Date: {data.get('creation_date', 'N/A')}\n"
                f"- Expiration Date: {data.get('expiration_date', 'N/A')}\n"
            )
            return info
        else:
            return f"Couldn't retrieve domain information. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
# OSINT Function: Get Domain Information with API Ninjas
def get_number_info(number):
    number_pattern = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}')
    if not number_pattern.match(number):
        return "Invalid number format. Please enter a valid number (e.g., +9779000000000)."

    try:
        headers = {'X-Api-Key': API_NINJAS_KEY}
        response = requests.get("https://api.api-ninjas.com/v1/validatephone?number={}".format(number), headers=headers)
        if response.status_code == 200:
            data = response.json()
            info = (
                f"**Number Information:**\n"
                f"- Status: {data.get('is_valid', 'N/A')}\n"
                f"- Country: {data.get('country', 'N/A')}\n"
                f"- Location: {data.get('location', 'N/A')}\n"
                f"- Timezones: {data.get('timezones', 'N/A')[0]}\n"
            )
            return info
        else:
            return f"Couldn't retrieve domain information. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
# OSINT Function: Get IP Information
def get_ip_info(ip_address):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if not ip_pattern.match(ip_address):
        return "Invalid IP address format. Please enter a valid IPv4 address."

    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        if response.status_code == 200:
            data = response.json()
            info = (
                f"**IP Address Info:**\n"
                f"- IP: {data.get('ip')}\n"
                f"- City: {data.get('city')}\n"
                f"- Region: {data.get('region')}\n"
                f"- Country: {data.get('country_name')}\n"
                f"- Org: {data.get('org')}\n"
            )
            return info
        else:
            return "Couldn't retrieve IP information. Please try again later."
    except Exception as e:
        return f"Error: {e}"

# Logical Response Function (Fallback)
def logical_response(message_text):
    responses = [
        "I'm not sure about that, but feel free to clarify!",
        "I don't have an answer for that, but I'm here to help with other things.",
        "Hmm, that's interesting. Can you tell me more?",
    ]
    return random.choice(responses)

# Intent Matching Function
def match_intent(message_text):
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in message_text:
                return random.choice(intent["responses"])
    return None

def speak_text(text):
    """Handles the TTS processing."""
    engine.say(text)
    engine.runAndWait()

async def respond(text, channel):
    """Handles TTS and sending a message to Discord."""
    # Run TTS asynchronously
#    speak_text(text)
    # Send the response message to Discord
    await channel.send(text)
@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg_content = message.content.lower().strip()

    # Define hotwords and associated OSINT functions
    if "google" in msg_content:
        search_term = msg_content.replace("google", "").strip()
        response = google_search(search_term)
        await respond(response,message.channel)
    elif "youtube" in msg_content:
        response = google_search(((msg_content.replace("youtube", "") + " site:youtube.com")).strip())
        await respond(response,message.channel)
    elif "linkedin" in msg_content:
        response = google_search(((msg_content.replace("linkedin", "") + " site:linkedin.com")).strip())
        await respond(response,message.channel)
    # OSINT Hotword-Based Detection
    elif "ip" in msg_content:
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', msg_content)
        if ip_match:
            ip_address = ip_match.group()
            response = get_ip_info(ip_address)
            await respond(response,message.channel)
            return
    elif ("dummy account" in msg_content or "fake account" in msg_content) and "male" in msg_content:
        response = get_random_male()
        await respond(response,message.channel)
    elif ("dummy account" in msg_content or "fake account" in msg_content) and "female" in msg_content:
        response = get_random_female()
        await respond(response,message.channel)
    elif "domain" in msg_content:
        domain_match = re.search(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', msg_content)
        if domain_match:
            domain = domain_match.group()
            response = get_domain_info(domain)
            await respond(response,message.channel)
            return
    elif "number" in msg_content:
        number_match = re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b', msg_content)
        if number_match:
            number = number_match.group()
            response = get_number_info(number)
            await respond(response,message.channel)
            return
    # Intent Matching Logic
    intent_response = match_intent(msg_content)
    if intent_response:
        await message.channel.send(intent_response.replace("human",human))
        return

    # Fallback Response for Unmatched Inputs
#    response = logical_response(msg_content)
#    await respond(response,message.channel)
# Run the bot with your Discord token
client.run(TOKEN)

