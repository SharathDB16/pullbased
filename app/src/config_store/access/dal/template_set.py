from libutils.base.db.connection import SqlAlchemyConnection
from libutils.base.db.models import EdgePackage, MasterPackage, TemplateSetVersion
from libutils.base.db.models import ConfigTemplate, ConfigTemplateVersion, MasterPackageConfigTemplate
from libutils.base.db.models import SwitchPackage
from sqlalchemy import func
import collections


class FacadeTemplateSet:

    @staticmethod
    def get_master_package_id(edge_type_id):
        """Gets all the master package ids for a particular type of edge"""
        with SqlAlchemyConnection.session_scope() as connection:
            result_obj = connection.query(EdgePackage.master_package_id).distinct()\
                .filter(EdgePackage.edge_type_id == edge_type_id).all()
            master_package_ids = [value for value, in result_obj]

            result_obj = connection.query(MasterPackage.id).filter(MasterPackage.id.in_(master_package_ids)).order_by(
                MasterPackage.execution_sequence).all()
            master_package_ids = [value for value, in result_obj]

            return master_package_ids

    @staticmethod
    def get_switch_package_id(edge_type_id, switch_type_id):
        with SqlAlchemyConnection.session_scope() as connection:
            result_obj = connection.query(SwitchPackage.master_package_id).distinct() \
                .filter(SwitchPackage.edge_type_id == edge_type_id,
                        SwitchPackage.switch_type_id == switch_type_id).all()
            switch_package_id = [value for value, in result_obj]
            return switch_package_id

    @staticmethod
    def get_template_set(current_set_version=None, tag_list=None):
        avail_tags = ['ALL']
        for tag in tag_list:
            if tag['value'].startswith("CONFIG"):
                avail_tags.append(tag['value'])
                break

        set_version = TemplateSetVersion.set_version_no
        template_version = TemplateSetVersion.template_version_no
        template_id = TemplateSetVersion.config_template_id

        with SqlAlchemyConnection.session_scope() as connection:
            if current_set_version is None:
                min_set_version = connection.query(func.min(set_version)).one()[0]
            else:
                min_set_version = current_set_version

            max_set_version = connection.query(func.max(set_version)).one()[0]

            result_obj = connection.query(template_id, template_version)\
                .filter(set_version > min_set_version, TemplateSetVersion.tag_name.in_(avail_tags)).all()

            master_package_ids = [(template_id, template_version) for
                                  template_id, template_version in result_obj]
            template_set = collections.defaultdict(dict)
            config_set = collections.defaultdict(list)
            for template_id, version in master_package_ids:
                config_set[template_id].append(version)
                config_set[template_id] = [max(config_set[template_id])]
                master_id_list = connection.query(MasterPackageConfigTemplate.master_package_id).filter(MasterPackageConfigTemplate.config_template_id==template_id).all()
                master_ids = [id for id, in master_id_list]
                for master_id in master_ids:
                    if template_id in config_set:
                        template_set[master_id][template_id] = config_set[template_id]
            return template_set, str(max_set_version)

    @staticmethod
    def get_template_details(template_id):
        with SqlAlchemyConnection.session_scope() as connection:
            template_data = connection.query(ConfigTemplate).filter(ConfigTemplate.id==template_id).first()
            return {
                "name": template_data.name,
                "description": template_data.description,
                "path": template_data.path,
                "owner": template_data.owner,
                "group": template_data.group,
                "permissions": template_data.permissions,
                "template_id": template_id
            }

    @staticmethod
    def get_template_version_details(template_id, template_version):
        with SqlAlchemyConnection.session_scope() as connection:
            version_data = connection.query(ConfigTemplateVersion).filter(ConfigTemplateVersion.config_template_id==template_id,
                                                                          ConfigTemplateVersion.version_no==template_version).first()
            return {
                "template_file": version_data.template_file.decode(),
                "comment": version_data.comment,
                "version_no": str(version_data.version_no)
            }

    @staticmethod
    def get_master_details(master_id):
        with SqlAlchemyConnection.session_scope() as connection:
            master_details = connection.query(MasterPackage).filter(MasterPackage.id==master_id).first()
            return {
                "name": master_details.name,
                "description": master_details.description,
                "status": master_details.status,
                "execution_sequence": master_details.execution_sequence
            }

    @staticmethod
    def get_master_files(master_id):
        with SqlAlchemyConnection.session_scope() as connection:
            master_file = connection.query(MasterPackage).filter(MasterPackage.id == master_id).first()
            return {
                "uninstall_file": master_file.uninstall_file.decode(),
                "pre_script_file": master_file.pre_script_file.decode(),
                "post_script_file": master_file.post_script_file.decode()
            }

