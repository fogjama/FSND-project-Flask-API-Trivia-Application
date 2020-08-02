# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Documentation

### Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the IDs and the values are the category names
- Request arguments: None
Sample request:
```
curl -X GET http://127.0.0.1:5000/categories
```

Sample response: 
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET '/questions?page={page}'
- Fetches a paginated list of question objects with 10 questions per page
- Request arguments: Optional page argument of type integer (defaults to 1 if absent)
- Returns: a list of category strings, a list of question dictionary objects, total number of questions in database, and a default current category.
Sample request:
```
curl -X GET http://127.0.0.1:5000/questions?page=2
```

Sample response:
```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### GET '/questions/{question_id}'
- Fetches a single question dictionary object by its ID
- Request Arguments: None
- Returns: A dictionary object containing question ID, question string, answer string, category string, and difficulty integer
Sample response:
```
curl -X GET http://127.0.0.1:5000/questions/10
```

Sample response:
```
{
  "answer": "Brazil",
  "category": "6",
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?",
  "success": true
}
```

### DELETE '/questions/{question_id}'
- Deletes a single question from the database by its ID
- Request Arguments: None
- Returns: ID of deleted question on success
Sample request:
```
curl -X DELETE http://127.0.0.1:5000/questions/20
```

Sample response:
```
{
    'success': True,
    'deleted': 20
}
```

### POST '/questions'
- Creates a new question from a JSON string
- Expected keys:
    ```
        question: string
        answer: string
        category: string (category id)
        difficulty: integer (1 to 5)
    ```
Sample request:
```
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the largest organ in the human body?","answer": "The skin", "category": "1", "difficulty":1}' http://127.0.0.1:5000/questions
```

Sample response:
```
{
    'success': True
}
```

### POST '/questions/{search_term}'
- Fetches a list of questions containing a {search_term} in the question string
- Request Arguments: None
Sample request:
```
curl -X POST http://127.0.0.1:5000/questions/title
```

Sample response:
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true
}
```

### GET '/categories/{category_id}/questions'
- Fetches a list of all questions for a specified category ID
- Request Arguments: None

Sample request:
```
curl -X GET http://127.0.0.1:5000/categories/2/questions
```

Sample response:
```
{
  "current_category": "3",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### POST '/quizzes'
- Fetches a random question from the bank of available remaining questions
- Expects:
    ```
        {
            'previous_questions': [list of question IDs],
            'quiz_category': {
                'type': category name as string, or "click"
                'id': category id as string, or "0"
            }
        }
    ```
Sample request:
```
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Science","id":"1"}}' http://127.0.0.1:5000/quizzes
```

Sample response:
```
{
  "question": {
    "answer": "One",
    "category": "2",
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}
```

## Errors
Error Code | Description
-----------|------------
400 | Bad request, often due to incorrect parameters
404 | Resource not found
405 | Method not allowed for endpoint
422 | Cannot process request
500 | Internal server error


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```