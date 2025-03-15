# Spotify Playlist Migrator

A Python script to transfer playlists between two Spotify accounts without requiring user management setup.

## Features
- 🚀 Transfer all playlists (public/private) between accounts
- ✅ Automatic duplicate prevention
- ⏳ Handles large playlists with pagination
- 📋 Preserves playlist metadata (name, description, visibility)

## Prerequisites
- Python 3.6+
- Spotify developer account
- Two active Spotify accounts (old & new)

## Setup

### 1. Install requirements
```bash
pip install spotipy
```

### 2. Create a Spotify App
- Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create a new app:
  - **App Name:** Playlist Migrator
  - **App Type:** Web App
  - **Redirect URIs:** `http://localhost:8080/callback`
  - **Website:** `http://localhost:8080`
  - **Add the accounts:** In the user management section add the emails of your accounts 
- Copy your **Client ID** and **Client Secret**

### 3. Configure the script
Edit the CLIENT_ID and CLIENT_SECRET, so that it matches with the one from your Spotify Developer App
```python
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"
```

## Usage
### Run the script
```bash
python transfer_playlists.py
```

### Authenticate Old Account
1. Open the provided link in a browser
2. Log in with your **old** account
3. After redirection, copy the **full URL** from the address bar (e.g., `http://localhost:8080/callback?code=AQBx...`)
4. Paste it into the terminal

### Authenticate New Account
1. Repeat the authentication process with your **new** account
2. Use a different browser or an incognito window if needed

### Let the script run
- Lists all playlists from the old account
- Creates them in the new account
- Transfers all unique tracks
- Skips existing playlists

## Troubleshooting
### Common Errors
| Error               | Solution |
|----------------------|--------|
| `INVALID_CLIENT`    | Verify `Client ID`/`Client Secret` |
| `403 Forbidden`     | Ensure the **Redirect URI** is correctly set in the Spotify Dashboard |
| **Duplicate playlists** | Delete the `.cache-old` and `.cache-new` files |
| **Empty playlists** | Check if the tracks are available in your region |

### Rate Limits
The script includes:
- Automatic rate limiting
- Batch processing (100 tracks per request)
- 1-second delay between requests


> **Note:** This is not an official Spotify tool. Use at your own responsibility.
