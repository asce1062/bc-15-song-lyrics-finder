import json
import socket
import urllib2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from models import SongLyricsFinder

# application starts
Session = sessionmaker()

# ... later
engine = create_engine('sqlite:///song_lyrics.db')
Session.configure(bind=engine)

sess = Session()

# Static variables.
# API Key and API Endpoint
apikey_musixmatch = 'bbc2cd1c9f66b9294d130add1b3534c4'
apiurl_musixmatch = 'http://api.musixmatch.com/ws/1.1/'
db_name = 'song_lyrics.db'


# Returns a list of songs that match the criteria.
def song_find_name(search_name):
    querystring = apiurl_musixmatch + "track.search?q_track=" + search_name + "&apikey=" + apikey_musixmatch + "&json"
    try:
        request = urllib2.Request(querystring)
        # timeout set to 4 seconds; automatically retries
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
        json_obj = json.loads(raw.decode("utf-8"))
        body = len(json_obj["message"]["body"])
        song_list = []
        track_table = PrettyTable(['Track Id', 'Track Name', 'Primary Artist'])
        for result in body:
            song_details = []
            song_id = result['track']['track_id']
            song_name = result['track']['track_name']
            artist_name = result['track']['artist_name']
            song_details.insert(0, song_id)
            song_details.insert(1, song_name)
            song_details.insert(2, artist_name)
            song_list.append(song_details)
            track_table.add_row([song_id, song_name, artist_name])
        print track_table
    except socket.timeout:
        print 'connection time out, try again'

song_find_name('system of a down')


def song_find(search_term):
    querystring = apiurl_musixmatch + "track.lyrics.get?track_id=" + urllib2.quote(
        search_term) + "&apikey=" + apikey_musixmatch + "&format=plain"
    try:
        request = urllib2.Request(querystring)
        # timeout set to 4 seconds; automatically retries
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
        json_obj = json.loads(raw.decode("utf-8"))
        body = len(json_obj["message"]["body"])
        if body == 0:
            print "No lyrics found"
        else:
            print json_obj["message"]["body"]["lyrics"]["lyrics_body"]
    except socket.timeout:
        print ("Timeout raised and caught")


song_find('3657996')


def song_save(song_id):
    querystring = apiurl_musixmatch + "track.lyrics.get?track_id=" + urllib2.quote(
        song_id) + "&apikey=" + apikey_musixmatch + "&format=plain"
    try:
        request = urllib2.Request(querystring)
        # timeout set to 4 seconds; automatically retries
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
        json_obj = json.loads(raw.decode("utf-8"))
        body = json_obj["message"]["body"]["lyrics"]["lyrics_body"]
        if body == 0:
            print "No lyrics found"
        else:
            song_found = SongLyricsFinder(song_id, body)
            sess.add(song_found)
            sess.commit()
            print "Song saved successfully."
    except socket.timeout:
        print ("Timeout raised and caught")


song_save('3657996')


def song_clear(clear):
    print "Are you sure you want to clear the database?"
    raw_input("Enter yes or no")
    if clear == "yes":
        try:
            sess.execute(SongLyricsFinder.delete())
            sess.commit()
            print "Database cleared successfully."
        except:
            sess.rollback()
    else:
        print ("Database Intact")
