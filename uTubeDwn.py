from pytubefix import YouTube
import moviepy.editor as mp
import os
import re
from pytube.innertube import _default_clients

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


########################################
#YouTube interface

# returns the title of the video w/out illegal char for OS
# @url -> the youtube video url
def getTitle(url):
	tmp = YouTube(url, use_oauth=True, allow_oauth_cache=True).title
	#remove character not allowed on file system
	tmp = re.sub(r'[^\w\s]', '', tmp)
	return tmp

# download only the video
# @resParam => the resolution wanted
# @nameOfFile => name to assign only to the video (tmp if both = video + audio)
def downloadVideo(url,resParam,folderDestination="./tmp/", nameOfFile="video"):
	print("Downloading the video")
	try:
		YouTube(url, use_oauth=True, allow_oauth_cache=True).streams.filter(res=str(resParam)+"p").first().download(output_path=folderDestination,filename=nameOfFile+'.mp4')
	except Exception as e:
		print("video or resolution aren't correct")
	print("done!")

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
#file handling

# merge video and audio downloaded
def mergeVideoAudio(url):
	print("Merging video and audio")
	audio = mp.AudioFileClip("./tmp/audio.mp4")
	video1 = mp.VideoFileClip("./tmp/video.mp4")
	final = video1.set_audio(audio)
    
    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")  # Correct indentation (same as the if statement)
        
	final.write_videofile("output/"+getTitle(url)+".mp4",codec='libx264' ,audio_codec='libvorbis')

def flushTmp():
	os.remove("./tmp/audio.mp4")
	os.remove("./tmp/video.mp4")
##################################################

def addVideoToQueue(queueVideo):
	url = input("\nInsert the video's url: ")
	print("pick a resolution of" + str(getResolutions(url)))
	resolution = input("Insert the resolution as a number (720/1080): ")
	mode = input("\n-----------\n\tA for only audio\n\tV for only video\n\tB for both\n->")

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

		elif(queueVideo.get(i).get("mode")=="V"):
			#just the video
			downloadVideo(i,queueVideo.get(i).get("res"),"./output/",getTitle(i))
		else:
			#both video and audio
			downloadVideo(i,queueVideo.get(i).get("res"))
			downloadAudio(i)
			mergeVideoAudio(i)
			flushTmp()

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
