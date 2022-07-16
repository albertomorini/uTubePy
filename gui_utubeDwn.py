import PySimpleGUI as sg
import platform
import darkdetect
import sys

sys.path.insert(0, '.')
import pyt_dwn as pytDwn
##########################################################################################

#convert the GUImode(video,audio,both) for the non-gui script.
def modeConverter(values):
	if(values.get(0)):
		#audio
		return "A"
	elif(values.get(1)):
		#video
		return "V"
	else:
		#audio&&video
		return "B"

def addVideoToQueue(queueVideo, values):
	if((values.get("url") != None or values.get("url")!='' ) and values.get("res") != None):
		queueVideo[values.get("url")]={
			"res":values.get("res"),
			"mode":modeConverter(values)
		}
	else:
		sg.SystemTray.notify('ERROR!', "The fields can't be empty")

	return queueVideo

def startDownloading(queueVideo):
	
	bgColor="#202020"
	colorButton=('white',"#585858")

	layout = [
	[sg.Text('downloading:',font=("Helvetica 23"), background_color=bgColor)],
	[sg.Output(key="output",size=(80,20),font=("Helvetica 17"))]
	]
	window = sg.Window('pYouTube downloading', layout, background_color=bgColor,finalize=True)


		
	for i in queueVideo:
		pytDwn.processQueue(queueVideo)

		event,values=window.read()
		if event == sg.WIN_CLOSED:
			break
			window.close()



####### GUI

def mainGUI():
	bgColor="#202020"
	colorButton=('white',"#585858")

	radio_choices = ['Only audio', 'Only video', 'Audio and video']

	layout = [
	[sg.Text('Welcome on pYouTube downloader!',font=("Helvetica 23"), background_color=bgColor)],
	[sg.Text("Insert a youtube's url", font=("Helvetica 19"), background_color=bgColor),sg.Input(font=("Helvetica 19"),key="url")],

	[sg.Button("Check video",font=("Helvetica 15"))],
	#SELECTOR FOR RESOLUTION
	[sg.Text("Resolution", font="Helvetica 18",background_color=bgColor)],
	[sg.Combo([],size=(15,0),font="Helvetica 17",key="res")],
	#RADIO BUTTONS FOR MODE
	[[sg.Radio(text, 1,font=("Helvetica 17"),background_color=bgColor),] for text in radio_choices],

	#start queue
	[sg.Submit("Add to queue",font=("Helvetica 15"), button_color=colorButton)],
	[sg.Submit("Start downloading",font=("Helvetica 15"), button_color=colorButton)],

	]
	window = sg.Window('pYouTube-downloader', layout, background_color=bgColor)

	queueVideo = dict()
	while True:
		event,values=window.read()

		if event == "Check video":
			if(values.get("url") != ""):
				bfr = pytDwn.getResolutions(values.get("url"))
				window["res"].update(value='',values=bfr)

		if event == "Add to queue":
			addVideoToQueue(queueVideo,values)
			window["url"].update("")
			window["res"].update([])


		if event == "Start downloading":
			addVideoToQueue(queueVideo,values)
			window.close()
			startDownloading(queueVideo)

		if event == sg.WIN_CLOSED:
			break
			window.close()


mainGUI()

