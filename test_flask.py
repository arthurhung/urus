try:
    from http import HTTPStatus
except ImportError:
    import httplib as HTTPStatus
from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import request
from flasgger import Schema
from flasgger import Swagger
from flasgger import SwaggerView
from flasgger import fields
from flasgger import swag_from
from flasgger import validate
from flask_restful import Resource, Api

# Examples include intentionally invalid defaults to demonstrate validation.
# _TEST_META_SKIP_FULL_VALIDATION = True

app = Flask(__name__)
# swag = Swagger(app)

# from flask_restful import reqparse, abort, Api, Resource

# app = Flask(__name__)
# api = Api(app)


@app.route("/manualvalidation", methods=['POST'])
# @swag_from("test_validation.yml")
def manualvalidation():
    """
    In this example you need to call validate() manually
    passing received data, Definition (schema: id), specs filename
    """
    data = request.json
    validate(data, 'User', "test_validation.yml")
    return jsonify(data)


# @app.route("/manualvalidation", methods=['POST'])
# class IDcardValidator(Resource):

#     @swag_from("test_validation.yml")
#     def post(self):
#         """
#         In this example you need to call validate() manually
#         passing received data, Definition (schema: id), specs filename
#         """
#         data = request.json
#         validate(data, 'User', "test_validation.yml")
#         return jsonify(data)

# api.add_resource(IDcardValidator, '/todos')

if __name__ == "__main__":
    app.run(debug=True)