import json

from flask import Blueprint, request, jsonify

from models import db
from models.room import Room

from sp_token import get_user_from_token

permission_api = Blueprint("Permission", __name__)


def has_permission_response():
    return jsonify({"success": True}), 200


@permission_api.route("/api/v1/has_permission", methods=["POST"])
@get_user_from_token(True)
def has_permission(user=None):
    """
    Insert new message and also get latest messages since offset,
    not just the message inserted
    """
    if user['isMod']:
        return has_permission_response()

    payload = request.get_json()
    action = payload["action"]

    if action == 'join_room':
        room_id = payload["room_id"]
        room = Room.query.filter(Room.id == room_id).first()
        if room and room.rules:
            rules = json.loads(room.rules)
            blacklist = rules.get('blacklist', [])
            if user['id'] in blacklist:
                return jsonify({"error": 'You are in blacklist of this room'}),  403

        return has_permission_response()

    if action == 'kick_user':
        return has_permission_response()

    if action == 'delete_message':
        room_id = payload["room_id"]
        room = Room.query.filter(Room.id == room_id).first()
        if room:
            if room.owner == user['id']:
                return has_permission_response()
            else:
                return jsonify({"error": 'No permission to delete message'}),  403
        else:
            return jsonify({"error": "room not found"}), 404

    return 'action not defined', 400
