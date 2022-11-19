from __future__ import unicode_literals
from dotenv import load_dotenv
import os
import youtube_dl
import supervisely as sly

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")

progress_video = None


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
    # api = sly.Api.from_env()
    # team_id = sly.env.team_id()

    # download("https://www.youtube.com/watch?v=63Kc8Xq9H0U")
    data = []
    with open("videos_list.txt", "r") as f:
        data = f.readlines()
    print(data)

    progress = sly.Progress("Processing", len(data))
    for url in data:
        normalized_url = url.strip()
        if normalized_url != "":
            try:
                download(normalized_url)
            except Exception as e:
                sly.logger.warn(repr(e))
        progress.iter_done_report()


if __name__ == "__main__":
    main()

exit(0)
# youtube-dl -f best -a videos_list.txt

#     local_path = os.path.join("src", sly.fs.get_file_name_with_ext(remote_path))
#     api.file.download(team_id, remote_path, local_path)

#     # result_name = (
#     #     sly.fs.get_file_name(local_path)
#     #     + "_youtube"
#     #     + sly.fs.get_file_ext(local_path)
#     # )
#     local_result_path = os.path.join("src", result_name)
#     paste_logo(local_path, local_result_path)

#     remote_result_path = os.path.join(os.path.dirname(remote_path), result_name)
#     if api.file.exists(team_id, remote_result_path) is True:
#         api.file.remove(team_id, remote_result_path)
#     api.file.upload(team_id, local_result_path, remote_result_path)

#     sly.fs.silent_remove(local_path)
#     sly.fs.silent_remove(local_result_path)

#     progress.iter_done_report()

# print("Done")
# if sly.is_production():
#     task_id = sly.env.task_id()
#     file_info = api.file.get_info_by_path(team_id, remote_result_path)
#     api.task.set_output_directory(task_id, file_info.id, remote_dir)
