from flask_restful import Resource, reqparse
from flask_api import status
from libutils.utility import validate_edge_id
from config_store.access.bl.template_set import TemplateSet


class TemplateSetResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('edge_id', type=validate_edge_id, required=True,
                                   help='Invalid edge id',
                                   nullable=False)
        self.reqparse.add_argument('set_version', type=float, required=False,
                                   help='Invalid set version',
                                   nullable=False)
        super(TemplateSetResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        result, set_version = TemplateSet.get_all_templates(args["edge_id"], args["set_version"])
        return {"data": result, "latest_set_version": set_version}, status.HTTP_200_OK
