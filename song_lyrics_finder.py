import json
import os
import socket
import urllib2

from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SongLyricsFinder, Base

# application starts
Session = sessionmaker()

# ... later
engine = create_engine('sqlite:///song_lyrics.db')
Session.configure(bind=engine)

session = Session()

# Static variables.
# API Key and API Endpoint
apikey_musixmatch = 'bbc2cd1c9f66b9294d130add1b3534c4'
apiurl_musixmatch = 'http://api.musixmatch.com/ws/1.1/'

os.system('cls' if os.name == 'nt' else 'clear')


# Returns a list of songs that match the criteria.
def search(search_term):
    """
    song find <search_query_string> - Returns a list of songs that match the criteria.
    """
    querystring = apiurl_musixmatch + "track.search?q_track=" + urllib2.quote(
        search_term) + "&apikey=" + apikey_musixmatch + "&format=plain"
    try:
        request = urllib2.Request(querystring)
        # timeout set 4 to seconds; automatically retries
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
        json_obj = json.loads(raw.decode("utf-8"))
        body = json_obj['message']['body']['track_list']
        list_of_all_songs = []
        track_table = PrettyTable(['Song ID', 'Song Name', 'Artist Name'])
        for result in body:
            song_details = []
            result_id = result['track']['track_id']
            title = result['track']['track_name']
            artist_name = result['track']['artist_name']
            song_details.insert(0, result_id)
            song_details.insert(1, title)
            song_details.insert(2, artist_name)
            list_of_all_songs.append(song_details)
            track_table.add_row(
                [result_id, title, artist_name])
        print track_table
    except socket.timeout:
        print 'Connection timed out, try again'


def song_view(song_id):
    """
    song view <song_id> - view song lyrics based on its ID.
    Should be optimized by checking if there's a local copy before
        searching online
    """
    querystring = apiurl_musixmatch + "track.lyrics.get?track_id=" + urllib2.quote(
        song_id) + "&apikey=" + apikey_musixmatch + "&format=plain"
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


def song_save(song_id):
    """
    song save <song_id> - Store song details and lyrics locally.
    """
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
            session.add(song_found)
            session.commit()
            print "Song saved successfully."
    except socket.timeout:
        print ("Timeout raised and caught")


def song_clear():
    """
    song clear - Clear entire local song database.
    """
    try:
        # Drop all tables then recreate them.
        Base.metadata.drop_all(bind=engine)
        print "Database cleared successfully."
        Base.metadata.create_all(bind=engine)
        print "Database recreated successfully."
    except:
        sess.rollback()
