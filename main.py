from get_recent_played import get_recent_played
from gen_text_img import gen_text_img
from post_on_twitter import post_on_twitter

if __name__ == '__main__':
    get_recent_played()
    post, date = gen_text_img()
    post_on_twitter(post, date)
