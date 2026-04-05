---
name: spotify-podcast-updates
description: Fetch new podcast episodes from the user's Spotify library released in the last 24 hours. Use when the user asks what's new in their podcasts, wants a daily podcast briefing, or asks about recent episodes from their Spotify subscriptions.
---

# Spotify Podcast Updates

Fetch new podcast episodes from the user's Spotify library released today or yesterday (last ~24 hours).

## Bundled Files

```
spotify-podcast-updates/
├── SKILL.md                        # this file
├── scripts/
│   ├── get_new_episodes.py         # Spotify API script
│   └── requirements.txt           # Python dependencies
└── assets/
    └── .env.example               # credential setup template
```

## Prerequisites

The following environment variables must be set before running this skill:

| Variable | Description |
|---|---|
| `SPOTIFY_CLIENT_ID` | Your Spotify app's Client ID |
| `SPOTIFY_CLIENT_SECRET` | Your Spotify app's Client Secret |
| `SPOTIFY_REFRESH_TOKEN` | A refresh token with `user-library-read` scope |

See `spotify-podcast-updates/assets/.env.example` for instructions on obtaining these values.

**Note:** The script reads env vars directly from the shell environment. If you store them in a `.env` file, load it first with `source .env` (or use `direnv`).

## Workflow

Make a todo list for all the tasks in this workflow and work on them one after another.

### 1. Check Environment Variables

Verify that `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REFRESH_TOKEN` are all set in the current shell environment.

Run:
```bash
echo "CLIENT_ID set: ${SPOTIFY_CLIENT_ID:+yes}" && \
echo "CLIENT_SECRET set: ${SPOTIFY_CLIENT_SECRET:+yes}" && \
echo "REFRESH_TOKEN set: ${SPOTIFY_REFRESH_TOKEN:+yes}"
```

If any variable is missing (line prints nothing after the colon), stop and tell the user which variables are missing. Refer them to `spotify-podcast-updates/assets/.env.example` for setup instructions. Do not proceed until all three are set.

### 2. Install Dependencies

Install the required Python package:

```bash
pip install -r spotify-podcast-updates/scripts/requirements.txt
```

If the file is not found, tell the user the skill files appear incomplete and that they should re-clone or restore the repository.

### 3. Run the Script

Execute the main script and capture output:

```bash
python spotify-podcast-updates/scripts/get_new_episodes.py
```

Note: If the user has many subscribed podcasts (50+), this may take a moment — it must fetch episodes for each show individually.

### 4. Handle Results

**If exit code is non-zero:**
- Show the user the error from stderr
- Common causes:
  - Invalid or expired credentials → re-run the OAuth flow described in `spotify-podcast-updates/assets/.env.example` to get a fresh `SPOTIFY_REFRESH_TOKEN`
  - Network error → retry once; if it persists, check internet connectivity
- Do not retry automatically more than once

**If exit code is 0:**
- Present the stdout output to the user in a clean, readable format
- If the output is `No new episodes in the last 24 hours.`, tell the user there are no new episodes today and suggest checking back tomorrow

## Wrap Up

Summarize the results to the user:
- How many new episodes were found
- Which shows had new episodes
- If none were found, confirm that their subscriptions were checked successfully
