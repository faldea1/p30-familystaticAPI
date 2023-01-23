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

    if members:
        return jsonify(members), 200
    else:
        return jsonify({"message": "no members available"}), 404


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)

    if member:
        response_member = {
            "id": member.get("id", ''),
            "first_name": member.get("first_name", ''),
            "age": member.get("age", ''),
            "lucky_numbers": member.get("lucky_numbers", [])           
        }
        return jsonify(response_member), 200
    else:
        return jsonify({"message": "ID was not found"}), 400


@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()

    if data:
        return jsonify(jackson_family.add_member(data)), 200
    else:
        return jsonify({"message": "member not found"}), 404


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member_deleted = jackson_family.delete_member(member_id)

    if member_deleted: 
        return jsonify({"done": True, "member_deleted": member_deleted}), 200
    else:
        return jsonify({"message": "ID was not found"}), 404


@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    updated_member = jackson_family.update_member(member_id, data)

    if member:
        return jsonify(updated_member), 200
    else:
        return jsonify({"message":"ID was not found for update"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
