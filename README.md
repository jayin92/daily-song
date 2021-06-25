# Daily Song

See what you listen today. 

## Usage

1. run `pip install -r requirements.txt` to install required package.
2. Create an app in [Spotify Dashborad](https://developer.spotify.com/dashboard/).
3. In app setting, set redirect URI as `http://localhost:8080`
4. Create `spotify_cred.json` file and add your `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` as below.
```json
{
    "SPOTIPY_CLIENT_ID": "xxxx",
    "SPOTIPY_CLIENT_SECRET": "xxxxx",
    "SPOTIFY_REDIRECT_URI": "http://localhost:8080",
}
```
5. Run `main.py`