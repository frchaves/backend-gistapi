
Add mock tests instead of real data

docker build -t my-flask-app .

## gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.
The existing code already implements most of the Flask boilerplate for you.
The main functionality is left for you to implement.
The goal is to implement an endpoint that searches a user's Gists with a regular expression.
For example, I'd like to know all Gists for user `justdionysus` that contain the pattern `import requests`.
The code in `gistapi.py` contains some comments to help you find your way.

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

   
## Answers to strech goals and shortcomings

* Implement a few tests (using a testing framework of your choice)
 -> Used unittest and pytest
* In all places where it makes sense, implement data validation, error handling, pagination -> Done
* Migrate from `requirements.txt` to `pyproject.toml` (e.g. using [poetry](https://python-poetry.org/)) -> Done, 
 req2toml.py does this
* Implement a simple Dockerfile -> Done
* Implement handling of huge gists -> Could be improved with a task queue such as Celery.
* Set up the necessary tools to ensure code quality (feel free to pick up a set of tools you personally prefer) ->
* Document how to start the application, how to build the docker image, how to run tests, and (optionally) how to run code quality checkers

* Prepare a TODO.md file describing possible further improvements to the archtiecture:
    - Can we use a database? What for? SQL or NoSQL? -> A SQL database could be used to a relational data schema that could have tables such as users,
    gists of users, urls, etc. 
    - How can we protect the api from abusing it? -> Several options are available: 
    Rate Limiting, API Keys, Authentication and Authorization, Input Validation, Output Sanitization
    
    - How can we deploy the application in a cloud environment? -> 
    After containerizing the application we can use a cloud provider such as AWS, we can push it to a container registry
    such as Amazon ECR. We provision the necessary infrastructure using EC2s instances. 
    Set the security groups, load balancers and firewalls and finally deploy and test the container image.
    
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment?
    Monitor the application's logs, set up automated tests, set up alerts, load test the application and 
    use a health check endpoint
    
