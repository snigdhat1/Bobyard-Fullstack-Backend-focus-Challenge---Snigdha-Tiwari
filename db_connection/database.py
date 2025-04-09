import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

# creating the database comments model 
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    author = Column(String(100))
    text = Column(Text)
    date = Column(DateTime)
    likes = Column(Integer)
    image = Column(String(500))  


# creating the connection to the database

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Load comments from the JSON file
def load_comments_from_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)

# Insert comments into the database
def insert_comments_to_db(db, data):
    for comment in data["comments"]:
        comment_obj = Comment(
            id=int(comment["id"]),
            author=comment["author"],
            text=comment["text"],
            date=datetime.fromisoformat(comment["date"].replace("Z", "+00:00")),  # Correct date format
            likes=comment["likes"],
            image=comment.get("image", "")
        )
        db.add(comment_obj)
    db.commit()


def load_and_insert_comments(db, json_file_path):
    comments_data = load_comments_from_json(json_file_path)
    insert_comments_to_db(db, comments_data)

# Load comments and insert them on startup or script run
load_and_insert_comments(session, '../comments.json')

session.close()
print("All data inserted")
