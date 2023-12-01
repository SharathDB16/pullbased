import re
import tempfile
import requests
from flask import Response
from jinja2 import Environment, Template, meta, BaseLoader
from template_store.access.dal.template import FacadeTemplatePreview, FacadeDownloadTemplateFile
from libutils.base.config.configuration import config_obj
from libutils.utility import edge_type_subtype, get_context
from libutils.generator_helper.ipam import Controller
from template_store.access.bl import log


class TemplatePreview:

    @staticmethod
    def list_variables(args):
        env = Environment()
        template_preview = args.file.read().decode('utf-8')
        ast = env.parse(template_preview)
        final_list = meta.find_undeclared_variables(ast)
        i_pam_obj = Controller(args.edge_id)
        edge_type, edge_sub_type = i_pam_obj.get_edge_type_subtype()
        context_class = get_context(edge_type, edge_sub_type)
        context_obj = context_class(args.edge_id, edge_type, edge_sub_type)
        context = context_obj.get_context()
        context.update({"edge_id": args.edge_id})

        for a in final_list:
            if a not in context:
                log.error(a)

        if context:
            template_preview = Template(template_preview).render(context)
        return Response(template_preview, mimetype="text/plain")


class ConfigTemplate:

    @staticmethod
    def get_config_template_list():
        return FacadeTemplatePreview.get_config_template_list()

    @staticmethod
    def add_config_template(args):
        path_exists = re.search("^(.+)/([^/]+)$", args["path"])
        if path_exists:
            return FacadeTemplatePreview.add_config_template(name=args["name"], description=args["description"],
                                                             owner=args["owner"], group=args["group"],
                                                             permission=args["permission"], path=args["path"])
        else:
            return True, False

    @staticmethod
    def add_template_version(args, template_id):
        return FacadeTemplatePreview.add_template_version(
            config_template_id=template_id, comment=args.comment,
            template_file=str.encode(args.template_file.read().decode('utf-8')))

    @staticmethod
    def download_config_template_file(version, template_id):
        return FacadeDownloadTemplateFile.download_config_template_file(version=version, template_id=template_id)

    @staticmethod
    def get_config_template_from_package(master_id):
        return FacadeTemplatePreview.get_config_template_from_package(master_id)

    @staticmethod
    def get_config_template_name_from_package(master_id):
        return FacadeTemplatePreview.get_config_template_name_from_package(master_id)

    @staticmethod
    def update_config_template_version():
        try:
            templates_to_update = []
            for template_id in templates_to_update:
                response = requests.get(f"{config_obj.config_template_url}{template_id}/")
                json_response = response.json()
                if json_response.get('template_file'):
                    temp = tempfile.TemporaryFile()
                    temp.write(json_response.get('template_file').encode())
                    temp.seek(0)
                    comment = {"comment": "update"}
                    template_file = {'template_file': temp.read()}
                    version_api = f"{config_obj.version_update_url}{template_id}/"
                    requests.post(version_api, files=template_file, data=comment)
                    temp.close()
            return True
        except Exception as e:
            log.error(e)
            return False


class SugarboxConf:

    @staticmethod
    def update_sugarbox_conf(self, edge_id):
        try:
            template_id = config_obj.sbox_template_id
            response = requests.get(f"{config_obj.config_template_url}{template_id}/")
            json_response = response.json()
            edge_type, edge_sub_type, switch_type, template_id, tag_list = edge_type_subtype(edge_id) or (None, None, None, None, None)
            self.context.update({"edge_id": edge_id})
            self.context.update({"edge_type": edge_type})
            self.context.update({"edge_sub_type": edge_sub_type})
            conf_file = Environment(loader=BaseLoader()).from_string(json_response.get('template_file'))
            return conf_file.render(self.context)
        except Exception as e:
            log.error(e)
            return False


class FuplimitConf:

    @staticmethod
    def update_fuplimit_conf(context, edge_id):
        try:
            template_id = config_obj.fup_template_id
            response = requests.get(f"{config_obj.config_template_url}{template_id}/")
            json_response = response.json()
            conf_file = Environment(loader=BaseLoader()).from_string(json_response.get('template_file'))
            return conf_file.render(context)
        except Exception as e:
            log.error(e)
            return False

class WGConf:

    @staticmethod
    def update_wg_conf(context, edge_id):
        try:
            template_id = config_obj.wg_template_id
            response = requests.get(f"{config_obj.config_template_url}{template_id}/")
            json_response = response.json()
            conf_file = Environment(loader=BaseLoader()).from_string(json_response.get('template_file'))
            return conf_file.render(context)
        except Exception as e:
            log.error(e)
            return False
