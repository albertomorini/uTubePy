# pyTubeDownloader, a YouTube downloader.
Unlike the others YouTube downloader, pytDownloader allows you to download a video with higher resolutions (like 1080p or 4k)

## Usage:
YouTube (and other web videos provider) split audio and video, then we have to download video and audio in a separate way, next we can merge these two temp files (video.mp4,audio.mp4) in a single one.

`$ python3 gui_pytdwn.py`

---

## CLI version
`$ python3 pyt_dwn.py`
1) then put the url, next the resolution and last the mode (A=audio only, V=video only, B=both audio and video)
2) choose if add another video or start download
3) enjoy ;)

## Dependencies:
- os
- moviepy.editor
- pytube
- PySimpleGUI as sg
- platform
- darkdetect
- sys

> installable with pip3

## Output of GUI be like:

![Output example](https://github.com/albertomorini/albertomorini/blob/main/uTubeDownloader/img/1.png)
![Output example](https://github.com/albertomorini/albertomorini/blob/main/uTubeDownloader/img/2.png)
![Output example](https://github.com/albertomorini/albertomorini/blob/main/uTubeDownloader/img/3.png)
![Output example](https://github.com/albertomorini/albertomorini/blob/main/uTubeDownloader/img/4.png)
![Output example](https://github.com/albertomorini/albertomorini/blob/main/uTubeDownloader/img/5.png)

## TODO & Problems

* PyTube has a common issue ('NoneType' object has no attribute 'span') you can see it on their github page (https://github.com/pytube/pytube/issues).

	A solution is provided by @ifahadone, you need to replace a function into "/Users/alby/Library/Python/3.8/lib/python/site-packages/pytube/cipher.py" file.
	Here link: https://github.com/pytube/pytube/issues/1243#issuecomment-1032242549
