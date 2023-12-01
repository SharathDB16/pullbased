from flask_restful import Resource
from flask_api import status
from flask import jsonify
from config_store.access.bl.set_version import SetVersion


class SetVersionResource(Resource):
    def __init__(self):
        pass

    def get(self):
        data = SetVersion.get_all_latest_set_version(self)
        print(data)
        if data:
            return data, status.HTTP_200_OK
        else:
            return data, status.HTTP_204_NO_CONTENT
