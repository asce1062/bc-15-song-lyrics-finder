#Song Lyrics Finder.

![song lyrics finder ui](https://i.imgur.com/wSjNUJN.png) 

**PROBLEM STATEMENT:**

- For this project, you will be expected to make use of [MusixMatch API](https://developer.musixmatch.com/) or [RapGenius API](https://docs.genius.com/).

- As a user, I can perform the following operations:

1. `song find <search_query_string>` - Returns a list of songs that match the criteria.

2. `song view <song_id>` - View song lyrics based on it’s id. Should be optimized by checking if there’s a local copy before checking online.

3. `song save <song_id>` - Store song details and lyrics locally.

4. `song clear` - Clear entire local song database.

**GETTING STARTED:**

1. Clone Repo:

    ```
    $ git clone https://github.com/asce1062/bc-15-song-lyrics-finder.git
    ```
    ```
    $ cd bc-15-song-lyrics-finder
    ```

2.  Activate your virtualenv. _if you're "that" kind of guy (lol)_

3. Install requiremets

    ```
    $ pip install -r requirements.txt
    ```
4. Create local database in same directory

    ```
    $ python models.py
    ```

5. Run 

    ```
    $ python main.py
    ```
**USAGE:**
 
- ```find <query>``` - Finds the top 10 artists based on query and returns Song ID, Song Name and Artist Name._Song ID will be used to find lyrics_
 
    *Usage*: ```find BYOB``` should display top 10 performances with the tittle **BYOB**.
- ```view <query>``` - Displays the Lyrics based on Song ID entered.
    
    *Usage*: ```find 3657996``` search and display lyrics using the song IDs generated from ```find BYOB```. In this case **BYOB** by **System of a Down** who's song ID is **3657996**
- ```save <query>``` - saves the song to a local database ```song_lyrics.db```.
    
    *Usage*: : ```save 3657996``` will save **BYOB** by **System of a Down** to the local database.
- ```cear``` - Clear the entire local database.
 
    *Usage* : ```clear``` will clear entire local database.
 