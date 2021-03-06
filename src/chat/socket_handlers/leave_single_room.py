import json
import logging

from boto3 import client as boto3_client
import requests
import redis

from common import delete_connection_from_rooms, broadcast_user_left


def handle(connection, data):
    """
    Remove connection from room
    Remove room from connection
    """
    room_id = data['roomId']
    user = connection.user

    delete_connection_from_rooms(connection, [room_id])
    connection.leave_room(room_id)

    return {
        "name": "left_room",
        "roomId": room_id,
        "user": user
    }
