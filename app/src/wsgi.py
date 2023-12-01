from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config_store.access.api.config_package import ConfigPackageResource
from config_store.access.api.template_set import TemplateSetResource
from config_store.access.api.set_version import SetVersionResource
from template_store.access.api.master_package import MasterPackageListResource, AssignMasterPackageResource, \
    MasterPackageResource, AssignMasterPackageConfigResource, GetMasterPackageResource, GetMasterPackageListResource
from template_store.access.api.config_template import ConfigTemplateResource, ConfigTemplatePreviewResource, \
    ConfigTemplateVersionResource, ConfigTemplateDownloadResource, GetConfigTemplateResource, \
    ConfigTemplateListResource, ConfigTemplateFileResource, GetSugarboxConfResource, GetFuplimitConfResource, \
    GetWGConfResource
from config_store.access.api.edge_telemetry import EdgePackageDownloadTelemetry, EdgePackageConsumptionTelemetry, \
    EdgeTelemetryReportList, EdgeTelemetryReport, EdgeTelemetryReportInfoList, EdgeTelemetryReportInfo, \
    EdgeTelemetryReportFetchLatest, EdgeTelemetryReportFetchEdgeType
#from elasticapm.contrib.flask import ElasticAPM
from libutils.base.config.configuration import config_obj
from libutils.utility import HealthCheck

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

app.config['ELASTIC_APM'] = {
          'SERVICE_NAME': config_obj.service_name, 'ENVIRONMENT': config_obj.environment_type,
          'SERVER_URL': config_obj.server_url
}
#apm = ElasticAPM(app)


def __config_template_resource_api():
    api.add_resource(ConfigTemplateResource, '/api/v1.0/config_template/')
    api.add_resource(GetConfigTemplateResource, '/api/v1.0/config_template/<int:master_id>/')
    api.add_resource(ConfigTemplatePreviewResource, '/api/v1.0/config_template/preview/<string:edge_id>/')
    api.add_resource(ConfigTemplateVersionResource, '/api/v1.0/config_template/version/<int:template_id>/')
    api.add_resource(ConfigTemplateDownloadResource, '/api/v1.0/config_template/download/<int:template_id>/')
    api.add_resource(ConfigTemplateListResource, '/api/v1.0/config_template/name/<int:master_id>/')
    api.add_resource(ConfigTemplateFileResource, '/api/v1.0/update_config_template/')
    api.add_resource(GetSugarboxConfResource, '/api/v1.0/get_sugarbox_config/<string:edge_id>/')
    api.add_resource(GetFuplimitConfResource, '/api/v1.0/get_fuplimit_config/<string:edge_id>/')
    api.add_resource(GetWGConfResource, '/api/v1.0/get_wg_config/<string:edge_id>/')


def __master_package_resource_api():
    api.add_resource(MasterPackageListResource, '/api/v1.0/master_package/')
    api.add_resource(MasterPackageResource, '/api/v1.0/master_package/<int:master_id>/')
    api.add_resource(AssignMasterPackageResource, '/api/v1.0/master_package/assign/<int:master_id>/')
    api.add_resource(GetMasterPackageResource, '/api/v1.0/master_package/<string:edge_type>/<string:edge_sub_type>/')
    api.add_resource(AssignMasterPackageConfigResource, '/api/v1.0/master_package_config/<int:master_id>/assign/'
                                                        '<int:template_id>/')
    api.add_resource(GetMasterPackageListResource, '/api/v1.0/master_package_list/<int:edge_type_id>/')


def __template_set_resource_api():
    api.add_resource(TemplateSetResource, '/api/v1.0/template_set/latest/')
    api.add_resource(SetVersionResource, '/api/v1.0/set_version/latest/')


def __config_package_resource_api():
    api.add_resource(ConfigPackageResource, '/api/v1.0/config_package/')


def __edge_telemetry_resource_api():
    api.add_resource(EdgePackageDownloadTelemetry, '/api/v1.0/edge_telemetry/package_download/<string:edge_id>/'
                                                   '<string:download_status>/')
    api.add_resource(EdgePackageConsumptionTelemetry, '/api/v1.0/edge_telemetry/package_consumption/<string:edge_id>/'
                                                      '<string:consumption_status>/')
    api.add_resource(EdgeTelemetryReportList, '/api/v1.0/edge_telemetry/report_list/')
    api.add_resource(EdgeTelemetryReport, '/api/v1.0/edge_telemetry/report/<string:edge_id>/')
    api.add_resource(EdgeTelemetryReportInfoList, '/api/v1.0/edge_telemetry_info_list/report/<int:page_num>/')
    api.add_resource(EdgeTelemetryReportInfo, '/api/v1.0/edge_telemetry_info/report/<string:edge_id>/')
    api.add_resource(EdgeTelemetryReportFetchLatest, '/api/v1.0/edge_telemetry_info/fetch_latest/')
    api.add_resource(EdgeTelemetryReportFetchEdgeType, '/api/v1.0/edge_telemetry_info/fetch_edge_type/')


def __health_check_api():
    api.add_resource(HealthCheck, '/v1/health')


def __init_all_api():
    __config_template_resource_api()
    __master_package_resource_api()
    __template_set_resource_api()
    __config_package_resource_api()
    __edge_telemetry_resource_api()
    __health_check_api()


if __name__ == "__main__":
    __init_all_api()
    app.run(debug=False)
