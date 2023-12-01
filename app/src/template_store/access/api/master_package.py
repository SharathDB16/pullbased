import werkzeug
from flask_api import status
from flask import jsonify
from flask_restful import Resource, reqparse
from libutils.utility import non_empty_string
from template_store.access.bl.master_package import MasterPackage


class MasterPackageListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=non_empty_string, required=True,
                                   help='Name must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('description', type=non_empty_string, required=True,
                                   help='Description must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('path', type=non_empty_string, required=False,
                                   help='Path must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('user', type=non_empty_string, required=False,
                                   help='User must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('group', type=non_empty_string, required=False,
                                   help='Group must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('permission', type=non_empty_string, required=False,
                                   help='Permission must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('uninstall_file', type=werkzeug.FileStorage, required=True,
                                   help='Uninstall file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('pre_script_file', type=werkzeug.FileStorage, required=True,
                                   help='Pre script file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('post_script_file', type=werkzeug.FileStorage, required=True,
                                   help='Post script file must be provided', nullable=False,
                                   location='files')

    def get(self):
        return MasterPackage.get_master_package_list()

    def post(self):
        args = self.reqparse.parse_args()
        status_val = MasterPackage.add_master_package(args)
        if status_val:
            return jsonify({"message": "Master Package added"})
        else:
            return {"message": "Master Package not added", "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class MasterPackageResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=non_empty_string, required=False,
                                   help='Name must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('description', type=non_empty_string, required=False,
                                   help='Description must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('path', type=non_empty_string, required=False,
                                   help='Path must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('user', type=non_empty_string, required=False,
                                   help='User must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('group', type=non_empty_string, required=False,
                                   help='Group must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('permission', type=non_empty_string, required=False,
                                   help='Permission must be provided with string value',
                                   nullable=False, location='values')

        self.reqparse.add_argument('uninstall_file', type=werkzeug.FileStorage, required=False,
                                   help='Uninstall file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('pre_script_file', type=werkzeug.FileStorage, required=False,
                                   help='Pre script file must be provided', nullable=False,
                                   location='files')

        self.reqparse.add_argument('post_script_file', type=werkzeug.FileStorage, required=False,
                                   help='Post script file must be provided', nullable=False,
                                   location='files')

    def put(self, master_id):
        args = self.reqparse.parse_args()
        status_val = MasterPackage.update_master_package(args, master_id)
        if status_val == 1:
            return jsonify({"message": "Master Package updated"})
        elif status_val == 0:
            return {"message": "Master Package not updated",
                    "description": "The requested master package is not present"}, status.HTTP_404_NOT_FOUND
        else:
            return {"message": "Master Package not updated",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST

    def delete(self, master_id):
        status_val = MasterPackage.delete_master_package(master_id)
        if status_val:
            return jsonify({"message": "Master Package deleted"})
        else:
            return {"message": "Master Package not deleted",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class AssignMasterPackageResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('edge_type', type=non_empty_string, required=True,
                                   nullable=False, help='Edge type must be provided with string value',
                                   location='json')

        self.reqparse.add_argument('edge_sub_type', type=non_empty_string, required=True,
                                   nullable=False, help='Edge sub type must be provided with string value',
                                   location='json')

    def post(self, master_id):
        args = self.reqparse.parse_args()
        status_, already_assigned = MasterPackage.assign_package_to_edge(args, master_id)

        if already_assigned is True:
            return jsonify({"message": "Package already assigned"})
        elif status_ is True:
            return jsonify({"message": "Package assigned"})
        else:
            return {"message": "Package not assigned",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST

    def delete(self, master_id):
        args = self.reqparse.parse_args()
        status_, invalid_package_id = MasterPackage.delete_package_from_edge(args, master_id)

        if invalid_package_id is True:
            return jsonify({"message": "Invalid package id"})
        elif status_ is True:
            return jsonify({"message": "Package deleted"})
        else:
            return {"message": "Package not deleted",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class AssignMasterPackageConfigResource(Resource):

    def post(self, master_id, template_id):
        status_, already_assigned = MasterPackage.assign_master_package_config(master_id, template_id)

        if already_assigned is True:
            return jsonify({"message": "Master package config already assigned"})
        elif status_ is True:
            return jsonify({"message": "Master package config assigned"})
        else:
            return {"message": "Master package config not assigned",
                    "description": "Something went wrong"}, status.HTTP_400_BAD_REQUEST


class GetMasterPackageResource(Resource):

    def get(self, edge_type, edge_sub_type):
        package_data = MasterPackage.get_master_package_to_edge(edge_type, edge_sub_type)
        if "data" in package_data:
            return package_data
        elif "description" in package_data:
            return package_data, status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return package_data, status.HTTP_404_NOT_FOUND


class GetMasterPackageListResource(Resource):

    def get(self, edge_type_id):
        return MasterPackage.get_master_package_to_edge_id(edge_type_id)
