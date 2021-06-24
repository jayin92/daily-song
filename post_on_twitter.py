import tweepy
import json
from os import listdir


def post_on_twitter(post="", date="2021-06-25"):
    with open("twitter_cred.json", "r") as file:
        cred = json.load(file)

    auth = tweepy.OAuthHandler(cred["consumer_key"], cred["consumer_secret"])
    auth.set_access_token(cred["access_token"], cred["access_token_secret"])

    api = tweepy.API(auth)

    media_ids = []
    
    img_dir = f"img/{date}"

    print("Uploading images...")
    for img in listdir(img_dir):
        r = api.media_upload(f"{img_dir}/{img}")
        media_ids.append(r.media_id_string)
    print("Uploaded.")

    print("Tweeting...")
    api.update_status(status=post, media_ids=media_ids)
    print("Finished!")
if __name__ == '__main__':
    post_on_twitter()