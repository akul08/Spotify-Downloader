from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json, requests
import subprocess

DEVELOPER_KEY = "AIzaSyCt3JVfcH5tRAYbBLoXEECJvmPnIf-xnGc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		developerKey=DEVELOPER_KEY)

	search_response = youtube.search().list(
		q=options.q,
		part="id,snippet",
		maxResults=options.m,
		).execute()
	
	mp4=options.mp4
	videos = []
	videos_id = []
	videos_name = []
	sno = 0
	
	thisisit = ''
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append("%d %s (%s)" % (sno, search_result["snippet"]["title"], search_result["id"]["videoId"]))
			videos_id.append(search_result["id"]["videoId"])
			videos_name.append(search_result["snippet"]["title"])
			sno += 1
			thisisit = search_result["id"]["videoId"]
	select = 0
	if len(videos):	
		print "Videos:\n", " \n".join(videos), "\n"
	if options.m > 1:
		select = input('Enter No. to Download : ')
		thisisit = str(videos_id[select])
	if not thisisit:
		return
	if mp4:
		link = 'http://youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com/watch?v=%s' % thisisit
		r = requests.get(link)
		try:
			data = json.loads(r.text)
			downloadlink = data['link']
			
		except ValueError:
			print 'Direct Downloading'
			from bs4 import BeautifulSoup as bs
			soup = bs(r.text)
			downloadlink = 'http://www.youtubeinmp3.com/download/%s' % soup.find(id='download')['href']
	
	else:
		from bs4 import BeautifulSoup as bs
		link = "http://www.youtubeinmp4.com/youtube.php?video=http://www.youtube.com/watch?v=%s" % thisisit
		r = requests.get(link)
		soup = bs(r.text)
		downloadlink = 'http://www.youtubeinmp4.com/%s' % soup.find(class_='downloadMP4')['href']
	
	print('Starting Automatic Download , Please wait while Download finishes.')
	if mp4:
		command = ['wget', '-c', '-q', '--show-progress', '--output-document=%s.mp3' % videos_name[select], downloadlink]
	else:
		command = ['wget', '-c', '-q', '--show-progress', '--output-document=%s.mp4' % videos_name[select], downloadlink]
	output = subprocess.call(command) # Downloading Song Using wget.	
	print 'Done! Have fun!!\n'

if __name__ == "__main__":
	argparser.add_argument("-q", help="Search term", default="Google")
	argparser.add_argument("-f", help="File having list of songs", default="")
	argparser.add_argument("-m", help="Max results", default=1)
	argparser.add_argument("-mp4", help="Download Mp4", default=1, action='store_false')
	args = argparser.parse_args()

	try:
		if not args.f:
			youtube_search(args)
		else:
			with open(args.f, 'r') as f:
				lines = f.readlines()
			for x in lines:
				args.q = x
				youtube_search(args)

	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
