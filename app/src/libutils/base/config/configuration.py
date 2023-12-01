import configparser
from subprocess import Popen, PIPE
from libutils.base.config import config_path


class Config:

    def __init__(self):
        self.config_path = self.get_path()
        self.populate_config()

    def parse(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)
        return config_parser

    def get_path(self):
        hostname = Popen(['hostname', '-f'], stdout=PIPE).communicate()[0].decode().strip()
        if "provisioningstore01.sboxdc.com" in hostname:
            env = "production.ini"
        elif "provisioningstore01.stg.sboxdc.com" in hostname:
            env = "staging.ini"
        else:
            env = "default.ini"

        return "{}{}".format(config_path, env)

    def populate_misc_config():
        file = 'misc.ini'
        full_path = "{}{}".format(config_path, file)
        config_parser = configparser.ConfigParser()
        config_parser.read(full_path)
        return config_parser

    def populate_config(self):
        config_obj = self.parse()
        self.environment_type = config_obj.get("Environment", "type")
        self.database_user_name = config_obj.get("Database", "username")
        self.database_password = config_obj.get("Database", "password")
        self.database_host = config_obj.get("Database", "host")
        self.database_name = config_obj.get("Database", "db_name")

        self.edge_details_url = config_obj.get("DP", "edge_details_url")
        self.mac_details_url = config_obj.get("DP", "mac_details_url")
        self.domain_name = config_obj.get("Tar_Domain", "name")
        self.log_level = config_obj.get("Log", "level").lower()

        self.ip_details_url = config_obj.get("IPAM", "ip_details_url")
        self.ipam_subnet_search_url = config_obj.get("IPAM", "subnet_search_url")
        self.wireguard_details_url = config_obj.get("IPAM", "wireguard_details_url")
        self.external_ip_details_url = config_obj.get("IPAM", "external_ip_details_url")
        self.cdn_external_ip_details_url = config_obj.get("IPAM", "cdn_external_ip_details_url")

        self.config_template_url = config_obj.get("Pullbased", "config_template_url")
        self.version_update_url = config_obj.get("Pullbased", "version_update_url")
        self.server_url = config_obj.get("Pullbased", "server_url")
        self.service_name = config_obj.get("Pullbased", "service_name")

        self.fup_template_id = config_obj.get("Template", "fup_template_id")
        self.sbox_template_id = config_obj.get("Template", "sbox_template_id")
        self.wg_template_id = config_obj.get("Template", "wg_template_id")

config_obj = Config()
