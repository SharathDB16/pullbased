from libutils.base.db.connection import SqlAlchemyConnection
from libutils.base.db.models import EdgePackage, MasterPackageConfigTemplate, EdgeType, TemplateSetVersion
from sqlalchemy import func
from flask import jsonify
from flask_api import status
import json


class FacadeSetVersion:
    @staticmethod
    def get_all_latest_set_version(self):
        with SqlAlchemyConnection.session_scope() as connection:
            data_list = list()
            master_package_id_list = connection.query().select_from(EdgeType).join(EdgePackage,
                                                                                   EdgeType.id == EdgePackage.edge_type_id) \
                .add_columns(EdgeType.type, EdgeType.sub_type,
                             func.group_concat(EdgePackage.master_package_id)).group_by(EdgePackage.edge_type_id)
            for master_package_ids in master_package_id_list:
                master_tuple = tuple(master_package_ids[2].split(','))
                config_template_list = connection.query(
                    func.group_concat(MasterPackageConfigTemplate.config_template_id)).filter(
                    MasterPackageConfigTemplate.master_package_id.in_(master_tuple)).one()
                if config_template_list:
                    config_template_tuple = tuple(config_template_list[0].split(','))
                    latest_set_version = connection.query(TemplateSetVersion.set_version_no,TemplateSetVersion.created_time).filter(
                        TemplateSetVersion.config_template_id.in_(config_template_tuple)).order_by(
                        TemplateSetVersion.created_time.desc()).limit(1)[0]
                    if latest_set_version:
                        data = {"edgeType": master_package_ids[0], "edgeSubType": master_package_ids[1],
                                "templateSetVersion": str(latest_set_version[0]),"createdDateTime":str(latest_set_version[1])}
                        data_list.append(data)

            if data_list:
                return data_list
            else:
                return data_list
