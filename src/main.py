from __future__ import unicode_literals
from dotenv import load_dotenv
import os
import supervisely as sly
import youtube_dl
import src.globals as g
from typing import List

from supervisely import handle_exceptions

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


def get_urls() -> List[str]:
    g.api.file.download(g.team_id, g.remote_path, g.local_path)
    urls = []
    with open(g.local_path, "r") as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]

    if len(urls) == 0:
        raise RuntimeError(
            "No urls found in the text file provided. Please, readme app overview and try again."
        )

    g.PROGRESS = sly.Progress("Processing", len(urls))
    sly.fs.silent_remove(g.local_path)
    return urls


def download(url: str):
    try:
        with youtube_dl.YoutubeDL(g.download_options) as ydl:
            ydl.download([url])
    except Exception as e:
        sly.logger.warn(f"An error occurred while downloading a video: {e}")


def upload(dataset_id):
    for video in os.listdir(g.output_dir):
        g.api.video.upload_path(
            dataset_id=dataset_id,
            name=sly.fs.get_file_name_with_ext(video),
            path=video,
            item_progress=True,
        )
        sly.fs.silent_remove(video)
        g.videos_cnt += 1
        g.PROGRESS.iter_done_report()


@handle_exceptions
def main():
    project = g.api.project.create(
        workspace_id=g.workspace_id,
        name=sly.fs.get_file_name(g.remote_path),
        type=sly.ProjectType.VIDEOS,
        change_name_if_conflict=True,
    )
    dataset = g.api.dataset.create(project.id, "YouTube Videos", change_name_if_conflict=True)

    urls = get_urls()
    sly.logger.info("Downloading videos...")
    (download(url) for url in urls)
    sly.logger.info(f"Successfully downloaded {len(urls)} videos, uploading...")
    upload(dataset.id)

    if g.videos_cnt == 0:
        raise RuntimeError("No videos were uploaded.")

    if sly.is_production():
        task_id = sly.env.task_id()
        g.api.task.set_output_project(task_id, project.id, project.name)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
