# Reddit Image and Video Downloader

Downloades all the images and videos from subreddits.

- subreddits are mentioned in `sub_list.csv` file.
- can adjust number of posts to get from each subreddit `( default = 20 )` .
- Uses Threading for improved speed.
- ffmpeg for downloading videos
- subreddit posts can be sorted by `new`, `hot`, `top`, and `rising`.
- skip already downloaded video `( defaults to override )`.
- Keeps record of data using sqlite