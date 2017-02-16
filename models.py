"""
http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
"""
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
    # Here we define columns for the table song_lyrics
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    song_id = Column(String(200), nullable=False)
    song_lyrics = Column(String(1062), nullable=False)

    def __init__(self, song_id, song_lyrics):
        self.song_id = song_id
        self.song_lyrics = song_lyrics

# Create an engine that stores data in the local directory's
# song_lyrics.db file.
engine = create_engine('sqlite:///song_lyrics.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
