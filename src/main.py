from __future__ import unicode_literals
import os
from dotenv import load_dotenv
import youtube_dl

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")


def my_hook(d):
    # if d["status"] == "downloading":
    #     print("Downloading video!")
    if d["status"] == "finished":
        print("Downloaded!")


def download(url, output_dir="data/"):
    ydl_opts = {
        "format": "22",
        "continue": True,
        "outtmpl": output_dir + "%(uploader)s - %(title)s.%(ext)s",
        "progress_hooks": [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    # download("https://www.youtube.com/watch?v=63Kc8Xq9H0U")
    data = []
    with open("videos_list.txt", "r") as f:
        data = f.readlines()
    print(data)
    for url in data:
        normalized_url = url.strip()
        download(normalized_url)


if __name__ == "__main__":
    main()

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download("videos_list.txt")
# youtube-dl -f best -a videos_list.txt
