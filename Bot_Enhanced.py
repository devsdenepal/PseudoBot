import asyncio
import json
import logging
import os
import random
import re

import discord
import requests
from discord.ext import commands

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration from environment variables (never commit real secrets)
TOKEN = os.environ.get("DISCORD_TOKEN", "")  # Your actual Discord bot token
SERVER_NAME = os.environ.get("SERVER_NAME", "Server")  # Use the actual server name
API_NINJAS_KEY = os.environ.get("API_NINJAS_KEY", "")  # Your API Ninjas key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")  # Google Custom Search JSON API key
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "")  # Google Programmable Search Engine ID
human = os.environ.get("BOT_OWNER_NAME", "Dev")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = commands.Bot(command_prefix="!", intents=intents)


def load_intents(path="intents.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


intents_data = load_intents()


def google_search(query):
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "Google search is not configured. Set GOOGLE_API_KEY and GOOGLE_CSE_ID."
    if not query:
        return "Please provide a search term after the keyword."

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if "items" in data:
            results = []
            for i in range(min(2, len(data["items"]))):
                item = data["items"][i]
                results.append(f"**{item['title']}**\n{item['snippet']}\nLink: {item['link']}")
            return "\n".join(results)
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
                f"Location: {user['location']['city']}, {user['location']['country']}"
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
                f"Location: {user['location']['city']}, {user['location']['country']}"
            )
        else:
            return "Couldn't generate a female dummy account."
    except Exception as e:
        return f"Error: {e}"


def get_domain_info(domain):
    """Get WHOIS info for a domain via the API Ninjas API."""
    domain_pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not domain_pattern.match(domain):
        return "Invalid domain format. Please enter a valid domain (e.g., example.com)."
    if not API_NINJAS_KEY:
        return "Domain lookup is not configured. Set API_NINJAS_KEY."

    try:
        headers = {"X-Api-Key": API_NINJAS_KEY}
        response = requests.get(
            "https://api.api-ninjas.com/v1/whois?domain={}".format(domain), headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            return (
                f"**Domain Information:**\n"
                f"- Domain: {data.get('domain_name', 'N/A')}\n"
                f"- Registrar: {data.get('registrar', 'N/A')}\n"
                f"- Creation Date: {data.get('creation_date', 'N/A')}\n"
                f"- Expiration Date: {data.get('expiration_date', 'N/A')}"
            )
        else:
            return f"Couldn't retrieve domain information. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"


def get_number_info(number):
    """Validate a phone number via the API Ninjas API."""
    number_pattern = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}"
    )
    if not number_pattern.match(number):
        return "Invalid number format. Please enter a valid number (e.g., +9779000000000)."
    if not API_NINJAS_KEY:
        return "Phone lookup is not configured. Set API_NINJAS_KEY."

    try:
        headers = {"X-Api-Key": API_NINJAS_KEY}
        response = requests.get(
            "https://api.api-ninjas.com/v1/validatephone?number={}".format(number), headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            timezones = data.get("timezones")
            tz = timezones[0] if isinstance(timezones, list) and timezones else "N/A"
            return (
                f"**Number Information:**\n"
                f"- Status: {data.get('is_valid', 'N/A')}\n"
                f"- Country: {data.get('country', 'N/A')}\n"
                f"- Location: {data.get('location', 'N/A')}\n"
                f"- Timezones: {tz}"
            )
        else:
            return f"Couldn't retrieve number information. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"


def get_ip_info(ip_address):
    """Get IP address geolocation/infrastructure info from ipapi.co."""
    ip_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    if not ip_pattern.match(ip_address):
        return "Invalid IP address format. Please enter a valid IPv4 address."

    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        if response.status_code == 200:
            data = response.json()
            return (
                f"**IP Address Info:**\n"
                f"- IP: {data.get('ip')}\n"
                f"- City: {data.get('city')}\n"
                f"- Region: {data.get('region')}\n"
                f"- Country: {data.get('country_name')}\n"
                f"- Org: {data.get('org')}"
            )
        else:
            return "Couldn't retrieve IP information. Please try again later."
    except Exception as e:
        return f"Error: {e}"


def match_intent(message_text):
    """Match a message against system intents. Returns a response or None."""
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in message_text:
                return random.choice(intent["responses"])
    return None


async def respond(text, channel):
    """Send a response message to Discord."""
    await channel.send(text)


@client.event
async def on_ready():
    print(f"Logged in as: {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg_content = message.content.lower().strip()

    # Keyword-based OSINT lookups
    if "google" in msg_content:
        search_term = msg_content.replace("google", "").strip()
        response = google_search(search_term)
        await respond(response, message.channel)
    elif "youtube" in msg_content:
        response = google_search((msg_content.replace("youtube", "") + " site:youtube.com").strip())
        await respond(response, message.channel)
    elif "linkedin" in msg_content:
        response = google_search(
            (msg_content.replace("linkedin", "") + " site:linkedin.com").strip()
        )
        await respond(response, message.channel)
    elif "ip" in msg_content:
        ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", msg_content)
        if ip_match:
            ip_address = ip_match.group()
            response = get_ip_info(ip_address)
            await respond(response, message.channel)
            return
        else:
            await respond("Please provide an IP address, e.g. 'ip 8.8.8.8'.", message.channel)
    elif ("dummy account" in msg_content or "fake account" in msg_content) and "male" in msg_content:
        response = get_random_male()
        await respond(response, message.channel)
    elif ("dummy account" in msg_content or "fake account" in msg_content) and "female" in msg_content:
        response = get_random_female()
        await respond(response, message.channel)
    elif "domain" in msg_content:
        domain_match = re.search(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", msg_content)
        if domain_match:
            domain = domain_match.group()
            response = get_domain_info(domain)
            await respond(response, message.channel)
            return
        else:
            await respond("Please provide a domain, e.g. 'domain example.com'.", message.channel)
    elif "number" in msg_content:
        number_match = re.search(
            r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b",
            msg_content,
        )
        if number_match:
            number = number_match.group()
            response = get_number_info(number)
            await respond(response, message.channel)
            return
        else:
            await respond("Please provide a phone number, e.g. 'number +9779000000000'.", message.channel)

    # Intent Matching Logic
    intent_response = match_intent(msg_content)
    if intent_response:
        await message.channel.send(intent_response.replace("human", human))
        return


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is not set. Create a .env file or export the variable.")
    client.run(TOKEN)