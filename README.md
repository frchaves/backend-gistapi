## gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.
There is an endpoint that searches a user's Gists with a regular expression.
For example, what are all the Gists for user `justdionysus` that contain the pattern `import requests`.

### Tech Stack:
- Python (Flask, Pytest)
- Docker


### Setup:
- Clone the project to a folder (_**https://github.com/frchaves/backend-gistapi**_)
- Open the terminal in the project folder (/backend-coding-challenge)
- Run the application with Docker:
  - `docker build -t my-flask-app .` to create the image 
  - `docker run -p 5000:5000 my-flask-app` to run the image
  
- Test the application with Postman, curl:
  - An example of a POST request would be
    {
    "username":"justdionysus",
    "pattern": "import requests"
    }.
    Where the response would be:
    `
    {
    "matches": [
        {
            "file_name": "john_waters.py.nosecrets",
            "url": "https://gist.github.com/65e6162d99c2e2ea8049b0584dd00912"
        }
    ],
    "pattern": "import requests",
    "status": "success",
    "username": "justdionysus"
}
`

### Run the tests inside Docker:
  - Access the django container with `docker-compose exec web bash`
  - Cd into /app/gistapi/tests, run pytest (pytest tests -v)

   
    
