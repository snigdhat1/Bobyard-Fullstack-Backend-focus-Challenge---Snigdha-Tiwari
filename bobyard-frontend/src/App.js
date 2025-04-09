import './App.css';
import React, {useState, useEffect} from 'react';
import { format } from 'date-fns';

function App() {
  const[comment, setComment] = useState([])

  useEffect(() => {
    fetchData();
  }, [])

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/comments');
      const jsonData = await response.json();
      console.log('Fetched Data:', jsonData);
      const sortedData = [...jsonData].sort((a, b) => 
        a.author.localeCompare(b.author)
      );
      console.log('Sorted Data:', sortedData);
      setComment(sortedData);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  }
  return (
    <div className="App">
      <header className="App-header">
       <h2>Comments</h2>
      </header>
      <div>
        {comment.length === 0 ? (
          <p> No comments available </p>
        ):
          (
            comment.map((c) =>(
              <div className="comment-container">
                <h3>{c.author}</h3>
                <p>{c.text}</p>
                <p>Likes: {c.likes}</p>
                {c.image && <img src={c.image} alt=""></img>}
                <p>Date of comment: {format(new Date(c.date), 'MM/dd/yyyy')}</p>
              </div>
            ))
          )}
      </div>
    </div>
  );
}

export default App;
