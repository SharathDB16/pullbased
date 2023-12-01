import sys
import unittest

sys.path.append("src")

from src.libutils.generator_helper import externalip
from tests import utilities


class TestExternalIP(unittest.TestCase):
    def test_get_external_ip_details(self):
        test_scenarios = [
            {
                "edge_id": "245216",
                "server_configs": {
                    "ip_details": {
                        "template": "accurate_responses/ip_details2.json",
                        "jinja2": {
                            "edge_type": "static",
                            "edge_sub_type": "default"
                        },
                        "return_code": 200
                    }
                },
                "expected_output": dict(
                    lan_edge_ip1="192.168.2.4",
                    lan_edge_ip2="192.168.2.5",
                    lan_edge_bitmask="255.255.255.0",
                    lan_edge_gateway="192.168.2.1"
                )
            },
            {
                "edge_id": "245216",
                "server_configs": {
                    "ip_details": {
                        "template": "accurate_responses/ip_details1.json",
                        "jinja2": {
                            "edge_type": "static",
                            "edge_sub_type": "default"
                        },
                        "return_code": 200
                    }
                },
                "expected_output": None
            }

        ]
        for scenario in test_scenarios:
            edge_id = scenario["edge_id"]
            server_configs = scenario["server_configs"]
            expected_output = scenario["expected_output"]
            utilities.update_ipam_db_server_configs(server_configs)
            external_ip_details = externalip.ExternalIP(edge_id)

            self.assertEqual(
                external_ip_details.get_external_ip_details(), expected_output)
