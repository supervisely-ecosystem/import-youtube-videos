import supervisely as sly
from dotenv import load_dotenv
import os

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

remote_path = sly.env.file()
local_path = os.path.join("src", sly.fs.get_file_name_with_ext(remote_path))

output_dir = "data/"
sly.fs.mkdir(output_dir)


# def my_hook(d):
#     global downloaded_video
#     global download_progress

#     if d["status"] == "downloading":
#         if download_progress is None:
#             download_progress = sly.Progress(
#                 f"Downloading {d['filename']}", total_cnt=d["total_bytes"], is_size=True
#             )

#     download_progress.set_current_value(d["downloaded_bytes"], report=True)

#     if d["status"] == "finished":
#         downloaded_video = d["filename"]
#         download_progress.set_current_value(d["total_bytes"])


opts = {
    "format": "best",
    "continue": True,
    "outtmpl": output_dir + "%(uploader)s - %(title)s.%(ext)s",
    # "progress_hooks": [my_hook],
    # "no-progress": True,
    "quiet": True,
}


# downloaded_video = None
# download_progress = None
PROGRESS = None
videos_uploaded = False
