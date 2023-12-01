import werkzeug
from flask_api import status
from flask import jsonify, Response
from flask_restful import Resource, reqparse
from libutils.utility import non_empty_string
from template_store.access.bl.template import TemplatePreview, ConfigTemplate, SugarboxConf, FuplimitConf, WGConf
from libutils.generator_helper.template_context import Base
from libutils.generator_helper.dpverse import DPController
from libutils.generator_helper.wireguardip import WireGuardIP
from libutils.base.config.configuration import config_obj


class ConfigTemplatePreviewResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('file', type=werkzeug.FileStorage, required=True,
                                   help='Template file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('edge_id', type=non_empty_string, required=True,
                                   help='Edge id must be provided with string value',
                                   location='values')

    def post(self, edge_id):
        args = self.reqparse.parse_args()
        return TemplatePreview.list_variables(args)


class ConfigTemplateResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=non_empty_string, required=True,
                                   nullable=False, help='Name must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('description', type=non_empty_string, required=True,
                                   nullable=False, help='Description must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('owner', type=non_empty_string, required=True,
                                   nullable=False, help='Owner must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('group', type=non_empty_string, required=True,
                                   nullable=False, help='Group must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('permission', type=non_empty_string, required=True,
                                   nullable=False, help='Permission must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('path', type=non_empty_string, required=True,
                                   nullable=False, help='Path must be provided with string value',
                                   location='json')

    def post(self):
        args = self.reqparse.parse_args()
        path_status, template_val, data = ConfigTemplate.add_config_template(args)
        if path_status is True:
            return jsonify({"message": "Incorrect path"})
        elif template_val is True:
            message = {"message": "Template added"}
            message.update(data)
            return jsonify(message)
        else:
            return {"message": "Template not added",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST

    def get(self):
        return ConfigTemplate.get_config_template_list()


class ConfigTemplateVersionResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('template_file', type=werkzeug.FileStorage, required=True,
                                   help='Template file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('comment', type=non_empty_string, required=True,
                                   help='Comment must be provided with string value',
                                   nullable=False, location='values')

    def post(self, template_id):
        args = self.reqparse.parse_args()
        template_version_val = ConfigTemplate.add_template_version(args, template_id)
        if template_version_val is True:
            return jsonify({"message": "Template version added"})
        else:
            return {"message": "Template version not added",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class ConfigTemplateDownloadResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('version', type=float, required=False,
                                   nullable=False)

    def get(self, template_id):
        args = self.reqparse.parse_args()
        template_file, template_name, template_path = ConfigTemplate.download_config_template_file(args["version"],
                                                                                                   template_id)
        if template_file is False and template_name is None:
            return {"message": "Could not get template file",
                    "description": "Something went wrong"}  , status.HTTP_500_INTERNAL_SERVER_ERROR
        elif template_file is False and template_name == "":
            return {"message": "Template file not found"}, status.HTTP_404_NOT_FOUND
        else:
            return jsonify({"template_name": template_name, "template_path": template_path,
                            "template_file": template_file})


class GetConfigTemplateResource(Resource):

    def get(self, master_id):
        master_data = ConfigTemplate.get_config_template_from_package(master_id)
        if master_data is None:
            return {"message": f"Could not find master id {master_id}"}, status.HTTP_404_NOT_FOUND
        return master_data


class ConfigTemplateListResource(Resource):

    def get(self, master_id):
        return ConfigTemplate.get_config_template_name_from_package(master_id)


class ConfigTemplateFileResource(Resource):

    def put(self):
        update_config_val = ConfigTemplate.update_config_template_version()
        if update_config_val is True:
            return jsonify({"message": "Template version updated"})
        else:
            return {"message": "Template version not updated",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class GetSugarboxConfResource(Resource):

    def get(self, edge_id):
        Base.__init__(self, edge_id)
        conf_file = SugarboxConf.update_sugarbox_conf(self, edge_id)
        if not conf_file:
            return {"message": "Something went wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return conf_file


class GetFuplimitConfResource(Resource):

    def get(self, edge_id):
        context = dict()
        dp_verse_obj = DPController(edge_id)
        dp_verse_details = dp_verse_obj.get_dp_verse_details()
        if dp_verse_details:
            context.update(dp_verse_details)
        conf_file = FuplimitConf.update_fuplimit_conf(context, edge_id)
        if not conf_file:
            return {"message": "Something went wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return conf_file


class GetWGConfResource(Resource):

    def get(self, edge_id):
        context = dict()
        wg_ip_obj = WireGuardIP(edge_id)
        context.update(wg_ip_obj.get_wireguard_details())
        print(context)
        if config_obj.environment_type == "staging":
            context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})
        conf_file = WGConf.update_wg_conf(context, edge_id)
        if not conf_file:
            return {"message": "Something went wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return conf_file

