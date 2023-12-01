import sys
import unittest

sys.path.append("src")

from src.libutils.generator_helper import dpverse
from tests import utilities


class TestDPController(unittest.TestCase):
    def test_get_dp_verse_details(self):
        test_scenarios ={
            "standard": [
                {
                    "edge_id": "245216",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "static",
                                "edge_sub_type": "default"
                            },
                            "return_code": 200
                        }
                    },
                    "expected_output" :dict(
                        ap_count=4,
                        wdvpn_ip="10.255.255.188",
                        tp_name="TP_4_Coach_U-1291_zhoqsocorpifrxvvopcc_1575023958246_0",
                        dp_name="CMRL",
                        state_name="NA",
                        state_code="NA",
                        template_id=1
                    )
                }

            ],
            "exception": [
                {
                    "edge_id": "125216",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details1.json",
                            "jinja2": {
                                "edge_type": "static",
                                "edge_sub_type": "default"
                            },
                            "return_code": 200
                        }
                    },
                    "expected_exception": dpverse.HTTPExceptionFactory
                },
                {
                    "edge_id": "125216",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details2.json",
                            "jinja2": {
                                "edge_type": "static",
                                "edge_sub_type": "default"
                            },
                            "return_code": 400
                        }
                    },
                    "expected_exception": dpverse.HTTPExceptionFactory
                }
            ]
        }
        for scenario in test_scenarios["standard"]:
            edge_id = scenario["edge_id"]
            server_configs = scenario["server_configs"]
            expected_output = scenario["expected_output"]
            utilities.update_ipam_db_server_configs(server_configs)
            dp_controller = dpverse.DPController(edge_id)

            self.assertEqual(dp_controller.get_dp_verse_details(), expected_output)

        for scenario in test_scenarios["exception"]:
            edge_id = scenario["edge_id"]
            server_configs = scenario["server_configs"]
            expected_exception = scenario["expected_exception"]
            utilities.update_ipam_db_server_configs(server_configs)
            dp_controller = dpverse.DPController(edge_id)

            with self.assertRaises(expected_exception):
                dp_controller.get_dp_verse_details()
