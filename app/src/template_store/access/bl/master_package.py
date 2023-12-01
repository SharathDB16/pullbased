from template_store.access.dal.master_package import FacadeMasterPackage


class MasterPackage:

    @staticmethod
    def get_master_package_list():
        return FacadeMasterPackage.get_master_package_list()

    @staticmethod
    def add_master_package(args):
        return FacadeMasterPackage.add_master_package(name=args.name, description=args.description, path=args.path,
                                                      user=args.user, group=args.group, permission=args.permission,
                                                      uninstall_file=str.encode(
                                                          args.uninstall_file.read().decode('utf-8')),
                                                      pre_script_file=str.encode(
                                                          args.pre_script_file.read().decode('utf-8')),
                                                      post_script_file=str.encode(
                                                          args.post_script_file.read().decode('utf-8')))

    @staticmethod
    def assign_package_to_edge(args, master_id):
        return FacadeMasterPackage.assign_package_to_edge(master_package_id=master_id,
                                                          edge_type=args["edge_type"],
                                                          edge_sub_type=args["edge_sub_type"])

    @staticmethod
    def delete_package_from_edge(args, master_id):
        return FacadeMasterPackage.delete_package_from_edge(master_package_id=master_id,
                                                            edge_type=args["edge_type"],
                                                            edge_sub_type=args["edge_sub_type"])

    @staticmethod
    def update_master_package(args, master_id):
        dict_ = {}
        if args.name is not None:
            dict_.update({"name": args.name})
        if args.description is not None:
            dict_.update({"description": args.description})
        if args.path is not None:
            dict_.update({"path": args.path})
        if args.user is not None:
            dict_.update({"user": args.user})
        if args.group is not None:
            dict_.update({"group": args.group})
        if args.permission is not None:
            dict_.update({"permission": args.permission})
        if args.uninstall_file is not None:
            dict_.update({"uninstall_file": str.encode(args.uninstall_file.read().decode('utf-8'))})
        if args.pre_script_file is not None:
            dict_.update({"pre_script_file": str.encode(args.pre_script_file.read().decode('utf-8'))})
        if args.post_script_file is not None:
            dict_.update({"post_script_file": str.encode(args.post_script_file.read().decode('utf-8'))})
        return FacadeMasterPackage.update_master_package(dict_, master_id)

    @staticmethod
    def delete_master_package(master_id):
        return FacadeMasterPackage.delete_master_package(master_id)

    @staticmethod
    def assign_master_package_config(master_id, template_id):
        return FacadeMasterPackage.assign_master_package_config(master_id, template_id)

    @staticmethod
    def get_master_package_to_edge(edge_type, edge_sub_type):
        return FacadeMasterPackage.get_master_package_config(edge_type, edge_sub_type)

    @staticmethod
    def get_master_package_to_edge_id(edge_type_id):
        return FacadeMasterPackage.get_master_package_to_edge_id(edge_type_id)
