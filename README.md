# Reddit Image and Video Downloader

Downloades all the images and videos from subreddits in different folders and keeps a record of links proccessed in a sqlite database.

- subreddits are mentioned in `sub_list.csv` file.
- can adjust number of posts to get from each subreddit `( default = 20 )` .
- Uses Threading for improved speed.
- ffmpeg for downloading videos
- subreddit posts can be sorted by `new`, `hot`, `top`, and `rising`.
- skip already downloaded video `( defaults to override )`.
- Keeps record of data using sqlite.

## How to Use-

1. Enter names of subreddits in the list in `sub_list.py`.
2. Rename `Config` file to `config.py`.
3. Edit the `config.py` file to insert your `client_id`, `secret`, and `app name`. [How to get these](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)
4. change `POST_SEARCH_AMOUNT` in `config.py` to set number of posts per subreddit.
5. change `sort_by` in `config.py` to choose from different sorting types.
6. run `main.py`