from config_store.access.bl.template_set import TemplateSet
from config_store.access.dal.template_set import FacadeTemplateSet
from libutils.utility import create_path_if_not_exists
from libutils.base.config import tar_path, edge_package_structure_path
from libutils.utility import edge_type_subtype, get_context
from libutils.base.config.configuration import config_obj
from libutils.dal.edge_info import FacadeEdgeInfo
from jinja2 import Template
from config_store.access.bl import log
import requests
import time
import os


class ConfigGenerator:

    @staticmethod
    def generate_package(edge_id, mac_address, set_version):
        if mac_address:
            mac_address_list = mac_address.split("|")
            for mac_address in mac_address_list:
                response = requests.get("{}{}".format(config_obj.mac_details_url, mac_address)).json()
                if response["meta"]["code"] == 200:
                    edge_id = response["data"]["edgeId"]
                    break

            if edge_id is None:
                return None, None, None, None

        edge_template_set, set_version = TemplateSet.get_all_templates(edge_id, set_version)

        if len(edge_template_set) == 0:
            log.info("No change in configuration for edge id {}".format(edge_id))
            return edge_id, set_version, None, None

        if not os.path.exists(tar_path):
            os.mkdir(tar_path)

        folder_name = "{}-{}".format(edge_id, time.strftime("%Y%m%d%H%M%S"))
        edge_type, edge_sub_type, switch_type, template_id, tag_list = edge_type_subtype(edge_id) or (None, None, None, None, None)
        ConfigGenerator.create_folder_structure(folder_name, edge_template_set, edge_type, edge_sub_type, edge_id)

        edge_id_path = "{}/{}/".format(edge_package_structure_path, folder_name)
        os.chdir(edge_id_path)

        with open("template_path.txt", "w+") as f:
            for template_list in edge_template_set:
                for template in (template_list["config_template"]):
                    f.write(template["path"])
                    f.write('\n')

        cmd = "{}{}{}".format("tar cfJ ", folder_name, ".tar.xz *")
        os.system(cmd)
        os.system("mv {}/{}.tar.xz {}".format(edge_id_path, folder_name, tar_path))

        return edge_id, set_version, "{}{}.tar.xz".format(config_obj.domain_name, folder_name), template_id

    @staticmethod
    def create_folder_structure(folder_name, template_set, edge_type, edge_sub_type, edge_id):

        # Create parent path
        create_path_if_not_exists("{}/{}".format(edge_package_structure_path, folder_name))

        # Create folder for edge_id
        edge_id_path = "{}/{}".format(edge_package_structure_path, folder_name)
        if not os.path.exists(edge_id_path):
            os.mkdir(edge_id_path)

        context_class = get_context(edge_type, edge_sub_type)
        context_obj = context_class(edge_id, edge_type, edge_sub_type)
        context = context_obj.get_context()
        context.update({"edge_id": edge_id})

        for master_package in template_set:

            master_package_name = master_package["name"].lower()
            if master_package["execution_sequence"] is not None and master_package["execution_sequence"] != "":
                master_package_name = "{}_{}".format(master_package["execution_sequence"], master_package_name)

            master_package_path_location = "{}/{}".format(edge_id_path, master_package_name)
            if not os.path.exists(master_package_path_location):
                os.mkdir(master_package_path_location)

            master_files = FacadeTemplateSet.get_master_files(master_package["master_package_id"])
            ConfigGenerator.create_execution_sequence_file(edge_id_path, master_package_name)

            if master_package["status"] == 0:
                ConfigGenerator.create_unistall_file(master_package_path_location, master_files["uninstall_file"])
            else:
                ConfigGenerator.create_config_template_file(master_package_path_location,
                                                            master_package["config_template"], context)
                ConfigGenerator.create_pre_script_file(master_package_path_location, master_files["pre_script_file"],
                                                       master_package["config_template"])
                ConfigGenerator.create_post_script_file(master_package_path_location, master_files["post_script_file"])

        ConfigGenerator.create_install_file(edge_id_path)
        ConfigGenerator.create_miscellaneous_file(edge_id_path, context)
        edge_info = FacadeEdgeInfo.get_edge_by_type_subtype(edge_type, edge_sub_type)
        ConfigGenerator.create_pre_general_script_file(edge_id_path, edge_info["pre_gen_script_file"])
        ConfigGenerator.create_post_general_script_file(edge_id_path, edge_info["post_gen_script_file"])

    @staticmethod
    def create_install_file(path):

        script = '''\
#!/bin/bash
(
sudo makerw
pkg_path=/opt/sugarbox/provisioningagent/config/new/$1 
cd "$pkg_path"

array=$(sort -n package_sequence.txt)
source pre_gen_script.sh
for package in $array; do
    echo "$package"

    if [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then
        echo "Breaking the execution"
        break
    fi

    if [ -e $package/uninstall.sh ]; then
        echo "$package | Uninstall file present"
        source $package/uninstall.sh
    fi
    if [ -e $package/prescript.sh ]; then
        echo "======================$package START============================"
        echo "$package | Prescript file present | Executing it"
        cd $package
        source prescript.sh
        source postscript.sh

        if status_check; then
	        echo "INFO: $package Worked..."
	        if [ -e /opt/sugarbox/provisioningagent/etc/status_fail.txt ]; then
			    rm /opt/sugarbox/provisioningagent/etc/status_fail.txt
		    fi
	    else
	        echo "ERROR: $package Not worked..."
	        touch /opt/sugarbox/provisioningagent/etc/status_fail.txt
	    fi
        cd "$pkg_path"
        echo "======================$package END==============================="
    fi
done
source post_gen_script.sh
) 2>&1 | sudo tee -a /var/log/sugarbox/provisioningagent/install_$1.log
        '''

        with open("{}/{}".format(path, "install.sh"), "a") as file:
            file.write(script)
        os.chmod("{}/{}".format(path, "install.sh"), 0o755)

    @staticmethod
    def create_unistall_file(path, content):
        with open("{}/{}".format(path, "uninstall.sh"), "a") as file:
            file.write(content)
        os.chmod("{}/{}".format(path, "uninstall.sh"), 0o755)

    @staticmethod
    def create_pre_script_file(path, content, config_template):
        with open("{}/{}".format(path, "prescript.sh"), "a") as file:
            file.write(content)
            # cmd = "sed -i '1 i #!/bin/bash' {}/{}".format(path, "prescript.sh")
            # print(cmd)
            # os.system(cmd)
            file.write("\n## File attributes #")
            for template in config_template:
                config_name = template["path"].split("/")[-1]
                file.write("\nsudo cp {} {} \n".format(config_name, template["path"]))
                file.write("echo 'File replaced {}'\n".format(template["path"]))

                if template["owner"] is not None and template["owner"] != "":
                    file.write("sudo chown {} {} \n".format(template["owner"], template["path"]))
                    file.write("echo 'changed owner of {}'\n".format(config_name))

                if template["group"] is not None and template["group"] != "":
                    file.write("sudo chgrp {} {} \n".format(template["group"], template["path"]))
                    file.write("echo 'changed group of {}'\n".format(config_name))

                if template["permissions"] is not None and template["permissions"] != "":
                    file.write("sudo chmod {} {} \n".format(template["permissions"], template["path"]))
                    file.write("echo 'changed permissions of {}'\n".format(config_name))

        os.chmod("{}/{}".format(path, "prescript.sh"), 0o755)

    @staticmethod
    def create_config_template_file(path, config_template, context):
        for template in config_template:
            template_name = template["path"].split("/")[-1]
            version_details = FacadeTemplateSet.get_template_version_details(template["template_id"],
                                                                             template["latest_version"]["version_no"])

            with open("{}/{}".format(path, template_name), "w") as file:
                if "{#" in version_details["template_file"]:
                    template = version_details["template_file"]
                else:
                    try:
                        template = Template(version_details["template_file"]).render(context)
                    except Exception as e:
                        template = version_details["template_file"]
                file.write(template)

    @staticmethod
    def create_post_script_file(path, content):
        with open("{}/{}".format(path, "postscript.sh"), "a") as file:
            file.write(content)
        os.chmod("{}/{}".format(path, "postscript.sh"), 0o755)

    @staticmethod
    def create_execution_sequence_file(path, package_name):
        with open("{}/{}".format(path, "package_sequence.txt"), "a") as file:
            file.write("{}\n".format(package_name))

    @staticmethod
    def create_pre_general_script_file(path, content):
        with open("{}/{}".format(path, "pre_gen_script.sh"), "a") as file:
            file.write("{}\n".format(content))
        os.chmod("{}/{}".format(path, "pre_gen_script.sh"), 0o755)

    @staticmethod
    def create_post_general_script_file(path, content):
        with open("{}/{}".format(path, "post_gen_script.sh"), "a") as file:
            file.write("{}\n".format(content))
        os.chmod("{}/{}".format(path, "post_gen_script.sh"), 0o755)

    @staticmethod
    def create_miscellaneous_file(path, context):
        with open("{}/{}".format(path, "misc.lst"), "a") as file:
            file.write("lan_first_ip={}\n".format(context["lan_first_ip"]))
            file.write("wan_first_ip={}\n".format(context["wan_first_ip"]))
            file.write("edge_id={}\n".format(context["edge_id"]))
