# Daily Song

See what you listen today. 

## Usage

1. Create an app in [Spotify Dashborad](https://developer.spotify.com/dashboard/).
2. In app setting, set redirect URI as `http://localhost:8080`
3. Create `spotify_cred.json` file and add your `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`. 
```json
{
    "SPOTIPY_CLIENT_ID": "xxxx",
    "SPOTIPY_CLIENT_SECRET": "xxxxx",
    "SPOTIFY_REDIRECT_URI": "http://localhost:8080",
}
```

3. Run `main.py`