from datetime import datetime
from libutils.base.db.models import EdgeTelemetryInfo, EdgeType
from libutils.base.db.connection import SqlAlchemyConnection
from template_store.access.dal import log
from libutils.base.config.configuration import Config


class FacadeEdgeTelemetry:
    @staticmethod
    def add_telemetry_info(code_id=None, edge_id=None, package_name=None, template_set_version=None,
                           report_status=None):
        try:
            telemetry_record = EdgeTelemetryInfo(code_id=code_id, edge_id=edge_id, package_name=package_name,
                                                 template_set_version=template_set_version,
                                                 report_status=str(report_status))
            with SqlAlchemyConnection.session_scope() as connection:
                connection.add(telemetry_record)
            return True
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def get_edge_telemetry_list():
        with SqlAlchemyConnection.session_scope() as connection:
            list_ = []
            telemetry_list = connection.query(EdgeTelemetryInfo.edge_id).distinct()
            for telemetry_values in telemetry_list:
                list_.append(telemetry_values.edge_id)
            edge_id_list = {"edge_id_list": list_}
            return {"data": edge_id_list}

    @staticmethod
    def get_edge_telemetry(edge_id=None):
        with SqlAlchemyConnection.session_scope() as connection:
            data = []
            obj = connection.query(EdgeTelemetryInfo).filter(
                EdgeTelemetryInfo.edge_id == edge_id, EdgeTelemetryInfo.code_id == 3).\
                order_by(EdgeTelemetryInfo.template_set_version.desc()).first()
            if obj:
                package_consumed_time = datetime.strftime(obj.created_time, "%d-%m-%Y %H:%M:%S")
                data = {"edge_id": obj.edge_id, "template_version": str(obj.template_set_version),
                        "updated_time": package_consumed_time}
            return {"meta": {'code': 200}, "data": data}

    @staticmethod
    def get_edge_telemetry_info_list(page_num=None):
        misc_config = Config.populate_misc_config()
        per_page = int(misc_config.get('Misc', 'per_page'))
        start = 0
        end = per_page
        if page_num != 1:
            start = per_page * (page_num - 1)
            end = start + per_page
        print(start, end)
        meta_info = {"code": 200, "timestamp": str(datetime.now())}
        pagination = {"total": 0, "page": page_num, "per_page": per_page}
        with SqlAlchemyConnection.session_scope() as connection:
            list_ = []
            distinct_edge_id_obj = connection.query(EdgeTelemetryInfo.edge_id).filter(EdgeTelemetryInfo.template_set_version != "0.00").distinct(EdgeTelemetryInfo.edge_id).limit(per_page).offset(start)
            total_records = connection.query(EdgeTelemetryInfo.edge_id).filter(EdgeTelemetryInfo.template_set_version != "0.00").group_by(EdgeTelemetryInfo.edge_id).count()
            pagination.update({'total': total_records})
            for data_obj in distinct_edge_id_obj:
                edge_data = connection.query(EdgeTelemetryInfo).filter(EdgeTelemetryInfo.edge_id == data_obj.edge_id,EdgeTelemetryInfo.template_set_version != "0.00").\
                    order_by(EdgeTelemetryInfo.created_time.desc()).first()
                if edge_data:
                    report_status = eval(edge_data.report_status)
                    template_set_version = edge_data.template_set_version
                    download_obj = connection.query(EdgeTelemetryInfo).filter(EdgeTelemetryInfo.edge_id == data_obj.edge_id,
                                                                              EdgeTelemetryInfo.template_set_version == edge_data.template_set_version,
                                                                              EdgeTelemetryInfo.code_id == 1).order_by(
                        EdgeTelemetryInfo.created_time.desc()).first()
                    consumed_time = None
                    downloaded_time = None
                    download_status = False
                    consumed_status = False
                    if download_obj:
                        download_status = True
                        downloaded_time = datetime.strftime(download_obj.created_time, "%Y-%m-%d %H:%M:%S")

                    consumed_obj = connection.query(EdgeTelemetryInfo).filter(
                        EdgeTelemetryInfo.template_set_version == edge_data.template_set_version,
                        EdgeTelemetryInfo.edge_id == edge_data.edge_id,
                        EdgeTelemetryInfo.code_id == 3).order_by(EdgeTelemetryInfo.
                                                                 created_time.desc()).first()

                if consumed_obj:
                    consumed_status = True
                    consumed_time = datetime.strftime(consumed_obj.created_time, "%Y-%m-%d %H:%M:%S")

                try:
                    data = {"edge_id": data_obj.edge_id, "package_name": report_status["package_name"],
                            "template_set_version": str(template_set_version),
                            "ip_address": report_status["ip_address"],
                            "consumed": consumed_status,
                            "downloaded": download_status,
                            "downloaded_time": downloaded_time,
                            "consumed_time": consumed_time
                            }
                    list_.append(data)
                except KeyError as e:
                    log.error(e)

            if not distinct_edge_id_obj:
                meta_info.update({'code': 204})

            return {"meta": meta_info, "data": list_, "pagination": pagination}

    @staticmethod
    def get_edge_telemetry_info(edge_id=None):
        meta_info = {"code": 200, "timestamp": str(datetime.now())}
        data = {}
        with SqlAlchemyConnection.session_scope() as connection:
            data_obj = connection.query(EdgeTelemetryInfo.code_id, EdgeTelemetryInfo.created_time,
                                        EdgeTelemetryInfo.report_status, EdgeTelemetryInfo.edge_id,
                                        EdgeTelemetryInfo.template_set_version).filter(EdgeTelemetryInfo.template_set_version != "0.00").order_by(EdgeTelemetryInfo.created_time.desc()).filter(
                EdgeTelemetryInfo.edge_id == edge_id).first()
            if data_obj:
                report_status = eval(data_obj.report_status)
                download_obj = connection.query(EdgeTelemetryInfo).filter(EdgeTelemetryInfo.edge_id == data_obj.edge_id,
                                                                          EdgeTelemetryInfo.template_set_version == data_obj.template_set_version,
                                                                          EdgeTelemetryInfo.code_id == 1).order_by(
                    EdgeTelemetryInfo.created_time.desc()).first()
                consumed_time = None
                downloaded_time = None
                download_status = False
                consumed_status = False
                if download_obj:
                    download_status = True
                    downloaded_time = datetime.strftime(download_obj.created_time, "%d-%m-%Y %H:%M:%S")

                consumed_obj = connection.query(EdgeTelemetryInfo).filter(
                    EdgeTelemetryInfo.template_set_version == data_obj.template_set_version,
                    EdgeTelemetryInfo.edge_id == data_obj.edge_id,
                    EdgeTelemetryInfo.code_id == 3).order_by(EdgeTelemetryInfo.
                                                             created_time.desc()).first()

                if consumed_obj:
                    consumed_status = True
                    consumed_time = datetime.strftime(consumed_obj.created_time, "%d-%m-%Y %H:%M:%S")
                try:
                    data = {"edge_id": report_status["edge_id"], "package_name": report_status["package_name"],
                            "template_set_version": str(report_status["template_set_version"]),
                            "ip_address": report_status["ip_address"],
                            "consumed": consumed_status,
                            "downloaded": download_status,
                            "downloaded_time": downloaded_time,
                            "consumed_time": consumed_time,
                            }
                except KeyError as e:
                    log.error(e)
            else:
                meta_info.update({'code': 204})

            return {"meta": meta_info, "data": data}

    @staticmethod
    def get_edge_telemetry_latest_info():
        with SqlAlchemyConnection.session_scope() as connection:
            telemetry_list = connection.query(EdgeTelemetryInfo.edge_id).distinct()
            latest_version_list = []
            for data in telemetry_list:
                obj = connection.query(EdgeTelemetryInfo).filter(EdgeTelemetryInfo.code_id == 3,
                                                                 EdgeTelemetryInfo.edge_id == data[0]).order_by(
                                                                 EdgeTelemetryInfo.id.desc()).first()
                if obj:
                    latest_version_list.append({"edge_id": obj.edge_id, "package_name": obj.package_name,
                                                "template_set_version": float(obj.template_set_version),
                                                "package_updated_time": obj.created_time.strftime("%d-%m-%Y %H:%M:%S")})

            return {"meta": {'code': 200}, "data": latest_version_list}

    @staticmethod
    def get_edge_telemetry_edge_types():
        with SqlAlchemyConnection.session_scope() as connection:
            edge_type_details = connection.query(EdgeType.id, EdgeType.type, EdgeType.sub_type)

            edge_type_list = []
            for edge in edge_type_details:
                edge_type_list.append({"id": edge.id, "edge_type": edge.type, "edge_subtype": edge.sub_type})
            return {"meta": {'code': 200}, "data": edge_type_list}
