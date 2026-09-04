# PseudoBot

A customizable **Discord chatbot** driven by an intent file (`intents.json`) with optional OSINT/info lookup commands. Two flavors are included:

- **`Bot.py`** — lightweight chatbot. Replies to any message prefixed with `!` by matching patterns in `intents.json`.
- **`Bot_Enhanced.py`** — adds keyword commands for Google search, IP / domain / phone lookup, and dummy-account generation.

## Quick start

### 1. Create a bot on Discord

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**.
2. **Bot** tab → **Reset Token** → copy the token.
3. Enable **Message Content Intent** (required for reading messages).
4. **OAuth2 → URL Generator**: scope `bot` + `applications.commands`, give `Send Messages` / `Read Message History` permissions, open the URL and invite the bot to your server.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
```

Fill in `DISCORD_TOKEN` (required) and, optionally, `GOOGLE_API_KEY` + `GOOGLE_CSE_ID` (Google search), `API_NINJAS_KEY` (domain/phone lookup), and `SERVER_NAME`.

### 4. Run

```bash
python Bot.py            # lightweight chatbot
# or
python Bot_Enhanced.py   # chatbot + info lookup commands
```

## Usage

### Bot.py

Send any message starting with `!`, e.g. `!hello` — the bot replies using the matching intent in `intents.json`.

### Bot_Enhanced.py

| You say                                    | The bot replies with                              |
| ------------------------------------------ | ------------------------------------------------- |
| `google <term>`                            | Top 2 Google results                              |
| `youtube <term>`                           | Top 2 results restricted to YouTube               |
| `linkedin <term>`                          | Top 2 results restricted to LinkedIn              |
| `ip 8.8.8.8`                               | IP geolocation / network info                      |
| `domain example.com`                       | WHOIS domain info (needs `API_NINJAS_KEY`)         |
| `number +9779000000000`                    | Phone validation (needs `API_NINJAS_KEY`)         |
| `dummy account male` / `dummy account female` | Randomly generated test account                  |

Any other message falls back to `intents.json` matching (with `human` replaced by `BOT_OWNER_NAME`).

## Customizing responses

Edit `intents.json`. Each intent has a `tag`, `patterns` (things users say), and `responses` (possible replies). The bot picks a random response per matched intent:

```json
{
  "tag": "greeting",
  "patterns": ["hi", "hello"],
  "responses": ["Hello!", "Hey there!"]
}
```

## Security notes

- **Never commit real API keys.** All secrets are read from environment variables (`.env`). A previously hardcoded Google API key was removed from the code — **rotate that key** if it was ever exposed.
- This bot reads and replies only in servers you invite it to; it has no access anywhere else. Use informational tools (WHOIS, IP, phone lookup) only for data you are authorized to investigate.

## License

[CC0 1.0 Universal](LICENSE) — public domain.