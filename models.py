# The following are all of the standard imports that are needed to run the
# database
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# automap base
# The following is what will create the declarative_base base that will be
# imported to every table.
Base = declarative_base()


# The following is the local song lyrics finder table which will store the
# songs and their lyrics
class SongLyricsFinder(Base):
    __tablename__ = 'song_lyrics'

    id = Column(Integer, primary_key=True)
    # Use  song ID as index to speed up db search
    song_id = Column(String(16), nullable=False, unique=True, index=True)
    song_lyrics = Column(String(1062), nullable=False)

    def __init__(self, song_id, song_lyrics):
        self.song_id = song_id
        self.song_lyrics = song_lyrics


engine = create_engine('sqlite:///song_lyrics.db')

# Create all tables.
Base.metadata.create_all(engine)
