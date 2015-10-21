import math, time, json, urllib2, random
from pyechonest import config, song

# easy_install -U pyechonest

rgb = 0
sC = 0
beats = [0] * 1000 # beat offsets in seconds from start
currentArtist = ""
currentTrackname = ""
currentStartTime = 0
currentEndTime = 0
currentBeatCount = 0

def sonos(dT, fr):
    global rgb

    c = 0
    for i in range(0, currentBeatCount):
        off = beats[i] - (dT - currentStartTime)
        if off > 0 and off < 1: c = off

    for i in range(0, sC):
        rgb[i * 3 + 0] = c
        rgb[i * 3 + 1] = c
        rgb[i * 3 + 2] = c
    return rgb

def getSonosTrack():

    return

def loadDataForTrack(a, t):
    global currentArtist, currentTitle, currentStartTime, currentEndTime, currentBeatCount
    global beats, config, song

    # move this to one-time setup
    config.ECHO_NEST_API_KEY="99EYQBTMXDJJA32N8"

    currentArtist = a
    currentTitle = t
    sr = song.search(artist = currentArtist, title = currentTitle)
    sng = sr[0] # grab the first results, eyes closed

    currentStartTime = time.time()
    currentEndTime = time.time() + sng.audio_summary['duration']

    url = sng.audio_summary['analysis_url']
    response = urllib2.urlopen(url)
    analysis_json = json.load(response)
    i = 0
    for beat in analysis_json['beats']:
        beats[i] = beat['start']
        i = i + 1
    currentBeatCount = i
    return

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3

    getSonosTrack()
    loadDataForTrack('John Tejada', 'Unstable Condition')

    app.register_generator('sonos', sonos)
