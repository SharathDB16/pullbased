from flask_restful import Resource, reqparse
from flask_api import status
from collections import OrderedDict
from libutils.utility import validate_edge_id, non_empty_string
from config_store.access.bl.config_generator import ConfigGenerator


class ConfigPackageResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mac_address', type=non_empty_string, required=False,
                                   help='Invalid mac_address',
                                   nullable=False)
        self.reqparse.add_argument('edge_id', type=validate_edge_id, required=False,
                                   help='Invalid edge id',
                                   nullable=False)
        self.reqparse.add_argument('set_version', type=float, required=False,
                                   help='Invalid set version',
                                   nullable=False)
        super(ConfigPackageResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        edge_id, latest_set_version, path, template_id = ConfigGenerator.generate_package(
                                                            args["edge_id"], args["mac_address"], args["set_version"])
        payload = OrderedDict()
        if edge_id is None and latest_set_version is None and path is None:
            payload["data"] = "Edge Id not found for given mac_address in DP"
            return payload, status.HTTP_404_NOT_FOUND
        elif path is None:
            payload["data"] = "No changes in configuration"
        else:
            payload["data"] = "Package generated"
            payload["path"] = path
            payload["template_id"] = template_id

        payload["edge_id"] = edge_id
        payload["latest_set_version"] = latest_set_version
        return payload, status.HTTP_200_OK
