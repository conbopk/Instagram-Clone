from flask import jsonify
from datetime import datetime, timezone


def api_response(data=None, message=None, status=200):
    response = {
        'success': 200 <= status < 300,
        'status': status
    }

    if message:
        response['message'] = message

    if data is not None:
        response['data'] = data

    return jsonify(response), status

def utc_now():
    return datetime.now(timezone.utc)
