from __future__ import unicode_literals
from dotenv import load_dotenv
import os
import youtube_dl
import supervisely as sly

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

downloaded_video = None
download_progress = None


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
        print("Downloaded!")
        downloaded_video = d["filename"]
        download_progress.set_current_value(d["total_bytes"])


def download(url, output_dir="data/"):
    ydl_opts = {
        "format": "22",
        "continue": True,
        "outtmpl": output_dir + "%(uploader)s - %(title)s.%(ext)s",
        "progress_hooks": [my_hook],
        # "no-progress": True,
        "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    global download_progress

    remote_path = sly.env.file()
    local_path = os.path.join("src", sly.fs.get_file_name_with_ext(remote_path))
    api.file.download(team_id, remote_path, local_path)

    project = api.project.get_or_create(
        workspace_id=workspace_id,
        name=sly.fs.get_file_name(remote_path),
        type=sly.ProjectType.VIDEOS,
    )

    dataset = api.dataset.create(
        project.id, "YouTube Videos", change_name_if_conflict=True
    )

    data = []
    with open(local_path, "r") as f:
        data = f.readlines()

    output_dir = "data/"
    sly.fs.mkdir(output_dir)

    progress = sly.Progress("Processing", len(data))
    for url in data:
        normalized_url = url.strip()
        if normalized_url != "":
            try:
                print(f"Start {normalized_url}")
                download_progress = None
                download(normalized_url, output_dir)
                api.video.upload_path(
                    dataset_id=dataset.id,
                    name=sly.fs.get_file_name_with_ext(downloaded_video),
                    path=downloaded_video,
                    item_progress=True,
                )
                sly.fs.silent_remove(downloaded_video)
                print(f"Finish {normalized_url}")
            except Exception as e:
                sly.logger.warn(repr(e))
        progress.iter_done_report()

    sly.fs.silent_remove(local_path)

    print("Done")
    if sly.is_production():
        task_id = sly.env.task_id()
        api.task.set_output_project(task_id, project.id, project.name)


if __name__ == "__main__":
    main()


# youtube-dl -f best -a videos_list.txt
