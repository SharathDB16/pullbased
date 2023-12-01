import sys
import unittest

sys.path.append("src")

from src.config_store.access.api import template_set


class MockRequirements:
    get_all_templates_returns = (None, None)
    @staticmethod
    def get_all_templates(edge_id, set_version):
        return MockRequirements.get_all_templates_returns

    def __init__(self):
        self.args_dict = dict()

    def add_argument(self, argument, *args, **named_args):
        self.args_dict[argument] = named_args

    def parse_args(self):
        return_dict = dict()
        for key in self.args_dict:
            return_dict[key] = ""
        return return_dict

class TestTemplateSet(unittest.TestCase):

    def test_init(self):
        template_set.reqparse.RequestParser = MockRequirements
        test_obj = template_set.TemplateSetResource()
        expected_dict = {
            'edge_id': dict(type=template_set.validate_edge_id, required=True,
                            help='Invalid edge id',
                            nullable=False),
            'set_version': dict(type=float, required=False,
                                help='Invalid set version',
                                nullable=False)
        }
        self.assertEqual(test_obj.reqparse.args_dict, expected_dict)

    def test_get(self):
        test_scenarios = [
            {
                "get_all_templates_returns": (
                    "This is a result test",
                    "This is a version test"
                ),
                "expected_output": (
                    {
                        "data": "This is a result test",
                        "latest_set_version": "This is a version test"
                    },
                    template_set.status.HTTP_200_OK
                )
            },
            {
                "get_all_templates_returns": (
                    "This is a result test 2",
                    "This is a version test 2"
                ),
                "expected_output": (
                    {
                        "data": "This is a result test 2",
                        "latest_set_version": "This is a version test 2"
                    },
                    template_set.status.HTTP_200_OK
                )
            }
        ]
        template_set.TemplateSet = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.get_all_templates_returns = scenario["get_all_templates_returns"]
            expected_output = scenario["expected_output"]
            test_obj = template_set.TemplateSetResource()
            self.assertEqual(test_obj.get(), expected_output)
