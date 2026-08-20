# pip install yt-dlp
import os
import re
from pathlib import Path

import yt_dlp

########################################
#YouTube interface

# returns the title of the video w/out illegal char for OS
# @url -> the youtube video url
def getTitle(url):
    print("Getting title...")
    options = {
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info["title"]
    title = re.sub(r'[^\w\s.-]', '', title)
    return title.strip()



# download only the audio
def downloadAudio(url, folderDestination="./output/"):
    print("Downloading audio...")

    try:
        Path(folderDestination).mkdir(parents=True, exist_ok=True)

        options = {
            "format": "bestaudio/best",
            "outtmpl": str(
                Path(folderDestination) / "%(title)s.%(ext)s"
            ),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                }
            ],
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        print("Downloaded!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False



# reutrns a list of resolutions available of the video
def getResolutions(url):
	availableRes= set()#remove the duplicated
	for i in YouTube(url, use_oauth=True, allow_oauth_cache=True).streams.all():
		if(i.resolution!=None):
			availableRes.add(int(i.resolution.split("p")[0]))
	return sorted(availableRes)

##################################################

##################################################

def addVideoToQueue(queueVideo):
	url = input("\nInsert the video's url: ")
	#print("pick a resolution of" + str(getResolutions(url)))
	resolution = 720 #1080 #input("Insert the resolution as a number (720/1080): ")
	mode = "A" #input("\n-----------\n\tA for only audio\n\tV for only video\n\tB for both\n->")

	queueVideo[url]={
		"res": resolution,
		"mode": mode
	}
	return queueVideo

def processQueue(queueVideo):
    for url, options in queueVideo.items():
        title = getTitle(url)
        print(f"\nProcessing: {title}")
        if options["mode"] == "A":
            downloadAudio(url,"./output/")


		

def showQueue(queueVideo):
	for i in queueVideo:
		print(getTitle(i))
		print(queueVideo.get(i).get("res"))
		if(queueVideo.get(i).get("mode")=="A"):
			print("Audio only")
		elif(queueVideo.get(i).get("mode")=="V"):
			print("Video only")
		else:
			print("Audio and video")


def main():
	print("Welcome on uTube Downloader ;)")

	queueVideo = dict()
	choice = 1
	while int(choice)!=0:
		queueVideo=addVideoToQueue(queueVideo)
		choice = input("To add another video press 1, to download the queue press 0:  ")

	print(queueVideo)
	processQueue(queueVideo)

	print("Done!\n your files are in output folder, bye ;)")

main()
