
# StreamAgain.com Plugin for Plex Media Center

PREFIX = "/video/streamagain"
NAME = "StreamAgain Plugin"

DOMAIN = 'streamagain.com'

MAIN = 'https://' + DOMAIN + '/api/v1/'

MOVIESMAIN = MAIN + 'discover/movies?from=0&to=50'
MOVIESLATEST = MOVIESMAIN + '&sort=added_on&quality=all&genre=all'
MOVIESTRENDING = MOVIESMAIN + '&sort=trending&quality=all&genre=all'
MOVIESNEWRELEASES = MOVIESMAIN + '&sort=release_date&quality=all&genre=all'

MOVIELINK = 'https://video9.sit2play.com%s'

CACHETIME = 300

COOKIE = None
AUTHCODE = None
PREMIUM = False

def Start():
	Log.Debug("Starting streamagain plugin")
	ObjectContainer.title1 = NAME

@handler(PREFIX, NAME)
def MainMenu():
	Log.Debug("Loading Main Menu")
	if not Prefs['cookie']: return MediaContainer(no_cache=True, message="Login Failed.")

	oc = ObjectContainer()
	#oc.add(DirectoryObject(key=Callback(TV), title="TV"))
	oc.add(DirectoryObject(key=Callback(Movies), title="Movies"))
	return oc


@route(PREFIX + '/movies')
def Movies(url=None, title='Movies'):
	oc=ObjectContainer(title1=title)

	if not url:
		oc.add(DirectoryObject(key=Callback(Movies, url=MOVIESLATEST), title = "Order by Latest"))
		oc.add(DirectoryObject(key=Callback(Movies, url=MOVIESNEWRELEASES), title = "Order by New Releases"))
		oc.add(DirectoryObject(key=Callback(Movies, url=MOVIESTRENDING), title = "Order by Trending"))

		return oc

	#req = HTML.ElementFromString(HTTP.Request(url,cacheTime = CACHETIME,headers = Header(referer=MAIN)).content)
	data = JSON.ObjectFromURL(url, headers=Header())
	numTitles = data['total']

	for movie in data['listings']:
		thisTitle = movie['title']
		thisFileID = moive['imdb_id']
		oc.add(DirectoryObject(
			key=Callback(MovieDetail, title=thisTitle, fileId=thisFileId),
			title = thisTitle))

	return oc


#https://streamagain.com/api/v1/discover/movies?from=0&to=50&sort=added_on&quality=all&genre=all
#@route(PREFIX + '/detail')
def MovieDetail(title, fileId):
	url = MAIN + 'title/' + fileId
	data = JSON.ObjectFromURL(url)
	oc = ObjectContainer(title1 = title)
	link = data['links']['links']['720p']
	oc.add(VideoClipObject(title = "720p", url = CreateURL(link)))
	###
	#create directory for trailers
	###
	return oc

def Header(referer=None, host=DOMAIN):
	headers = {
			"User-Agent":        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
		}
	if COOKIE:
		headers['Cookie'] = COOKIE
	return headers


def GetCookie(name):
	if not COOKIE:
		return None
	cookies = COOKIE.split("; ")
	for cookie in cookies:
		key, val = cookie.split("=")
		if key == name:
			return val
	return None

def Login():
	global COOKIE


	logged_in = False
	page = None


	if not Prefs['cookie']:
		return False # we can't login if we don't have a cookie
	else:
		COOKIE = Prefs['cookie']
		return True


def CreateURL(file):
	return MOVIELINK % (
		file)
