from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone
from typing import Optional, Annotated
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Define the Comment model
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100))
    text = Column(Text)
    date = Column(DateTime)
    likes = Column(Integer)
    image = Column(String(500))

# Create the tables in the database (if not already created)
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_connect = Annotated[Session, Depends(get_db)]
# API Endpoints
@app.post("/comments")
def create_comment(author: str, text: str,likes: int, db: db_connect, image: Optional[str] = None):
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    new_comment = Comment(
        author=author,
        text=text,
        date=utc_now,
        likes=likes,
        image=image or ""
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@app.get("/comments")
def get_comment(db: db_connect, id: int = None):
    if id:
        query = db.query(Comment).where(Comment.id == id).first()
        if not query: 
            raise HTTPException(status_code=404, detail="Comment not found")
        return query
    else:
        query = db.query(Comment).all()
        return query

@app.put("/comments")
def update_comment(id: int, db: db_connect, author: Optional[str] = None, text: Optional[str] = None, date: Optional[datetime]= None, likes: Optional[int] = None, image: Optional[str] = None):
    query = db.query(Comment).where(Comment.id == id).first()

    if not query: 
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if author is not None:
        query.author = author
    if text is not None:
        query.text = text
    if date is not None:
        query.date = date
    if likes is not None:
        query.likes = likes
    if image is not None:
        query.image = image
    
    # Commit the changes
    db.commit()
    db.refresh(query)
    return query

@app.delete("/comments")
def delete_comment(id: int, db: db_connect):
    query = db.query(Comment).where(Comment.id == id).first()

    if not query:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(query)
    db.commit()
    return {"message" : "Comment deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)