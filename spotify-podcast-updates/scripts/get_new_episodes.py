#!/usr/bin/env python3
"""
Fetch podcast episodes released in the last 24 hours from the user's Spotify library.

Required environment variables:
    SPOTIFY_CLIENT_ID      - Your Spotify app's client ID
    SPOTIFY_CLIENT_SECRET  - Your Spotify app's client secret
    SPOTIFY_REFRESH_TOKEN  - A refresh token with user-library-read scope

Usage:
    python get_new_episodes.py
"""

import os
import sys
from datetime import date, timedelta

import requests

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


def get_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    """Exchange a refresh token for a short-lived access token."""
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    if not response.ok:
        print(
            f"ERROR: Failed to obtain access token ({response.status_code}): {response.text}",
            file=sys.stderr,
        )
        sys.exit(1)

    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        print(
            "ERROR: No access_token in Spotify token response. Check your credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    return access_token


def get_all_shows(access_token: str) -> list:
    """Return all shows saved in the user's Spotify library (handles pagination)."""
    headers = {"Authorization": f"Bearer {access_token}"}
    shows = []
    url = f"{SPOTIFY_API_BASE}/me/shows"
    params = {"limit": 50}

    while url:
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            print(
                f"ERROR: Failed to fetch shows ({response.status_code}): {response.text}",
                file=sys.stderr,
            )
            sys.exit(1)

        data = response.json()
        for item in data.get("items", []):
            show = item.get("show", {})
            shows.append({"id": show.get("id"), "name": show.get("name")})

        # Follow pagination; clear params so offset isn't double-applied
        url = data.get("next")
        params = {}

    return shows


def get_recent_episodes(access_token: str, show_id: str, target_dates: set) -> list:
    """
    Return episodes for a show whose release_date falls within target_dates.

    Episodes are returned newest-first by Spotify, so we stop as soon as we
    encounter a date older than the earliest target date.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{SPOTIFY_API_BASE}/shows/{show_id}/episodes"
    params = {"limit": 50, "market": "from_token"}
    min_date = min(target_dates)
    recent = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            # Non-fatal: skip this show and continue processing others
            print(
                f"WARNING: Could not fetch episodes for show {show_id} "
                f"({response.status_code}). Skipping.",
                file=sys.stderr,
            )
            return recent

        data = response.json()
        for episode in data.get("items", []):
            if not episode:
                continue
            # Only compare when we have day-level precision
            if episode.get("release_date_precision") != "day":
                continue
            release_date = episode.get("release_date", "")
            if release_date < min_date:
                # Episodes are newest-first; everything after this is older
                return recent
            if release_date in target_dates:
                recent.append(
                    {
                        "name": episode.get("name", ""),
                        "release_date": release_date,
                    }
                )

        url = data.get("next")
        params = {}

    return recent


def main():
    # Validate required environment variables
    missing = [
        var
        for var in ("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REFRESH_TOKEN")
        if not os.environ.get(var)
    ]
    if missing:
        print(
            f"ERROR: Missing required environment variable(s): {', '.join(missing)}\n"
            "See .env.example for setup instructions.",
            file=sys.stderr,
        )
        sys.exit(1)

    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    refresh_token = os.environ["SPOTIFY_REFRESH_TOKEN"]

    # Target: today and yesterday (YYYY-MM-DD), covering the last ~24 hours
    today = date.today()
    target_dates = {today.isoformat(), (today - timedelta(days=1)).isoformat()}

    access_token = get_access_token(client_id, client_secret, refresh_token)
    shows = get_all_shows(access_token)

    results = []
    for show in shows:
        episodes = get_recent_episodes(access_token, show["id"], target_dates)
        for episode in episodes:
            results.append(
                {
                    "show_name": show["name"],
                    "episode_name": episode["name"],
                    "release_date": episode["release_date"],
                }
            )

    if not results:
        print("No new episodes in the last 24 hours.")
        return

    print(f"Found {len(results)} new episode(s) from your Spotify podcasts:\n")
    for r in results:
        print(f'"{r["show_name"]}" — "{r["episode_name"]}" ({r["release_date"]})')


if __name__ == "__main__":
    main()
