from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_in = request.get_json(silent=True)
    if not isinstance(picture_in, dict) or not isinstance(picture_in.get("id"), int):
        return {"message": "picture must include an integer id"}, 400
    for picture in data:
        if picture["id"] == picture_in["id"]:
            return {"Message": f"picture with id {picture_in['id']} already present"}, 302
    data.append(picture_in)
    return jsonify(picture_in), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_in = request.get_json(silent=True)
    if not isinstance(picture_in, dict):
        return {"message": "picture must be a JSON object"}, 400
    if picture_in.get("id", id) != id:
        return {"message": "picture id must match the URL"}, 400
    for index, picture in enumerate(data):
        if picture["id"] == id:
            picture_in["id"] = id
            data[index] = picture_in
            return jsonify(picture_in), 200
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            del data[index]
            return "", 204
    return {"message": "picture not found"}, 404
