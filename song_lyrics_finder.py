import json
import socket
import urllib2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


def song_find(search_term):
    while True:
        querystring = apiurl_musixmatch + "track.lyrics.get?track_id=" + urllib2.quote(
            search_term) + "&apikey=" + apikey_musixmatch + "&format=plain"
        while True:
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
                continue
            break


song_find('3657996')
