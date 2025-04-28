# from pytubefix import YouTube
# pip install yt-dlp
import os
import re

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

from pytubefix import YouTube
from pytubefix import request
from pytubefix import extract
from pytubefix.innertube import _default_clients
from pytubefix.exceptions import RegexMatchError

ssl._create_default_https_context = ssl._create_unverified_context


########################################
#YouTube interface

# returns the title of the video w/out illegal char for OS
# @url -> the youtube video url
def getTitle(url):
	tmp = YouTube(url, use_oauth=True, allow_oauth_cache=True).title
	#remove character not allowed on file system
	tmp = re.sub(r'[^\w\s]', '', tmp)
	return tmp

# download only the audio
def downloadAudio(url, folderDestination="./tmp/", nameOfFile="audio"):
	print("Downloading the audio")
	try:
		YouTube(url, use_oauth=True, allow_oauth_cache=True).streams.filter(only_audio=True).first().download(output_path=folderDestination,filename=nameOfFile+".mp4")
	except Exception as e:
		print("url doesn't exists or there isn't audio in the video/video quality")
	print("done!")

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
	resolution = 1080 #input("Insert the resolution as a number (720/1080): ")
	mode = "A" #input("\n-----------\n\tA for only audio\n\tV for only video\n\tB for both\n->")

	queueVideo[url]={
		"res": resolution,
		"mode": mode
	}
	return queueVideo

def processQueue(queueVideo):
	for i in queueVideo:
		print("Processing: "+getTitle(i))

		if(queueVideo.get(i).get("mode")=="A"):
			#just the audio
			downloadAudio(i,"./output/",getTitle(i))

		

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
