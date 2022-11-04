import re
import os
import praw
import ctypes
import random
import requests
from PIL import Image
from dotenv import dotenv_values


def download_image(image_url, path):
    """downloads an image from the internet and puts in into the specified path"""
    img_data = requests.get(image_url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)


def change_resolution(new_resolution, image_path):
    """take an image given its path and changes it to the new specified resolution"""
    (
        Image.open(image_path)
             .convert('RGB')
             .resize(new_resolution)
             .save(image_path)
    )


def find_random_reddit_image(reddit_instance: praw.Reddit, subreddit, flair, limit, time_filter):
    """downloads a random image from reddit"""
    jpg_or_png = re.compile(r"\.(?:jpg|png)$")
    submission_list = []
    if flair == '':
        submission_generator = reddit_instance.subreddit(subreddit).top(time_filter=time_filter, limit=limit)
    else:
        submission_generator = reddit_instance.subreddit(subreddit).search(
            f'flair:"{flair}"',
            time_filter=time_filter,
            limit=limit
        )
    for submission in submission_generator:
        if jpg_or_png.findall(submission.url):
            submission_list.append(submission)
    submission = random.choice(submission_list)
    return submission.url


def main():
    config = dotenv_values(".env")
    image_file_path = './wallpaper.jpg'
    absolute_path = os.path.abspath(image_file_path)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    my_reddit = praw.Reddit(
        client_id=config.get('reddit_client_id'),
        client_secret=config.get('reddit_client_secret'),
        user_agent=config.get('reddit_user_agent'),
        username=config.get('reddit_username'),
        password=config.get('reddit_password')
    )
    url = find_random_reddit_image(
        reddit_instance=my_reddit,
        subreddit=config['subreddit'],
        flair=config['flair'],
        limit=int(config['limit']),
        time_filter=config['time_filter']
    )
    download_image(url, image_file_path)
    change_resolution(resolution, image_file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)  # changes the wallpaper


if __name__ == '__main__':
    main()
