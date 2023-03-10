from __future__ import unicode_literals
from dotenv import load_dotenv
import os
import re
from pytube import YouTube
import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()
team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

downloaded_video = None
download_progress = None

# def get_youtube_id(link):

#     assert link.startswith("https://www.youtube.com/"), "Invalid YouTube link. Please use desktop format of url starting with 'https://www.youtube.com/...'"
#     try:
#         # Extract the video ID from the link using regular expressions
#         video_id = re.search(r'(?<=v=)[^&#]+', link).group(0)
#     except AttributeError:
#         # If the regular expression doesn't match, raise an exception with a custom error message
#         raise ValueError("Invalid YouTube link.")

#     print(f'Youtube ID is {video_id}')
#     return video_id


def download(url, output_dir="data/"):
    global downloaded_video
    yt = YouTube(str(url))
    stream = yt.streams.get_highest_resolution()
    # video_path = output_dir + f"/{get_youtube_id}."
    downloaded_video = stream.download(output_path=output_dir)


def main():
    global download_progress

    remote_path = sly.env.file()
    local_save_path = os.path.join("src", sly.fs.get_file_name_with_ext(remote_path))
    api.file.download(team_id, remote_path, local_save_path)

    project = api.project.get_or_create(
        workspace_id=workspace_id,
        name=sly.fs.get_file_name(remote_path),
        type=sly.ProjectType.VIDEOS,
    )

    dataset = api.dataset.create(project.id, "YouTube Videos", change_name_if_conflict=True)

    data = []

    with open(local_save_path, "r") as f:
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
                # ln -s /Users/germanvorozko/work-apps/supervisely/supervisely ./supervisely
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

    sly.fs.silent_remove(local_save_path)

    print("Done")
    if sly.is_production():
        task_id = sly.env.task_id()
        api.task.set_output_project(task_id, project.id, project.name)


if __name__ == "__main__":
    main()


# youtube-dl -f best -a videos_list.txt
