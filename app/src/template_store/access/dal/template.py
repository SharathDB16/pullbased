from libutils.utility import version_incrementer
from libutils.base.db.connection import SqlAlchemyConnection
from libutils.base.db.models import EdgeType, ConfigTemplate, ConfigTemplateVersion, TemplateSetVersion, \
    ConfigVariable, EdgeConfigVariable, MasterPackageConfigTemplate, MasterPackage
from template_store.access.dal import log


class FacadeTemplatePreview:
    @staticmethod
    def check_variable(edge_type, edge_sub_type, final_list):
        with SqlAlchemyConnection.session_scope() as connection:
            avail_in_db, not_avail_in_db = [], []
            edge_type_id = connection.query(EdgeType.id).filter(EdgeType.type == edge_type,
                                                                EdgeType.sub_type == edge_sub_type).first()
            not_assigned = False
            for list_val in final_list:
                config_variable_id = connection.query(ConfigVariable.id).filter(ConfigVariable.name == list_val).first()
                if config_variable_id:
                    edge_config_id = connection.query(EdgeConfigVariable.id).filter(
                        EdgeConfigVariable.edge_type_id == edge_type_id[0],
                        EdgeConfigVariable.config_variable_id == config_variable_id[0]).first()
                    if edge_config_id:
                        dict_ = {"id": config_variable_id[0], "variable_name": list_val, "assigned_status": True}
                    else:
                        not_assigned = True
                        dict_ = {"id": config_variable_id[0], "variable_name": list_val, "assigned_status": False}
                    avail_in_db.append(dict_)
                else:
                    not_avail_in_db.append(list_val)
            return avail_in_db, not_avail_in_db, not_assigned

    @staticmethod
    def get_config_template_list():
        with SqlAlchemyConnection.session_scope() as connection:
            list_ = []
            config_template_list = connection.query(ConfigTemplate).all()
            for config_template_value in config_template_list:
                id_ = config_template_value.id
                name = config_template_value.name
                description = config_template_value.description
                master_package_id_list = connection.query(MasterPackageConfigTemplate.master_package_id).\
                    filter(id_ == MasterPackageConfigTemplate.config_template_id)
                master_package_list_ = []
                for master_id in master_package_id_list:
                    master_package = connection.query(MasterPackage.name).filter(master_id == MasterPackage.id).first()
                    for master_package_name in master_package:
                        master_package_list_.append(master_package_name)
                list_.append({"id": id_, "name": name, "description": description,
                              "master_package_list": master_package_list_})
            return {"data": list_}

    @staticmethod
    def get_config_template_from_package(master_id):
        with SqlAlchemyConnection.session_scope() as connection:
            list_ = []
            master_id_exists = connection.query(MasterPackage).filter(MasterPackage.id == master_id).count()
            if master_id_exists == 0:
                return None
            config_template_id_list = connection.query(MasterPackageConfigTemplate.config_template_id).filter(
                MasterPackageConfigTemplate.master_package_id == master_id)

            for config_template_id in config_template_id_list:
                config_template_list = connection.query(ConfigTemplate).filter(
                    ConfigTemplate.id == config_template_id[0])
                for config_template_value in config_template_list:
                    id_ = config_template_value.id
                    name = config_template_value.name
                    description = config_template_value.description
                    version_no = connection.query(ConfigTemplateVersion.version_no).filter(
                        ConfigTemplateVersion.config_template_id == id_).order_by(ConfigTemplateVersion.id.desc()).first()
                    list_.append({"id": id_, "name": name, "description": description, "version_no": float(version_no[0])})
            return {"data": list_}

    @staticmethod
    def add_config_template(name=None, description=None, owner=None, group=None, permission=None, path=None):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                conf_tep_obj = ConfigTemplate(name=name, description=description, owner=owner, group=group,
                                              permissions=permission, path=path)
                connection.add(conf_tep_obj)
                connection.commit()
                connection.refresh(conf_tep_obj)
                data = {"template_id": conf_tep_obj.id}

            return False, True, data
        except Exception as e:
            log.error(e)
            return False, False

    @staticmethod
    def add_template_version(config_template_id=None, comment=None, template_file=None):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                template_version_no = connection.query(ConfigTemplateVersion.version_no).filter(
                    ConfigTemplateVersion.config_template_id == config_template_id).order_by(
                    ConfigTemplateVersion.id.desc()).first()
                if template_version_no:
                    template_version_no = version_incrementer(template_version_no[0])
                else:
                    template_version_no = version_incrementer(template_version_no)

                failed = False
                try:
                    connection.add(
                        ConfigTemplateVersion(config_template_id=config_template_id, comment=comment,
                                              version_no=template_version_no, template_file=template_file))
                except Exception as e:
                    log.error(e)
                    failed = True

                if not failed:
                    template_set_version_no = connection.query(TemplateSetVersion.set_version_no).order_by(
                        TemplateSetVersion.id.desc()).first()
                    if template_set_version_no:
                        template_set_version_no = version_incrementer(template_set_version_no[0])
                    else:
                        template_set_version_no = version_incrementer(template_set_version_no)
                    connection.add(TemplateSetVersion(set_version_no=template_set_version_no,
                                                      config_template_id=config_template_id,
                                                      template_version_no=template_version_no))
            return True
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def get_config_template_name_from_package(master_id):
        with SqlAlchemyConnection.session_scope() as connection:
            list_ = []
            config_template_id_list = connection.query(MasterPackageConfigTemplate.config_template_id).filter(
                MasterPackageConfigTemplate.master_package_id == master_id)

            for config_template_id in config_template_id_list:
                config_template_list = connection.query(ConfigTemplate).filter(
                    ConfigTemplate.id == config_template_id[0])
                for config_template_value in config_template_list:
                    list_.append({"id": config_template_value.id, "name": config_template_value.name})
            return {"meta": {'code': 200}, "data": list_}


class FacadeDownloadTemplateFile:
    @staticmethod
    def download_config_template_file(version=None, template_id=None):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                if version is None:
                    template_obj = connection.query(ConfigTemplateVersion).filter(
                        ConfigTemplateVersion.config_template_id == template_id).order_by(
                        ConfigTemplateVersion.id.desc()).first()
                else:
                    template_obj = connection.query(ConfigTemplateVersion).filter(
                        ConfigTemplateVersion.config_template_id == template_id,
                        ConfigTemplateVersion.version_no == version).first()
                if template_obj is None:
                    return False, ""
                template_file = template_obj.template_file.decode()
                template_data = connection.query(ConfigTemplate.name, ConfigTemplate.path).filter(ConfigTemplate.id ==
                                                                                                  template_id).first()
                template_name = template_data[0] + "_v" + str(template_obj.version_no)
                template_path = template_data[1]
            return template_file, template_name, template_path
        except Exception as e:
            log.error(e)
            return False, None
