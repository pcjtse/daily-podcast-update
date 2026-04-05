# Daily Podcast Update

A collection of [agent skills](https://agentskills.io) for keeping up with your podcast subscriptions.

## Skills

### [`spotify-podcast-updates`](./spotify-podcast-updates/)

Connects to the Spotify Web API and reports any new podcast episodes released in the last 24 hours from your subscribed shows.

## Quick Start

**Prerequisites**
- Python 3.8+
- pip
- A [Spotify Developer](https://developer.spotify.com/dashboard) account

**Setup**

1. Clone this repository:
   ```bash
   git clone https://github.com/pcjtse/daily-podcast-update.git
   cd daily-podcast-update
   ```

2. Copy the credentials template and fill in your values:
   ```bash
   cp spotify-podcast-updates/assets/.env.example .env
   # Edit .env with your SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN
   source .env
   ```
   See [`spotify-podcast-updates/assets/.env.example`](./spotify-podcast-updates/assets/.env.example) for step-by-step instructions on obtaining a refresh token.

3. Install dependencies:
   ```bash
   pip install -r spotify-podcast-updates/scripts/requirements.txt
   ```

4. Run:
   ```bash
   python spotify-podcast-updates/scripts/get_new_episodes.py
   ```

**Example output**
```
Found 3 new episode(s) from your Spotify podcasts:

"The Daily" — "How the Trade War Unfolded" (2026-04-05)
"Hard Fork" — "The AI Agents Are Here" (2026-04-05)
"Decoder with Nilay Patel" — "Inside Apple's AI Strategy" (2026-04-04)
```

## Skill Format

Skills in this repo follow the [agentskills.io](https://agentskills.io) specification:

```
skill-name/
├── SKILL.md        # agent workflow instructions
├── scripts/        # executable scripts
└── assets/         # templates and resources
```
