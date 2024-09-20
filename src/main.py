from __future__ import unicode_literals
import os
import yt_dlp
import supervisely as sly
import src.globals as g
from typing import List

from supervisely import handle_exceptions


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


def download_urls(urls):
    try:
        with yt_dlp.YoutubeDL(g.opts) as ydl:
            ydl.download(urls)
    except Exception as e:
        sly.logger.error(
            f"An error occurred while downloading a video.", extra={"exception message": str(e)}
        )
        raise RuntimeError(f"An error occurred while downloading a video.")


def upload_videos(dataset_id, names):
    paths = [os.path.join(g.output_dir, name) for name in names]
    try:
        video_infos = g.api.video.upload_paths(
            dataset_id=dataset_id,
            names=names,
            paths=paths,
            progress_cb=g.PROGRESS.iters_done_report,
        )
        g.videos_uploaded = True
    except Exception as e:
        sly.logger.error("Error while uploading videos.", extra={"exception": str(e)})
        raise RuntimeError("Error while uploading videos.")
    finally:
        (sly.fs.silent_remove(path) for path in paths)


@handle_exceptions
def main():
    project = g.api.project.create(
        workspace_id=g.workspace_id,
        name=sly.fs.get_file_name(g.remote_path),
        type=sly.ProjectType.VIDEOS,
        change_name_if_conflict=True,
    )
    dataset = g.api.dataset.create(project.id, "YouTube Videos", change_name_if_conflict=True)

    sly.logger.info("Downloading videos...")
    download_urls(get_urls())
    sly.logger.info("Successfully downloaded videos, uploading...")

    upload_videos(dataset.id, os.listdir(g.output_dir))
    if not g.videos_uploaded:
        raise RuntimeError("No videos were uploaded.")
    sly.logger.info("Finished uploading videos.")

    if sly.is_production():
        task_id = sly.env.task_id()
        g.api.task.set_output_project(task_id, project.id, project.name)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
