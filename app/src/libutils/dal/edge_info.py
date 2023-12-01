from libutils.base.db.models import EdgeType
from libutils.base.db.connection import SqlAlchemyConnection


class FacadeEdgeInfo:

    @staticmethod
    def get_edge_by_type_subtype(type_=None, sub_type=None):
        with SqlAlchemyConnection.session_scope() as connection:
            edge_type_query = connection.query(EdgeType).filter(EdgeType.type == type_, EdgeType.sub_type == sub_type)
            if edge_type_query.count():
                edge_info = edge_type_query.first()
                return {
                    "id": edge_info.id,
                    "edge_type": edge_info.type,
                    "edge_sub_type": edge_info.sub_type,
                    "pre_gen_script_file": edge_info.pre_gen_script_file.decode(),
                    "post_gen_script_file": edge_info.post_gen_script_file.decode()
                }
            else:
                return None
