import praw
import requests
import ctypes
import os
from PIL import Image
import re
from dotenv import dotenv_values
import random


# Modifiable Globals
subreddit = 'wallpaper'
image_file_path = './wallpaper.jpg'
generator_limit = 100

# Unmodifiable Globals
jpg_or_png = re.compile(r"\.(?:jpg|png)$")
config = dotenv_values(".env")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
absolute_path = os.path.abspath(image_file_path)


def download_image(image_url):
    img_data = requests.get(image_url).content
    with open(image_file_path, 'wb') as handler:
        handler.write(img_data)


def change_resolution(new_resolution, image_path):
    (
        Image.open(image_path)
        .convert('RGB')
        .resize(new_resolution)
        .save(image_path)
    )


def main():
    reddit = praw.Reddit(
        client_id=config.get('reddit_client_id'),
        client_secret=config.get('reddit_client_secret'),
        user_agent=config.get('reddit_user_agent')
    )
    submission_list = []
    submission_generator = reddit.subreddit(subreddit).top(time_filter="week", limit=generator_limit)
    for submission in submission_generator:
        if jpg_or_png.findall(submission.url):
            submission_list.append(submission)
    submission = random.choice(submission_list)
    url = submission.url
    download_image(url)
    change_resolution(resolution, image_file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)  # changes the window's backdrop


if __name__ == '__main__':
    main()
