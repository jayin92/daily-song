import spotipy
import json
import pytz
from colour import Color
from rich import print, box, color
from rich.padding import Padding
from rich.table import Table
from rich.console import Console
from datetime import datetime, date
from spotipy.oauth2 import SpotifyOAuth


def remove_key(d, keys: list):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_key(v, keys) for v in d]
    return {k: remove_key(v, keys) for k, v in d.items()
            if k not in keys}


def ms_to_min_sec(n: int) -> str:
    n //= 1000
    res = ""
    hour = n // 3600
    res += f'{hour:0>2}:' if hour != 0 else ""
    minu = n % 3600 // 60
    res += f'{minu:0>2}:' if minu != 0 else ""
    sec = n % 60
    res += f'{sec:0>2}' if sec != 0 else ""

    return res


def filter_date(d) -> list:
    tz = pytz.timezone("Asia/Taipei")
    utc = pytz.timezone("UTC")
    today = date.today()
    green = Color("green")
    gradient = list(green.range_to(Color("red"), 100))
    res = []
    total_durartion = 0
    for song in d:
        song_dt = utc.localize(datetime.fromisoformat(
            song["played_at"][:-1])).astimezone(tz)
        if song_dt.date() == today:
            total_durartion += song["track"]["duration_ms"]
    table = Table(
        title=f"[bold u]Songs Listen on {str(today)}[/bold u]", box=box.MINIMAL_DOUBLE_HEAD, show_footer=True)
    table.add_column("Artists", justify="left",
                     style="bright_cyan", footer=f"[bold bright_cyan]# of Songs: {len(d)}[/bold bright_cyan]")

    table.add_column("Song", justify="left", style="turquoise2")

    table.add_column("Duration", justify="right", style="light_slate_blue",
                     footer=f"[bold light_slate_blue]{ms_to_min_sec(total_durartion)}[/bold light_slate_blue]")

    table.add_column("Played At", justify="left", style="cyan")

    for song in d:
        song_dt = utc.localize(datetime.fromisoformat(
            song["played_at"][:-1])).astimezone(tz)
        if song_dt.date() == today:
            res.append(song)
            pop = song["track"]["popularity"]
            pop_color = color.parse_rgb_hex(gradient[pop-1].hex_l[1:])
            table.add_row(
                song["track"]["artists"][0]["name"],
                f'[pop_color]{pop: >3}[/pop_color] {song["track"]["name"]}',
                ms_to_min_sec(song["track"]["duration_ms"]),
                str(song_dt.time())[:-7],
            )
      
    console = Console()
    console.print(table)
    return res

def get_recent_played():
    client_id_file = open("spotify_cred.json", "r")
    client_id = json.load(client_id_file)

    scope = "user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id["SPOTIPY_CLIENT_ID"], client_id["SPOTIPY_CLIENT_SECRET"], client_id["SPOTIFY_REDIRECT_URI"], scope=scope))
    
    data = remove_key(sp.current_user_recently_played(), ["available_markets"])
    data = filter_date(data["items"])
    last = data[-1]
    tz = pytz.timezone("Asia/Taipei")
    utc = pytz.timezone("UTC")
    today = date.today()
    last_dt = utc.localize(datetime.fromisoformat(
            last["played_at"][:-1])).astimezone(tz)
    
    flag = True
    while(flag or last.date() == today):
        break
        flag = False
        timestamp = datetime.fromisoformat(last["played_at"][:-1]).timestamp()
        print(timestamp)
    
    return data


if __name__ == '__main__':
    
    client_id_file = open("spotify_cred.json", "r")
    client_id = json.load(client_id_file)

    scope = "user-read-recently-played"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id["SPOTIPY_CLIENT_ID"], client_id["SPOTIPY_CLIENT_SECRET"], client_id["SPOTIFY_REDIRECT_URI"], scope=scope))

    data = remove_key(sp.current_user_recently_played(), ["available_markets"])
    data = filter_date(data["items"])  # data is now a list

    recently_played = json.dumps(data, ensure_ascii=False, indent=2)

    with open("recent_played.json", "w", encoding="utf8") as file:
        file.write(recently_played)
