import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  page_questions = questions[start:end]

  return page_questions


def adjust_category_id(cat_id):
  adjusted_cat_id = str(int(cat_id) + 1)

  return adjusted_cat_id

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''
  CORS(app, resources={r'*': {'origins': '*'}})

  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE')
    return response

  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  # '''
  @app.route('/categories', methods=['GET'])
  def categories():
    c_query = Category.query.all()
    categories = []
    for c in c_query:
      categories.append(c.type)

    return jsonify({
      'success': True,
      'categories': categories
    })


  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''

  @app.route('/questions', methods=['GET'])
  def get_question_list():
    selection = Question.query.order_by(Question.id).all()
    questions = paginate_questions(request, selection)
    
    total_questions = len(Question.query.all())
    
    c_query = Category.query.all()
    categories = []
    for c in c_query:
      categories.append(c.type)

    current_category = categories[0]

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': total_questions,
      'categories': categories,
      'current_category': current_category
    })


  @app.route('/questions/<question_id>', methods=['GET'])
  def get_question(question_id):

    try:
      q = Question.query.filter_by(id=question_id).one_or_none()
        
      if q == None:
        abort(404)
      
      print(q, file=sys.stderr)

      return jsonify({
        'id': q.id,
        'question': q.question,
        'answer': q.answer,
        'category': q.category,
        'difficulty': q.difficulty
      })
    except:
      abort(422)


  # '''
  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 
  # '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_quest(question_id):

    try:
      q = Question.query.filter_by(id=question_id).one_or_none()

      if q == None:
        abort(404)

      q.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)

  # '''
  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  # '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    question = request.get_json()

    try:
      new_question = Question(
        question=question['question'],
        answer=question['answer'],
        category=question['category'],
        difficulty=question['difficulty']
      )

      new_question.insert()

      return jsonify({
      'success': True
    })

    except Exception as e:
      print(f'Exception: --> {e}', file=sys.stderr)
      abort(422)


  # '''
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
  # '''
  @app.route('/questions/<search_term>', methods=['POST'])
  def search_questions(search_term):
    selection = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
    questions = [question.format() for question in selection]

    return({
      'success': True,
      'questions': questions
    })

  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def get_questions(category_id):
    cat_id = adjust_category_id(category_id)
    selection = Question.query.filter_by(category=cat_id).all()
    questions = [question.format() for question in selection]

    return({
      'success': True,
      'questions': questions,
      'total_questions': len(questions),
      'current_category': cat_id
    })


  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''
  @app.route('/quizzes', methods=['POST'])
  def play_game():

    body = request.get_json()

    try:
      previous_questions = body['previous_questions']
      quiz_category = body['quiz_category']

      if quiz_category['type'] == 'click':
        available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        cat_id = adjust_category_id(quiz_category['id'])
        available_questions = Question.query.filter(Question.category==cat_id).filter(Question.id.notin_(previous_questions)).all()

      question_bank = [q.format() for q in available_questions]

      if len(question_bank) == 0:
        question = None
      else:
        question = question_bank[random.randrange(0, len(available_questions))]


      return jsonify({
        'success': True,
        'question': question
      })
    
    except:
      abort(422)


  # '''
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404


  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Cannot process request'
    }), 422
  

  return app

    