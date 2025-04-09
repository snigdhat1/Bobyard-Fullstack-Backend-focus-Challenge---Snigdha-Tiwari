# Bobyard-Fullstack-Backend-focus-Challenge---Snigdha-Tiwari

# Prerequisites

Before setting up the backend, ensure you have the following installed:

- Python (3.7+)
- MySQL Server
- `pip` (Python package installer)

# To Install Dependencies
``` python -m venv venv ```
```source venv/bin/activate ```
``` pip install -r requirements.txt ```

# To Run the Backend
Create a .env file with the variable ```mysql+pymysql://user:password@localhost/db_name```
Once you have created the file, run the database.py file -> ```python database.py```
Then run ```uvicorn main:app --reload``` and go to http://127.0.0.1:8000/docs

# To Run the Frontend
Make sure you have node and npm installed:
```node -v```
```npm -v```
- cd into the ```bobyard-frontend``` folder and run ```npm install``` to install the dependencies
- run ```npm start```
