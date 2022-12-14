import praw
import threading
import requests
import subprocess
import os
import database

from sub_list import *
from config import *


CHECK_FOLDER = os.path.isdir(image_path)
if not CHECK_FOLDER:
    os.makedirs(image_path)

CHECK_FOLDER = os.path.isdir(video_path)
if not CHECK_FOLDER:
    os.makedirs(video_path)
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent,)

def sorted_sub(sub):
    if sort_by == "new":
        return reddit.subreddit(sub).new(limit=POST_SEARCH_AMOUNT)
    elif sort_by == "top":
        return reddit.subreddit(sub).top(limit=POST_SEARCH_AMOUNT)
    elif sort_by == "hot":
        return reddit.subreddit(sub).hot(limit=POST_SEARCH_AMOUNT)
    elif sort_by == "rising":
        return reddit.subreddit(sub).rising(limit=POST_SEARCH_AMOUNT)
    elif sort_by == "gilded":
        return reddit.subreddit(sub).gilded(limit=POST_SEARCH_AMOUNT)
    elif sort_by == "controversial":
        return reddit.subreddit(sub).controversial(limit=POST_SEARCH_AMOUNT)
    else:
        return ValueError


def download(url, name):
    if os.path.exists(video_path+name+".mp4"):
        # ans = input(f"File '{name}.mp4' already exists. Overwrite? [y/N] ")
        ans = 'y'
        if ans in ['N', 'n']:
            return
        os.remove(video_path+name+".mp4")
    cmd = 'ffmpeg -i "%s" -c copy %s.mp4' %(url, name)
    download = subprocess.run(cmd, cwd=video_path, capture_output=True).returncode
    if download == 0:
        return (f"{name} downloaded successfully")
    else:
        return (f"downloading {name} failed")



def get_from(post, sub):
    # for image
    if post.url.lower().endswith(".jpg") or post.url.lower().endswith(".png"):
        try:
            resp = requests.get(post.url, headers=header).content
            with open(f"{image_path}{sub}-{post.id}.png", "wb") as f:
                f.write(resp)
                f.close()
            database.insert(sub, post.url, post.id, post.url)
                
        except Exception as e:
            print(f"failed. {post.url.lower()}", " Error : ", e)

    # for video
    else:
        if post.is_video:
            m3u8 = post.media['reddit_video']['hls_url']
            download(m3u8, f"{sub}-{post.id}")
            database.insert(sub, post.url, post.id, m3u8)
        else:
            try:
                resp = requests.head("https://www.reddit.com/video/" + post.url.split('/v.redd.it/')[1], headers=header).headers['Location']
                json_url = resp[:-1:]+".json"
                json_data = requests.get(json_url, headers=header).json()
                m3u8 = json_data[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["hls_url"]
                download(m3u8, f"{sub}-{post.id}")
                database.insert(sub, post.url, post.id, m3u8)
            except Exception as e:
                print(f"failed. {post.url.lower()}", " Error : ", e)


def main():
    for line in subs:
        sub = line.strip()
        subreddit = sorted_sub(sub)
        print(f"Starting {sub}!")
        database.con_table(sub)

        threads = []

        for post in subreddit:
            t = threading.Thread(target = get_from, args=(post, sub,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
        for t in threads:
            while t.is_alive():
                continue
        print(f"{sub} complete")

if __name__ == "__main__":
    main()

