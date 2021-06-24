import json
import requests
import os
from get_recent_played import ms_to_min_sec
from math import *
from tqdm import tqdm
from PIL import Image
from datetime import datetime, date

def create_n_by_n_img(imgs: list, n: int):
    w = imgs[0].width 
    h = imgs[0].height
    res = Image.new('RGB', (n*w, n*h))
    empty = Image.new('RGB', (w, h))
    for i in range(n):
        for j in range(n):
            idx = n*i+j
            if idx < len(imgs):
                res.paste(imgs[idx], (w*j, h*i))
            else:
                res.paste(empty, (w*j, h*i))

    return res


def gen_text_img():
    with open("recent_played.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    today = str(date.today())

    try:
        os.mkdir(f"img/{today}")
        print(f"Directory img/{today} created.")
    except FileExistsError:
        print(f"Directory img/{today} already exists.")

    
    total_duration = 0
    imgs = []

    cnt = 0
    artists = set()
    for song in tqdm(data):
        artists.add(song["track"]["artists"][0]["name"])
        total_duration += song["track"]["duration_ms"]
        url = song["track"]["album"]["images"][1]["url"] # 0: 640, 1: 300, 2: 64
        cover = Image.open(requests.get(url, stream=True).raw)
        imgs.append(cover)
        if len(imgs) == 25:
            cnt += 1
            create_n_by_n_img(imgs, 5).save(f"img/{today}/{cnt}.png")
            imgs = []

    if len(imgs) != 0:
        cnt += 1
        create_n_by_n_img(imgs, ceil(sqrt(len(imgs)))).save(f"img/{today}/{cnt}.png")

    post = f"Music on {today}\nTotal Duration: {ms_to_min_sec(total_duration)}\n"
    for artist in artists:
        if len(post) + len(artist) <= 240:            
            post += f"{artist}\n"
    with open(f"post/{today}.txt", "w", encoding="utf-8") as file:
        file.write(post)
        print(f"post/{today}.txt saved.")
    
    return post, today

if __name__ == '__main__':
    gen_text_img()