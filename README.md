**Song Lyrics Finder**

- For this project, you will be expected to make use of [MusixMatch API](https://developer.musixmatch.com/)  or [RapGenius API](https://docs.genius.com/).

- As a user, I can perform the following operations:

1. `song find <search_query_string>` - Returns a list of songs that match the criteria.

2. `song view <song_id>` - View song lyrics based on it’s id. Should be optimized by checking if there’s a local copy before checking online.

3. `song save <song_id>` - Store song details and lyrics locally.

4. `song clear` - Clear entire local song database.
