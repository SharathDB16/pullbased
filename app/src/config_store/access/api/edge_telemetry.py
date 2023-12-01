from config_store.access.bl.edge_telemetry import EdgePackageTelemetry
from flask_restful import Resource, reqparse, request
from libutils.utility import validate_edge_id, non_empty_string
from flask_api import status
import json


class EdgePackageDownloadTelemetry(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('edge_id', type=validate_edge_id, required=True,
                                   help='Invalid edge id',
                                   nullable=False)
        self.reqparse.add_argument('package_name', type=non_empty_string, required=True,
                                   help='Invalid package name',
                                   nullable=False)
        self.reqparse.add_argument('template_set_version', type=non_empty_string, required=True,
                                   help='Template set version not provided',
                                   nullable=False)

    def post(self, edge_id, download_status):
        args = self.reqparse.parse_args()
        remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
        request_data = json.loads(str(request.data, encoding='utf-8'))
        request_data.update({"ip_address": remote_ip})
        telemetry_info, description = EdgePackageTelemetry.set_package_download_telemetry(args, download_status,
                                                                                          request_data)

        if telemetry_info is True:
            return {"message": "success", "description": "{}".format(description)}, status.HTTP_200_OK
        else:
            return {"message": "Something went wrong",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class EdgePackageConsumptionTelemetry(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('edge_id', type=validate_edge_id, required=True,
                                   help='Invalid edge id',
                                   nullable=False)
        self.reqparse.add_argument('package_name', type=non_empty_string, required=True,
                                   help='Invalid package name',
                                   nullable=False)
        self.reqparse.add_argument('template_set_version', type=non_empty_string, required=True,
                                   help='Template set version not provided',
                                   nullable=False)

    def post(self, edge_id, consumption_status):
        args = self.reqparse.parse_args()
        remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
        request_data = json.loads(str(request.data, encoding='utf-8'))
        request_data.update({"ip_address": remote_ip})
        telemetry_info, description = EdgePackageTelemetry.set_package_consumption_telemetry(args, consumption_status,
                                                                                             request_data)
        if telemetry_info is True:
            return {"message": "success", "description": "{}".format(description)}, status.HTTP_200_OK
        else:
            return {"message": "Something went wrong",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class EdgeTelemetryReportList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self):
        return EdgePackageTelemetry.get_edge_telemetry_list()


class EdgeTelemetryReport(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self, edge_id):
        return EdgePackageTelemetry.get_edge_telemetry(edge_id)


class EdgeTelemetryReportInfoList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self, page_num):
        return EdgePackageTelemetry.get_edge_telemetry_info_list(page_num)


class EdgeTelemetryReportInfo(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self, edge_id):
        return EdgePackageTelemetry.get_edge_telemetry_info(edge_id)


class EdgeTelemetryReportFetchLatest(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self):
        return EdgePackageTelemetry.get_edge_telemetry_latest_info()


class EdgeTelemetryReportFetchEdgeType(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self):
        return EdgePackageTelemetry.get_edge_telemetry_edge_types()
