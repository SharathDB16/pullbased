import sys
import unittest

sys.path.append("src")


from src.config_store.access.api import config_package

generate_package_returns = (None, None, None)

class MockConfigGeneratorRequestParser:

    def __init__(self):
        self.args_dict = dict()
    @staticmethod
    def generate_package(edge_id, mac_address, set_version):
        return generate_package_returns
    
    def add_argument(self, argument, *args, **named_args):
        self.args_dict[argument] = named_args
    
    def parse_args(self):
        return dict(edge_id="", mac_address="", set_version="")


class TestConfigPackage(unittest.TestCase):

    def test_init(self):
        config_package.reqparse.RequestParser = MockConfigGeneratorRequestParser
        test_obj = config_package.ConfigPackageResource()
        expected_dict = {
            'mac_address':dict(type = config_package.non_empty_string, required = False,
            help = 'Invalid mac_address',
            nullable = False),
            'edge_id': dict(type = config_package.validate_edge_id, required = False,
            help = 'Invalid edge id',
            nullable = False),
            'set_version': dict(type=float, required=False,
                                   help='Invalid set version',
                                   nullable=False)
        }
        self.assertEqual(test_obj.reqparse.args_dict, expected_dict)



    def test_get(self):
        test_scenarios = [{
            "generate_package_returns": (None, None, None),
            "expected_output": (
                {
                    "data": "Edge Id not found for given mac_address in DP"
                },
                config_package.status.HTTP_404_NOT_FOUND
            )
        }, {
            "generate_package_returns": ("", None, None),
            "expected_output": (
                {
                    "data": "No changes in configuration",
                    "edge_id": "",
                    "latest_set_version": None
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": (None, "", None),
            "expected_output": (
                {
                    "data": "No changes in configuration",
                    "edge_id": None,
                    "latest_set_version": ""
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": ("", "", None),
            "expected_output": (
                {
                    "data": "No changes in configuration",
                    "edge_id": "",
                    "latest_set_version": ""
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": ("", None, "package_path1"),
            "expected_output": (
                {
                    "data": "Package generated",
                    "path": "package_path1",
                    "edge_id": "",
                    "latest_set_version": None
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": (None, "", "package_path2"),
            "expected_output": (
                {
                    "data": "Package generated",
                    "path": "package_path2",
                    "edge_id": None,
                    "latest_set_version": ""
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": (None, None, "package_path3"),
            "expected_output": (
                {
                    "data": "Package generated",
                    "path": "package_path3",
                    "edge_id": None,
                    "latest_set_version": None
                },
                config_package.status.HTTP_200_OK
            )
        }, {
            "generate_package_returns": ("test", "best", "package_path3"),
            "expected_output": (
                {
                    "data": "Package generated",
                    "path": "package_path3",
                    "edge_id": "test",
                    "latest_set_version": "best"
                },
                config_package.status.HTTP_200_OK
            )
        }
        ]
        config_package.ConfigGenerator = MockConfigGeneratorRequestParser
        config_package.reqparse.RequestParser = MockConfigGeneratorRequestParser
        for scenario in test_scenarios:
            global generate_package_returns
            generate_package_returns = scenario["generate_package_returns"]
            expected_output = scenario["expected_output"]
            test_obj = config_package.ConfigPackageResource()
            self.assertEqual(test_obj.get(), expected_output)
