from get_recent_played import get_recent_played
from gen_text_img import gen_text_img
from post_on_twitter import post_on_twitter
from post_on_telegram import post_on_telegram

if __name__ == '__main__':
    get_recent_played()
    tweet, telegram_post, date = gen_text_img()
    # post_on_twitter(tweet, date)
    post_on_telegram(telegram_post, date)
