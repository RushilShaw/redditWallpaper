import praw
import requests
import ctypes
import os
from PIL import Image
import re
from dotenv import dotenv_values


# Modifiable Globals
subreddit = 'wallpaper'
image_file_path = './wallpaper.jpg'

# Unmodifiable Globals
jpg_or_png = re.compile(r"\.(?:jpg|png)$")
config = dotenv_values(".env")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
current_path = os.getcwd()
absolute_path = f"{current_path}\\{image_file_path[2:] if image_file_path[:2] == './' else image_file_path}"


def download_image(image_url):
    img_data = requests.get(image_url).content
    with open(image_file_path, 'wb') as handler:
        handler.write(img_data)


def change_resolution(new_resolution, image_path):
    (
        Image.open(image_path)
        .convert('RGB')
        .resize(new_resolution, Image.ANTIALIAS)
        .save(image_path)
    )


def main():
    reddit = praw.Reddit(
        client_id=config.get('reddit_client_id'),
        client_secret=config.get('reddit_client_secret'),
        user_agent=config.get('reddit_user_agent')
    )
    submission = reddit.subreddit(subreddit).random()
    url = submission.url
    count = 0
    while not jpg_or_png.findall(url) or submission.score < 1000:  # images must be jpgs
        assert count < 50, "Image not able to be created"
        submission = reddit.subreddit(subreddit).random()
        url = submission.url
        count += 1
    download_image(url)
    change_resolution(resolution, image_file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)  # changes the window's backdrop


if __name__ == '__main__':
    main()
