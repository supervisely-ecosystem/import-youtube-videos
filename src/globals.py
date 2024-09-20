import supervisely as sly
import os

api = sly.Api.from_env()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
remote_path = sly.env.file()


def my_hook(d):
    global downloaded_video
    global download_progress

    if d["status"] == "downloading":
        if download_progress is None:
            download_progress = sly.Progress(
                f"Downloading {d['filename']}", total_cnt=d["total_bytes"], is_size=True
            )

    download_progress.set_current_value(d["downloaded_bytes"], report=True)

    if d["status"] == "finished":
        downloaded_video = d["filename"]
        download_progress.set_current_value(d["total_bytes"])


output_dir = "data/"
sly.fs.mkdir(output_dir)
local_path = os.path.join("src", sly.fs.get_file_name_with_ext(remote_path))

download_options = {
    "format": "best",
    "continue": True,
    "outtmpl": output_dir + "%(uploader)s - %(title)s.%(ext)s",
    "progress_hooks": [my_hook],
    # "no-progress": True,
    "quiet": True,
}


downloaded_video = None
download_progress = None
PROGRESS = None
videos_cnt = 0
