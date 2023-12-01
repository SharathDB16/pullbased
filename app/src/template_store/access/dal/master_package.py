from libutils.base.db.models import MasterPackageConfigTemplate, MasterPackage, EdgePackage, EdgeType, \
    ConfigTemplateVersion
from libutils.base.db.connection import SqlAlchemyConnection
from sqlalchemy.orm.exc import NoResultFound
from template_store.access.dal.template import FacadeTemplatePreview
from template_store.access.dal import log


class FacadeMasterPackage:
    @staticmethod
    def get_master_package_list():
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                list_ = []
                master_template_list = connection.query(MasterPackage).all()
                for master_template_value in master_template_list:
                    id_ = master_template_value.id
                    name = master_template_value.name
                    description = master_template_value.description
                    status = master_template_value.status
                    uninstall_file = master_template_value.uninstall_file.decode()
                    pre_script_file = master_template_value.pre_script_file.decode()
                    post_script_file = master_template_value.post_script_file.decode()
                    list_.append({"id": id_, "name": name, "description": description, "status": status,
                                  "uninstall_file": uninstall_file, "pre_script_file": pre_script_file,
                                  "post_script_file": post_script_file})
                return {"data": list_}
        except Exception as e:
            log.error(e)

    @staticmethod
    def add_master_package(name=None, description=None, path=None, user=None, group=None, permission=None,
                           uninstall_file=None, pre_script_file=None, post_script_file=None):
        try:
            master_package_record = MasterPackage(name=name, description=description, path=path, user=user,
                                                  group=group, permission=permission, uninstall_file=uninstall_file,
                                                  pre_script_file=pre_script_file, post_script_file=post_script_file)
            with SqlAlchemyConnection.session_scope() as connection:
                connection.add(master_package_record)
            return True
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def assign_package_to_edge(master_package_id=None, edge_type=None, edge_sub_type=None):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                edge_type_id = connection.query(EdgeType.id).filter(EdgeType.type == edge_type,
                                                                    EdgeType.sub_type == edge_sub_type).first()
                edge_package_id = connection.query(EdgePackage.id).filter(
                    EdgePackage.edge_type_id == edge_type_id[0],
                    EdgePackage.master_package_id == master_package_id).first()
                if edge_package_id is None:
                    connection.add(EdgePackage(edge_type_id=edge_type_id[0], master_package_id=master_package_id))
                    return True, False
                else:
                    return False, True
        except Exception as e:
            log.error(e)
            return False, False

    @staticmethod
    def delete_package_from_edge(master_package_id=None, edge_type=None, edge_sub_type=None):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                edge_type_id = connection.query(EdgeType.id).filter(EdgeType.type == edge_type,
                                                                    EdgeType.sub_type == edge_sub_type).first()
                edge_package_id = connection.query(EdgePackage.id).filter(
                    EdgePackage.edge_type_id == edge_type_id[0],
                    EdgePackage.master_package_id == master_package_id).first()
                if edge_package_id is None:
                    return False, True
                else:
                    connection.query(EdgePackage).filter(EdgePackage.id == edge_package_id[0]).delete()
                    return True, False
        except Exception as e:
            log.error(e)
            return False, False

    @staticmethod
    def update_master_package(args, master_id):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                output = connection.query(MasterPackage).filter(MasterPackage.id == master_id).update(args)
            return output
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def delete_master_package(master_id):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                connection.query(MasterPackage).filter(MasterPackage.id == master_id).update({"status": 0})
                config_template_id = connection.query(MasterPackageConfigTemplate.config_template_id).filter(
                    MasterPackageConfigTemplate.master_package_id == master_id).order_by(
                        MasterPackageConfigTemplate.id.desc()).first()
                template_file = connection.query(ConfigTemplateVersion.template_file).filter(
                    ConfigTemplateVersion.config_template_id == config_template_id[0]).order_by(
                    ConfigTemplateVersion.id.desc()).first()
                FacadeTemplatePreview.add_template_version(
                    config_template_id=config_template_id[0], comment="Uninstall", template_file=template_file[0])
            return True
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def assign_master_package_config(master_id, template_id):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                edge_package_id = connection.query(MasterPackageConfigTemplate.id).filter(
                    MasterPackageConfigTemplate.config_template_id == template_id,
                    MasterPackageConfigTemplate.master_package_id == master_id).first()
                if edge_package_id is None:
                    connection.add(MasterPackageConfigTemplate(config_template_id=template_id,
                                                               master_package_id=master_id))
                    return True, False
                else:
                    return False, True
        except Exception as e:
            log.error(e)
            return False, False

    @staticmethod
    def get_master_package_config(edge_type, edge_sub_type):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                list_ = []
                edge_type_id = connection.query(EdgeType.id).filter(EdgeType.type == edge_type,
                                                                    EdgeType.sub_type == edge_sub_type).first()
                if edge_type_id is None:
                    return {"message": "Invalid edge type, or edge sub type"}
                package_id_list = connection.query(EdgePackage.master_package_id).filter(
                    EdgePackage.edge_type_id == edge_type_id[0])
                for package_id in package_id_list:
                    master_template_list = connection.query(MasterPackage).filter(MasterPackage.id == package_id[0])
                    for master_template_value in master_template_list:
                        id_ = master_template_value.id
                        name = master_template_value.name
                        description = master_template_value.description
                        status = master_template_value.status
                        list_.append({"id": id_, "name": name, "description": description, "status": status})
                return {"data": list_}
        except Exception as exception:
            raise exception

    @staticmethod
    def get_master_package_to_edge_id(edge_type_id):
        try:
            with SqlAlchemyConnection.session_scope() as connection:
                package_id_list = connection.query(EdgePackage.master_package_id).filter(
                    EdgePackage.edge_type_id == edge_type_id)

                list_ = []
                if package_id_list:
                    for package_id in package_id_list:
                        master_template_list = connection.query(MasterPackage).filter(MasterPackage.id == package_id[0])
                        for master_template_value in master_template_list:
                            list_.append({"id": master_template_value.id, "name": master_template_value.name})
                    return {"meta": {'code': 200}, "data": list_}
                else:
                    return {"message": "No Master Package Found"}
        except Exception as exception:
            raise exception
