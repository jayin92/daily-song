import spotipy
import json
from datetime import datetime, date
import pytz
from spotipy.oauth2 import SpotifyOAuth


def remove_key(d, keys: list):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_key(v, keys) for v in d]
    return {k: remove_key(v, keys) for k, v in d.items()
            if k not in keys}

def filter_date(d) -> list:
    tz = pytz.timezone("Asia/Taipei")
    utc = pytz.timezone("UTC")
    today = date.today()
    res = []
    for song in d:
        song_dt = utc.localize(datetime.fromisoformat(song["played_at"][:-1])).astimezone(tz)
        if song_dt.date() == today:
            res.append(song)
            print(f'{song["track"]["artists"][0]["name"]} - {song["track"]["name"]}')
    return res

if __name__ == '__main__':
    client_id_file = open("spotify_cred.json", "r")
    client_id = json.load(client_id_file)

    scope = "user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id["SPOTIPY_CLIENT_ID"], client_id["SPOTIPY_CLIENT_SECRET"], client_id["SPOTIFY_REDIRECT_URI"], scope=scope))

    data = remove_key(sp.current_user_recently_played(), ["available_markets"])
    data = filter_date(data["items"]) # data is now a list
    
    recently_played = json.dumps(data, ensure_ascii=False, indent=2)

    with open("recent_played.json", "w", encoding="utf8") as file:
        file.write(recently_played)
