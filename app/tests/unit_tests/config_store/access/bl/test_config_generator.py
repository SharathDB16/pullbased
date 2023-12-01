import sys
import unittest
from unittest import mock
from unittest.mock import patch

sys.path.append("src")

from src.config_store.access.bl import config_generator

class TestConfigGenerator(unittest.TestCase):
    @patch("src.config_store.access.bl.config_generator.requests")
    def test_get_edge_id_from_mac(self, request_mock):
        test_scenarios = [
            {
                "input": dict(mac_address="1|2|3|4"),
                "request_get_called_with": "{}{}".format(
                    config_generator.config_obj.mac_details_url, "2"),
                "responses": [
                    {
                        "meta": dict(code=404)
                    },
                    {
                        "meta": dict(code=200),
                        "data": dict(edgeId="125216")
                    }
                ],
                "expected":"125216"
            },
            {
                "input": dict(mac_address="1|2|3|4"),
                "request_get_called_with": "{}{}".format(
                    config_generator.config_obj.mac_details_url, "3"),
                "responses": [
                    {
                        "meta": dict(code=404)
                    },
                    {
                        "meta": dict(code=404)
                    },
                    {
                        "meta": dict(code=200),
                        "data": dict(edgeId="22E941")
                    }
                ],
                "expected": "22E941"
            }
        ]
        for scenario in test_scenarios:
            request_mock.get.return_value = request_mock
            request_mock.json.side_effect = scenario["responses"]
            expected = scenario["expected"]
            returned = config_generator.ConfigGenerator.get_edge_id_from_mac(**scenario["input"])
            self.assertEqual(returned, expected)
            request_mock.get.assert_called_with(
                scenario["request_get_called_with"])

    @patch("src.config_store.access.bl.config_generator.os")
    @patch("src.config_store.access.bl.config_generator.time.strftime")
    @patch("src.config_store.access.bl.config_generator.edge_type_subtype")
    @patch("src.config_store.access.bl.config_generator.TemplateSet.get_all_templates")
    @patch("src.config_store.access.bl.config_generator.ConfigGenerator.create_folder_structure")
    @patch("src.config_store.access.bl.config_generator.ConfigGenerator.get_edge_id_from_mac")
    def test_generate_package(self, mac_to_edge_mock, create_folder_structure_mock, get_all_templates_mock, edge_type_subtype_mock, strftime_mock, os_mock):
        test_scenarios = [
            {
                "input": dict(edge_id=None, mac_address="test", set_version=None),
                "expected": (None, None, None),
                "mac_to_edge_mock": {"side_effect": [None]},
                "call_patterns":[
                    {
                        "object": mac_to_edge_mock,
                        "called_with": ["test"]
                    }
                ]
            },
            {
                "input": dict(edge_id=None, mac_address="test", set_version=None),
                "expected": ("125216", None, None),
                "mac_to_edge_mock": {"side_effect": ["125216"]},
                "get_all_templates_mock":{"side_effect": [([], None)]},
                "call_patterns":[
                    {
                        "object": mac_to_edge_mock,
                        "called_with": ["test"]
                    },
                    {
                        "object": get_all_templates_mock,
                        "called_with": ["125216", None]
                    }
                ]
            },
            {
                "input": dict(edge_id=None, mac_address="test", set_version=None),
                "expected": ("225216", "set_version", None),
                "mac_to_edge_mock": {"side_effect": ["225216"]},
                "get_all_templates_mock":{"side_effect": [([], "set_version")]},
                "call_patterns":[
                    {
                        "object": mac_to_edge_mock,
                        "called_with": ["test"]
                    },
                    {
                        "object": get_all_templates_mock,
                        "called_with": ["225216", None]
                    }
                ]
            },
            {
                "input": dict(edge_id=None, mac_address="test", set_version="set_version"),
                "expected": ("225216", "set_version1", None),
                "mac_to_edge_mock": {"side_effect": ["225216"]},
                "get_all_templates_mock":{"side_effect": [([], "set_version1")]},
                "call_patterns":[
                    {
                        "object": mac_to_edge_mock,
                        "called_with": ["test"]
                    },
                    {
                        "object": get_all_templates_mock,
                        "called_with": ["225216", "set_version"]
                    }
                ]
            },
            {
                "input": dict(edge_id="235E3A", mac_address=None, set_version="set_version"),
                "expected": ("235E3A", "set_version2", "{}{}.tar.xz".format(config_generator.config_obj.domain_name, "235E3A-replaced_time")),
                "mac_to_edge_mock": {"side_effect": Exception},
                "get_all_templates_mock":{"side_effect": [("1234", "set_version2")]},
                "strftime_mock":{"return_value": "replaced_time"},
                "edge_type_subtype_mock":{"side_effect":[("edge_typeA", "edge_sub_typeB", "switch_typeC")]},
                "os_mock":{"side_effect":[None, None, None]},
                "call_patterns": [
                    {
                        "object": get_all_templates_mock,
                        "called_with": ["235E3A", "set_version"]
                    },
                    {
                        "object": edge_type_subtype_mock,
                        "called_with": ["235E3A"]
                    },
                    {
                        "object": create_folder_structure_mock,
                        "called_with": ["235E3A-replaced_time", "1234", "edge_typeA", "edge_sub_typeB", "235E3A"]
                    },
                    {
                        "object": os_mock.chdir,
                        "called_with": ["{}/{}/".format(config_generator.edge_package_structure_path, "235E3A-replaced_time")]
                    },
                    {
                        "object": os_mock.system,
                        "called_with": ["mv /opt/sugarbox/config/edge_package_structure/235E3A-replaced_time/235E3A-replaced_time.tar.xz /opt/sugarbox/config/tar"]
                    }
                ]
            }
        ]
        for scenario in test_scenarios:
            mac_to_edge_mock.configure_mock(
                **(scenario.get("mac_to_edge_mock", {})))
            get_all_templates_mock.configure_mock(
                **(scenario.get("get_all_templates_mock", {})))
            edge_type_subtype_mock.configure_mock(
                **(scenario.get("edge_type_subtype_mock", {})))
            strftime_mock.configure_mock(
                **(scenario.get("strftime_mock", {})))
            os_mock.configure_mock(
                **(scenario.get("os_mock", {})))
            expected = scenario["expected"]
            returned = config_generator.ConfigGenerator.generate_package(**scenario["input"])
            self.assertEqual(returned, expected)
            call_patterns = scenario["call_patterns"]
            for pattern in call_patterns:
                mock_object = pattern["object"]
                called_with = pattern.get("called_with", None)
                if called_with is None:
                    mock_object.assert_called()
                else:
                    mock_object.assert_called_with(*called_with)

