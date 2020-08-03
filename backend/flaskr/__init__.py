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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE')
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        c_query = Category.query.all()
        categories = {}
        for c in c_query:
            categories[c.id] = c.type

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/questions', methods=['GET'])
    def get_question_list():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

        total_questions = len(Question.query.all())

        c_query = Category.query.all()
        categories = {}
        for c in c_query:
            categories[c.id] = c.type

        current_category = categories[1]

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

            if q is None:
                abort(404)

            return jsonify({
                'success': True,
                'id': q.id,
                'question': q.question,
                'answer': q.answer,
                'category': q.category,
                'difficulty': q.difficulty
            })
        except BaseException:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_quest(question_id):

        try:
            q = Question.query.filter_by(id=question_id).one_or_none()

            if q is None:
                abort(404)

            q.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except BaseException:
            abort(404)

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

    @app.route('/questions/<search_term>', methods=['POST'])
    def search_questions(search_term):
        selection = Question.query.filter(
            Question.question.ilike(
                '%' + search_term + '%')).all()

        if len(selection) == 0:
            questions = None
        else:
            questions = [question.format() for question in selection]

        return jsonify({
            'success': True,
            'questions': questions
        })

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_questions(category_id):

        selection = Question.query.filter_by(category=category_id).all()
        questions = [question.format() for question in selection]

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def play_game():

        body = request.get_json()

        try:
            previous_questions = body['previous_questions']
            quiz_category = body['quiz_category']

            if quiz_category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                cat_id = quiz_category['id']
                available_questions = Question.query.filter(
                    Question.category == cat_id).filter(
                    Question.id.notin_(previous_questions)).all()

            question_bank = [q.format() for q in available_questions]

            if len(question_bank) == 0:
                question = None
            else:
                question = question_bank[random.randrange(
                    0, len(available_questions))]

            return jsonify({
                'success': True,
                'question': question
            })

        except BaseException:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Bad request'
        }), 400

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

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    return app
