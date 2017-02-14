import json
import socket
import sys
import urllib2

from prettytable import PrettyTable


def load_credentials():
    client_id = 'nZ89l3yiybiRCT80HpGvTPD1mmpQBHGrdwUW9R2x8B5DXfSMvED7Xf-TQ_v0BHbm'
    client_secret = 'gBd2C3WG4rY_Obh1IxVklikQfLvalrVD6jpYVthIWME1L7irb0hZt-joUidsN7IgQ7KQTcx3A5jKMFiNj84IzA'
    client_access_token = 'yxXuSkNFSQy4eMexworytckrwaC7XbLW6KyFaMPFE7qUZ7FnNyIH4gsYQjScQWSF'
    return client_id, client_secret, client_access_token


def search(search_term, client_access_token):
    # Unfortunately, looks like it maxes out at 50 pages (approximately
    # 1,000 results), roughly the same number of results as displayed on
    # web front end
    page = 1
    try:
        querystring = "http://api.genius.com/search?q=" + \
                      urllib2.quote(search_term) + "&page=" + str(page)
        request = urllib2.Request(querystring)
        request.add_header(
            "Authorization", "Bearer " + client_access_token)
        # Must include user agent of some sort, otherwise 403 returned
        request.add_header(
            "User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")
        # timeout set to 4 seconds; automatically retries if times
        # out
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
        json_obj = json.loads(raw.decode("utf-8"))
        body = json_obj['response']['hits']
        list_of_all_songs = []
        track_table = PrettyTable(
            ['Track Id', 'Track Name', 'Primary Artist'])
        for result in body:
            song_details = []
            result_id = result["result"]["id"]
            title = result["result"]["title"]
            primaryartist_name = result["result"]["primary_artist"]["name"]
            song_details.insert(0, result_id)
            song_details.insert(1, title)
            song_details.insert(2, primaryartist_name)
            list_of_all_songs.append(song_details)
            track_table.add_row(
                [result_id, title, primaryartist_name])
        print track_table
    except socket.timeout:
        print 'Connection timed out, try again'


def main():
    # so you can input searches from command line if you want
    arguments = sys.argv[1:]
    search_term = arguments[0].translate(None, "\'\"")
    client_id, client_secret, client_access_token = load_credentials()
    search(search_term, client_access_token)


if __name__ == '__main__':
    main()
