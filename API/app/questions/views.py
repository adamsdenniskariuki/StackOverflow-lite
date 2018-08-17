import json
from datetime import datetime
from flask import request, jsonify, abort
from . import questions
from app.data import data

def locate(id, items):
    """This function takes 2 arguments (id : int and items : string)
        To locate the item, question or user, with the identifier, id, 
        from the collection of items: either questions or users."""
    collection = data[items]
    required_item = {}
    found = False
    index = 0
    for i in range(len(collection)):
        if int(collection[i]['id']) == int(id):
            required_item = collection[i]
            found = True
            index = i
    if found:
        return (required_item, index)
    else:
        return None
        
@questions.route('/api/v1/questions/', methods=['POST', 'GET'])
def get_questions():
    """This function handles request to the questions resource"""
    if request.method == 'GET':
        # return all questions in the db
        response = jsonify(data['questions'])
        response.status_code = 200
    else: 
        # handles a POST request
        # return the new question with the question id
        question_id = int(data["questions"][-1]['id']) + 1
        req_data = json.loads(
            request.data.decode('utf-8').replace("'", '"'))
        question_text = req_data['text']
        asked_by = req_data['asked_by']
        date = '{:%B %d, %Y}'.format(datetime.now())
        new_question = {
            "id":question_id,
            "text":question_text,
            "asked_by":asked_by,
            "date":date,
            "answers":[]
        }
        data['questions'].append(new_question)
        response = jsonify(new_question)
        response.status_code = 201

    return response
    
@questions.route('/api/v1/questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def question(id, **kwargs):
    """This function, given a particular question id,
        retrieves the question or edits the question"""
    response = {}
    # locate the question
    q = locate(int(id), "questions")
    
    if q is None:
        # question not found
        # return error 404
        abort(404)

    if request.method == 'GET':
        # return the question
        response = jsonify(q[0])
        response.status_code = 200
    elif request.method == 'PUT':
        # obtain the required edit
        edited_question = json.loads(request.data.decode('utf-8').replace("'", '"'))['text']
        # edit the question in the data store
        q[0]['text'] = edited_question
        response = jsonify({
                    "id":id,
                    "text":edited_question
                    })
        response.status_code = 200
    else:
        # delete the question
        question_index = q[1]
        del data["questions"][question_index]
        response = jsonify({
            "question_id":id,
            "action":"deleted"})
        response.status_code = 200

    return response

@questions.route('/api/v1/questions/<int:id>/answers', methods=['POST'])
def answer(id, **kwargs):
    """ This function allows the user to post an answer 
    to a particular question, given the question id """
    questions = data['questions']
    question = {} 
    answer = json.loads(request.data.decode('utf-8').replace("'", '"'))
    # initialize up votes to 0
    answer['up_votes'] = "0"
    # locate the question
    question = locate(int(id), "questions")[0]
    if question:
        # question is located, append answer
        question['answers'].append(answer)
        # return a response with the question id and the answer
        response = jsonify({
            "question_id":str(question['id']),
            "text":answer['text'],                
        })
        response.status_code = 201
        return response         
    else:
        # the question with the given id was not found
        # return error 404
        abort(404)
