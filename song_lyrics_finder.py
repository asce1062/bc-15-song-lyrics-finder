import json
import socket
import urllib2
import time
import sys

from time import sleep
from clint.textui import colored
from prettytable import PrettyTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SongLyricsFinder, Base

# application starts
Session = sessionmaker()

# ... later
engine = create_engine('sqlite:///song_lyrics.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Session.configure(bind=engine)

# instantiate database transactions
# A Session() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = Session()

# Static variables.
# API Key and API Endpoint
apikey_musixmatch = 'bbc2cd1c9f66b9294d130add1b3534c4'
apiurl_musixmatch = 'http://api.musixmatch.com/ws/1.1/'


def do_task():
    time.sleep(1)


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
        # raw = response.read()
        print colored.green("Starting", bold=12)
        all_data = ''
        while True:
            do_task()
            print '\b.',
            sys.stdout.flush()
            data = response.read(2048)
            if not data:
                break
            all_data += data
            sleep(0.4)
        print "\n"
        json_obj = json.loads(all_data.decode("utf-8"))
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
        print colored.yellow(track_table, bold=12)
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
        # raw = response.read()
        print colored.green("Starting", bold=12)
        all_data = ''
        while True:
            do_task()
            print '\b.'
            sys.stdout.flush()
            data = response.read(2048)
            if not data:
                break
            all_data += data
            sleep(0.4)
        print "\n"
        json_obj = json.loads(all_data.decode("utf-8"))
        body = len(json_obj["message"]["body"])
        if body == 0:
            print colored.red("No lyrics found", bold=12)
        else:
            print colored.cyan(json_obj["message"]["body"]["lyrics"]["lyrics_body"], bold=12)
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
        # raw = response.read()
        print colored.green("Starting", bold=12)
        all_data = ''
        while True:
            do_task()
            print '\b.',
            sys.stdout.flush()
            data = response.read(2048)
            if not data:
                break
            all_data += data
            sleep(0.4)
        print "\n"
        json_obj = json.loads(all_data.decode("utf-8"))
        body = json_obj["message"]["body"]["lyrics"]["lyrics_body"]
        if body == 0:
            print colored.red("No lyrics found", bold=12)
        else:
            song_found = SongLyricsFinder(song_id, body)
            session.add(song_found)
            session.commit()
            print colored.green("Song saved successfully.", bold=12)
    except socket.timeout:
        print ("Timeout raised and caught")


def song_clear():
    """
    song clear - Clear entire local song database.
    """
    try:
        # Drop all tables then recreate them.
        Base.metadata.drop_all(bind=engine)
        print colored.red("Database cleared successfully.", bold=12)
        Base.metadata.create_all(bind=engine)
    except:
        session.rollback()
