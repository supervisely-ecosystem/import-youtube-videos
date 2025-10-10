<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/204161277-3366a8b4-656f-4e59-9ecd-faa8033f60ff.jpg"/>  

# Import YouTube video

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Acknowledgement">Acknowledgement</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](../../../../supervisely-ecosystem/import-youtube-videos)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-youtube-videos)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/import-youtube-videos.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/import-youtube-videos.png)](https://supervisely.com)

</div>

# Overview

App iterates over all youtube url links in a *.txt* file and uploades listed videos to a platform in form of a project.

This app comes in handy when you want to work with videos from YouTube in the platform. The problem with that being is that YouTube does not allow for direct download, so you have to deal with sketchy services. Good thing is - the current app covers this issue.

# How to Run

0. Create *.txt* file with a list of YouTube links to videos that you would like to download, just like in the example shown below:

```md
https://www.youtube.com/watch?v=nuYLz1CjRf0
https://www.youtube.com/watch?v=psGDf2VrvK8
https://www.youtube.com/watch?v=M69gZrLm9oc
```

1. Go to Team Files
<img src="https://user-images.githubusercontent.com/115161827/202218609-485003e6-e295-4d3b-9bd5-fa302e43eea2.png" >

2. Upload *.txt* file that contains YouTube urls
<img src="https://user-images.githubusercontent.com/115161827/203781775-acde06c1-4035-4d74-a9b8-0386c0850f8c.gif">

3. Right click to file and run the app from the context menu
  <img src="https://user-images.githubusercontent.com/115161827/203782776-dc90fb85-05d8-4cc0-a761-6c18db4b4f16.gif">


## Result

As a result of running this app, project with all of your uploaded videos will appear in your workspace.

<img src="https://user-images.githubusercontent.com/115161827/203787133-aaea00c0-7246-40b9-9023-f4131e753e26.gif"  style='padding-top: 10px'>

# Acknowledgement
This app is based on the fork of the original `youtube-dl`([github](https://github.com/ytdl-org/youtube-dl)). ![GitHub Org's stars](https://img.shields.io/github/stars/ytdl-org/youtube-dl?style=social) library called `yt-dlp`. Check it out on [github](https://github.com/yt-dlp/yt-dlp). ![GitHub Org's stars](https://img.shields.io/github/stars/yt-dlp/yt-dlp?style=social)
