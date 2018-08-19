import json
#local imports
from flask import Flask, jsonify, request, make_response
from .data import data

def _locate(id, items):
    """This function takes 2 arguments (id : int and items : string)
        To locate the item = question or user, with the identifier = id, 
        from the collection of items."""
    collection = data[items]
    required_item = {}
    found = False
    index = 0
    for i in range(len(collection)):
        if int(collection[i]['id']) == int(id):
            required_item = collection[i]
            found = True
            index = i
            break
    if found:
        return (required_item, index)
    else:
        return (None, None)

def not_found(e):
    """This function returns a custom JSON response when a resource is not found"""
    error = {
        "path_accessed":str(request.path),
        "message":"The path accessed / resource requested cannot be found, please check"
    }
    response = make_response(jsonify(error), 404)
    return response

def bad_request(e):
    """This function creates a custom JSON response when a bad request is made"""
    error = {
        "path_accessed":str(request.path),
        "message":"The request made had errors, please check the headers or params",
        "request_data":json.loads(request.data.decode().replace("'",'"'))
    }
    response = make_response(jsonify(error), 400)
    return response

def create_app():   
    app = Flask(__name__)
    from .questions import questions as questions_blueprint
    app.register_blueprint(questions_blueprint)
    from .users import users as users_blueprints
    app.register_blueprint(users_blueprints)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found)
    
    return app
    
app = create_app()
    