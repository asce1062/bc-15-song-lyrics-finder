from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# application starts
Session = sessionmaker()

# ... later
engine = create_engine('sqlite:///song_lyrics.db')
Session.configure(bind=engine)

sess = Session()
