from config_store.access.dal.template_set import FacadeTemplateSet
from libutils.utility import edge_type_subtype
from libutils.dal.edge_info import FacadeEdgeInfo
from config_store.access.bl import log


class TemplateSet:

    @staticmethod
    def get_all_templates(edge_id, set_version):
        edge_type, edge_sub_type, switch_type, template_id, tag_list = edge_type_subtype(edge_id) or (None, None, None, None, None)
        if edge_type is not None:
            edge_type = FacadeEdgeInfo.get_edge_by_type_subtype(edge_type, edge_sub_type)
            master_package_ids = FacadeTemplateSet.get_master_package_id(edge_type["id"])

            if edge_type != "mobile":
                switch_package_id = FacadeTemplateSet.get_switch_package_id(edge_type["id"], switch_type)
                master_package_ids.extend(switch_package_id)

            template_set, set_version = FacadeTemplateSet.get_template_set(current_set_version=set_version, tag_list=tag_list)
            edge_template_set = list()

            for master_id in master_package_ids:
                master_dict = dict()

                if master_id in template_set:
                    config_dict = list()
                    config_set = template_set[master_id]

                    for template_id in config_set:
                        template_metadata = FacadeTemplateSet.get_template_details(template_id)
                        item = dict()
                        item["name"] = template_metadata["name"]
                        item["description"] = template_metadata["description"]
                        item["path"] = template_metadata["path"].replace('"$edge_id"', edge_id)
                        item["owner"] = template_metadata["owner"]
                        item["group"] = template_metadata["group"]
                        item["permissions"] = template_metadata["permissions"]
                        item["template_id"] = template_metadata["template_id"]

                        template_version = config_set[template_id][0]
                        version_attributes = FacadeTemplateSet.get_template_version_details(template_id, template_version)
                        version = dict()
                        version["version_no"] = version_attributes["version_no"]
                        version["comment"] = version_attributes["comment"]

                        item.update({"latest_version": version})
                        config_dict.append(item)

                    master_package_details = FacadeTemplateSet.get_master_details(master_id)
                    master_dict.update({"name": master_package_details["name"]})
                    master_dict.update({"description": master_package_details["description"]})
                    master_dict.update({"status": master_package_details["status"]})
                    master_dict.update({"execution_sequence": master_package_details["execution_sequence"]})
                    master_dict.update({"master_package_id": master_id})
                    master_dict.update({"config_template": config_dict})
                    edge_template_set.append(master_dict)
            return edge_template_set, set_version
