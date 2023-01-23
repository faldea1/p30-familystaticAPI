"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id=None)
    member = jackson_family.get_member(member_id)

    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "ID was not found"}), 400


@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()

    if isinstance(data, dict):
        jackson_family.add_member(data)
        return jsonify({"message": "new member incorporated"}), 200
    else:
        return jsonify({"meesage": "the request has an error"}), 400


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id=None):
    member = jackson_family.delete_member(member_id)

    if member: 
        return jsonify(member), 200
    else:
        return jsonify({"message": "ID was not found"}), 400


@app.route('/member/<int:member_id>', methods=['PUT'])
def refresh_member(member_id=None):
    data = request.get_json()
    member = jackson_family.update_member(member_id, data)

    if member:
        return jsonify({"message":"member has been updated"}), 200
    else:
        return jsonify({"message":"ID was not found"}), 400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
