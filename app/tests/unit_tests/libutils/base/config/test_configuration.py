import sys
import unittest

sys.path.append("src")


from src.libutils.base.config import configuration

class MockPopenConfigParser():
    communicate_returns = ""
    data_dict = {
        "Environment": {"type": "type"},
        "Database": {
            "username": "username",
                        "password": "password",
                        "host": "host",
                        "db_name": "db_name"},
        "DP": {
            "edge_details_url": "edge_details_url",
            "mac_details_url": "mac_details_url"},
        "Tar_Domain": {"name": "name"},
        "Log": {"level": "level"},
        "IPAM": {"subnet_search_url": "subnet_search_url",
                 "external_ip_details_url": "external_ip_details_url"}
    }

    def __init__(self, *uargs, **nargs):
        pass

    def communicate(self):
        return self.communicate_returns
    
    @staticmethod
    def ConfigParser():
        return MockPopenConfigParser()
    
    def read(self, path):
        self.passed_path = path
    
    def get(self, selection, option, *unargs, **nargs):
        return self.data_dict[selection][option]


class TestConfig(unittest.TestCase):
    def test_get_path(self):
        test_scenarios = [
            {
                "hostname": b"provisioningstore01.sboxdc.com",
                "expected_output": f"{configuration.config_path}production.ini"
            },
            {
                "hostname": b"provisioningstore01.stg.sboxdc.com",
                "expected_output": f"{configuration.config_path}staging.ini"
            },
            {
                "hostname": b"test_other",
                "expected_output": f"{configuration.config_path}default.ini"
            }
        ]
        configuration.Popen = MockPopenConfigParser
        for scenario in test_scenarios:
            hostname = scenario["hostname"]
            expected_output = scenario["expected_output"]
            MockPopenConfigParser.communicate_returns = [hostname]
            test_obj = configuration.Config()
            self.assertEqual(test_obj.get_path(), expected_output)

    def test_parse(self):
        test_scenarios = [
            {
                "hostname": b"provisioningstore01.sboxdc.com",
                "expected_output": f"{configuration.config_path}production.ini"
            },
            {
                "hostname": b"provisioningstore01.stg.sboxdc.com",
                "expected_output": f"{configuration.config_path}staging.ini"
            },
            {
                "hostname": b"test_other",
                "expected_output": f"{configuration.config_path}default.ini"
            }
        ]
        configuration.Popen = MockPopenConfigParser
        MockPopenConfigParser.communicate_returns = [b"this gets default"]
        configuration.configparser = MockPopenConfigParser
        for scenario in test_scenarios:
            hostname = scenario["hostname"]
            expected_output = scenario["expected_output"]
            MockPopenConfigParser.communicate_returns = [hostname]
            test_obj = configuration.Config()
            self.assertEqual(test_obj.parse().passed_path, expected_output)
    
    def test_populate_misc_config(self):
        configuration.configparser = MockPopenConfigParser
        expected_output = f"{configuration.config_path}misc.ini"

        self.assertEqual(
            configuration.Config.populate_misc_config().passed_path, expected_output)

    def test_populate_config(self):
        test_scenarios = [
            {
                "data_dict": {
                    "Environment": {"type": "type"},
                    "Database": {
                        "username": "username",
                        "password": "password",
                        "host": "host",
                        "db_name": "db_name"},
                    "DP": {
                        "edge_details_url": "edge_details_url",
                        "mac_details_url": "mac_details_url"},
                    "Tar_Domain": {"name": "name"},
                    "Log": {"level": "level"},
                    "IPAM": {"subnet_search_url": "subnet_search_url",
                             "external_ip_details_url": "external_ip_details_url"}
                },
                "expected_key_values": {
                    "environment_type": "type",
                    "database_user_name": "username",
                    "database_password": "password",
                    "database_host": "host",
                    "database_name": "db_name",
                    "edge_details_url": "edge_details_url",
                    "mac_details_url": "mac_details_url",
                    "domain_name": "name",
                    "log_level": "level",
                    "ipam_subnet_search_url": "subnet_search_url",
                    "external_ip_details_url": "external_ip_details_url"
                }
            },
            {
                "data_dict": {
                    "Environment": { "type" : "type_test" },
                    "Database": { 
                        "username" : "username_a",
                                  "password" : "password_b",
                                  "host" : "host_C",
                                  "db_name" : "db_name_D"},
                    "DP": {
                        "edge_details_url": "edge_details_urlE",
                        "mac_details_url": "mac_details_url+"},
                    "Tar_Domain": {"name": "nameg"},
                    "Log": {"level": "levelH"},
                    "IPAM": {"subnet_search_url":"subnet_search_urli",
                             "external_ip_details_url": "external_ip_details_urlj"}
                },
                "expected_key_values": {
                    "environment_type": "type_test",
                    "database_user_name": "username_a",
                    "database_password": "password_b",
                    "database_host": "host_C",
                    "database_name": "db_name_D",
                    "edge_details_url": "edge_details_urlE",
                    "mac_details_url": "mac_details_url+",
                    "domain_name": "nameg",
                    "log_level": "levelh",
                    "ipam_subnet_search_url": "subnet_search_urli",
                    "external_ip_details_url": "external_ip_details_urlj"
                }
            }
        ]
        configuration.configparser = MockPopenConfigParser
        configuration.Popen = MockPopenConfigParser
        for scenario in test_scenarios:
            MockPopenConfigParser.data_dict = scenario["data_dict"]
            test_obj = configuration.Config()
            for key in scenario["expected_key_values"]:
                expected_value = scenario["expected_key_values"][key]
                current_value = test_obj.__getattribute__(key)
                self.assertEqual(current_value, expected_value)

