import praw
import threading
import requests
import subprocess
import os
import database

from config import *


POST_SEARCH_AMOUNT = 20
by  = ["new", "hot", "top", "rising"]
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"}
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "images/")
CHECK_FOLDER = os.path.isdir(image_path)
if not CHECK_FOLDER:
    os.makedirs(image_path)
video_path = os.path.join(dir_path, "video/")
CHECK_FOLDER = os.path.isdir(video_path)
if not CHECK_FOLDER:
    os.makedirs(video_path)
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent,)
subs = open("sub_list.csv", "r")


def sorted_sub(sub, by = None):
    if by:
        return exec(f"{reddit.subreddit(sub)}.{by}(limit={POST_SEARCH_AMOUNT})")
    return reddit.subreddit(sub).rising(limit=POST_SEARCH_AMOUNT)

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
            print(f"failed. {post.url.lower()}")
            print(e)

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
                print(f"failed. {post.url.lower()}")
                print(e)



def main(by=None):
    for line in subs:
        sub = line.strip()
        subreddit = sorted_sub(sub, by=by)
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

