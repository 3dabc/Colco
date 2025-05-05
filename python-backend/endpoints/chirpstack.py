from flask import Blueprint, jsonify, request
from chirpstack_config import get_chirpstack_client
from chirpstack_api.as_pb.external.api import ApplicationListRequest

chirpstack_bp = Blueprint('chirpstack', __name__)

@chirpstack_bp.route('/chirpstack/applications', methods=['GET'])
def list_applications():
    try:
        client = get_chirpstack_client()
        request = ApplicationListRequest(limit=10, offset=0)
        response = client.List(request)

        applications = [
            {"id": app.id, "name": app.name, "description": app.description}
            for app in response.result
        ]
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500