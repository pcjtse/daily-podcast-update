# Daily Podcast Update

A collection of [agent skills](https://agentskills.io) for keeping up with your podcast subscriptions.

## Skills

### [`spotify-podcast-updates`](./spotify-podcast-updates/)

Connects to the Spotify Web API and reports any new podcast episodes released in the last 24 hours from your subscribed shows.

## Quick Start

**Prerequisites**
- [Claude Code](https://claude.ai/code) (openclaw)
- Python 3.8+ and pip
- A [Spotify Developer](https://developer.spotify.com/dashboard) account

### 1. Install the skill

Copy the skill directory into your Claude Code skills folder:

```bash
git clone https://github.com/pcjtse/daily-podcast-update.git
cp -r daily-podcast-update/spotify-podcast-updates ~/.openclaw/skills/
```

### 2. Set up Spotify credentials

Copy the template and fill in your values:

```bash
cp ~/.openclaw/skills/spotify-podcast-updates/assets/.env.example ~/.env.spotify
```

Edit `~/.env.spotify` with your `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REFRESH_TOKEN`. See [`spotify-podcast-updates/assets/.env.example`](./spotify-podcast-updates/assets/.env.example) for step-by-step instructions on obtaining a refresh token from the Spotify Developer Dashboard.

Export the variables in your shell profile (e.g. `~/.bashrc` or `~/.zshrc`) so they are available in every Claude Code session:

```bash
export SPOTIFY_CLIENT_ID=your_client_id
export SPOTIFY_CLIENT_SECRET=your_client_secret
export SPOTIFY_REFRESH_TOKEN=your_refresh_token
```

### 3. Install Python dependencies

```bash
pip install -r ~/.openclaw/skills/spotify-podcast-updates/scripts/requirements.txt
```

### 4. Use the skill in Claude Code

Start a Claude Code session and ask:

> "What new podcast episodes came out today?"

Claude will automatically trigger the `spotify-podcast-updates` skill, check your Spotify subscriptions, and report any episodes released in the last 24 hours.

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
