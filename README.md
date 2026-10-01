# SB24 — @SBWordFlipBot

SB24 is a focused Telegram text case conversion bot.

## Purpose

The bot provides exactly three primary text-conversion actions:

1. UPPERCASE
2. lowercase
3. Title Case

There are no external URLs, landing pages, payment flows, redirects, gambling features, or unrelated tools.

## Project structure

```
app/
  __init__.py
  config.py
  content.py
  handlers.py
  keyboards.py
  main.py
.env.example
requirements.txt
render.yaml
README.md
```

## Local setup

1. Create a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set the required environment variable:

   ```bash
   export BOT_TOKEN="YOUR_BOT_TOKEN"
   ```

   Optional:

   ```bash
   export BOT_NAME="SB24"
   export BOT_USERNAME="@SBWordFlipBot"
   ```

4. Run:

   ```bash
   python -m app.main
   ```

## Render deployment

Create a background worker using the included `render.yaml`.

Set `BOT_TOKEN` as a secret environment variable in Render. Do not commit a real bot token to GitHub.

The service starts with:

```bash
python -m app.main
```

## Telegram profile setup

On startup, the application attempts to configure:

- Bot name: SB24
- Short description/about: SB24 flips text case: uppercase, lowercase, or title case.
- Description: Transform your text directly in Telegram. Choose UPPERCASE, lowercase, or Title Case, send your text, and SB24 returns the converted result.

These settings are sent through the Telegram Bot API. If Telegram rejects a profile update, the bot logs the error and continues running.

## Main user flow

```
/start
  ↓
Welcome message
  ↓
UPPERCASE | lowercase
Title Case
  ↓
User sends text
  ↓
Converted result
```

## Verification notes

The project intentionally keeps the main menu to exactly three visible conversion buttons.

Before promotion, confirm in the live bot that:

- /start displays all three buttons.
- Each conversion returns the expected text transformation.
- No external links appear in any bot message.
- The bot profile text matches the implemented functionality.
- BOT_TOKEN is configured only through environment variables.

Telegram Ads review decisions are made by Telegram and are not guaranteed by this project.
