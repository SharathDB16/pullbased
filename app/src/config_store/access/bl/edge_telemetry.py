from config_store.access.dal.edge_telemetry import FacadeEdgeTelemetry
from config_store.access.api import log


class EdgePackageTelemetry:

    @staticmethod
    def set_package_download_telemetry(args, download_status, request_data):

        if download_status == 'success':
            code_id = 1
            description = "Package Download Successful"
        else:
            code_id = 2
            description = "Package Download Failed"

        log.critical("Edge id {} | {} | package name : {}, template_set version: {}".format(
            args["edge_id"], description, args["package_name"], args["template_set_version"]))
        telemetry_info = FacadeEdgeTelemetry.add_telemetry_info(
            code_id, args["edge_id"], args["package_name"], args["template_set_version"], request_data)
        return telemetry_info, description

    @staticmethod
    def set_package_consumption_telemetry(args, consumption_status, request_data):

        if consumption_status == 'success':
            code_id = 3
            description = "Package Consumption Successful"
        else:
            code_id = 4
            description = "Package Consumption Failed"

        log.critical("Edge id {} | {} | package name : {}, template_set version: {}".format(
            args["edge_id"], description, args["package_name"], args["template_set_version"]))
        telemetry_info = FacadeEdgeTelemetry.add_telemetry_info(
            code_id, args["edge_id"], args["package_name"], args["template_set_version"], request_data)
        return telemetry_info, description

    @staticmethod
    def get_edge_telemetry_list():
        return FacadeEdgeTelemetry.get_edge_telemetry_list()

    @staticmethod
    def get_edge_telemetry(edge_id):
        return FacadeEdgeTelemetry.get_edge_telemetry(edge_id)

    @staticmethod
    def get_edge_telemetry_info_list(page_num):
        return FacadeEdgeTelemetry.get_edge_telemetry_info_list(page_num)

    @staticmethod
    def get_edge_telemetry_info(edge_id):
        return FacadeEdgeTelemetry.get_edge_telemetry_info(edge_id)

    @staticmethod
    def get_edge_telemetry_latest_info():
        return FacadeEdgeTelemetry.get_edge_telemetry_latest_info()

    @staticmethod
    def get_edge_telemetry_edge_types():
        return FacadeEdgeTelemetry.get_edge_telemetry_edge_types()

