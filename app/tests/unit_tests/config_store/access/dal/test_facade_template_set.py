import sys
import unittest

sys.path.append("src")

from src.config_store.access.dal import template_set

# ToDo test for changing input
# ToDo modify for testability and add test cases

class MockListItem:
    def __init__(self, edge_id):
        self.edge_id = edge_id

    @staticmethod
    def get_mock_item_list(data):
        return [MockListItem(value) for value in data]

class MockTemplateData:
    data_dict = dict()
    def __getattribute__(self, name):
        return MockTemplateData.data_dict.get(name, None)

class MockRequirements:
    query_record = None
    order_by_record = None
    all_record = None
    filter_record = None
    first_returns = None

    all_returns = None
    throw_exception_on_add = ""

    @staticmethod
    def edge_telemetry_info_mock(**nargs):
        return nargs

    @staticmethod
    def session_scope():
        return MockRequirements()

    def query(self, *uargs, **nargs):
        MockRequirements.query_record = (uargs, nargs)
        return self

    def distinct(self, *uargs, **nargs):
        MockRequirements.distinct_record = (uargs, nargs)
        return self

    def order_by(self, *uargs, **nargs):
        MockRequirements.order_by_record = (uargs, nargs)
        return self

    def filter(self, *uargs, **nargs):
        MockRequirements.filter_record = (uargs, nargs)
        return self
    
    def first(self):
        return MockRequirements.first_returns

    def all(self, *uargs, **nargs):
        MockRequirements.all_record = (uargs, nargs)
        return MockRequirements.all_returns

    def __enter__(self):
        return self

    def __exit__(self, *uargs, **nargs):
        pass


class TestFacedTemplateSet(unittest.TestCase):
    def test_get_master_package_id(self):
        test_scenarios = [
            {
                "all_returns": [
                    ("id1", ),
                    ("id2", )
                ],
                "expected_output": [
                    "id1",
                    "id2"
                ]
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.all_returns = scenario["all_returns"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_master_package_id(None), expected_output)

    def test_get_switch_package_id(self):
        test_scenarios = [
            {
                "all_returns": [
                    ("id1", ),
                    ("id2", )
                ],
                "expected_output": [
                    "id1",
                    "id2"
                ]
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.all_returns = scenario["all_returns"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_switch_package_id(None, None), expected_output)

    def test_get_template_details(self):
        test_scenarios = [
            {
                "first_returns": MockTemplateData(),
                "data_dict": {},
                "template_id": "temp_id",
                "expected_output": {
                    "name": None,
                    "description": None,
                    "path": None,
                    "owner": None,
                    "group": None,
                    "permissions": None,
                    "template_id": "temp_id"
                }
            },
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "name": "name1",
                    "description": "description1",
                    "path": "path1",
                    "owner": "owner1",
                    "group": "group1",
                    "permissions": "permissions1"
                },
                "template_id": "temp_id",
                "expected_output": {
                    "name": "name1",
                    "description": "description1",
                    "path": "path1",
                    "owner": "owner1",
                    "group": "group1",
                    "permissions": "permissions1",
                    "template_id": "temp_id"
                }
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.first_returns = scenario["first_returns"]
            MockTemplateData.data_dict = scenario["data_dict"]
            template_id = scenario["template_id"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_template_details(template_id), expected_output)

    def test_get_template_version_details(self):
        test_scenarios = [
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "template_file": b"this is a template file test",
                    "comment": "This is a comment",
                    "version_no": 1.45
                },
                "expected_output": {
                    "template_file": "this is a template file test",
                    "comment": "This is a comment",
                    "version_no": "1.45"
                }
            },
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "template_file": b"this is a template file test 2",
                    "comment": "This is a also comment",
                    "version_no": 1.67
                },
                "expected_output": {
                    "template_file": "this is a template file test 2",
                    "comment": "This is a also comment",
                    "version_no": "1.67"
                }
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.first_returns = scenario["first_returns"]
            MockTemplateData.data_dict = scenario["data_dict"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_template_version_details(None, None), expected_output)

    def test_get_master_details(self):
        test_scenarios = [
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                },
                "expected_output": {
                    "name": None,
                    "description": None,
                    "status": None,
                    "execution_sequence": None
                }
            },
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "name": "name1",
                    "description": "description1",
                    "status": "status1",
                    "execution_sequence": "execution_sequence1"
                },
                "expected_output": {
                    "name": "name1",
                    "description": "description1",
                    "status": "status1",
                    "execution_sequence": "execution_sequence1"
                }
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.first_returns = scenario["first_returns"]
            MockTemplateData.data_dict = scenario["data_dict"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_master_details(None), expected_output)

    def test_get_master_files(self):
        test_scenarios = [
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "uninstall_file": b" uninstall file 1",
                    "pre_script_file": b"pre script file 1",
                    "post_script_file": b"post script file 1"
                },
                "expected_output": {
                    "uninstall_file": " uninstall file 1",
                    "pre_script_file": "pre script file 1",
                    "post_script_file": "post script file 1"
                }
            },
            {
                "first_returns": MockTemplateData(),
                "data_dict": {
                    "uninstall_file": b" uninstall file 2",
                    "pre_script_file": b"pre script file 2",
                    "post_script_file": b"post script file 2"
                },
                "expected_output": {
                    "uninstall_file": " uninstall file 2",
                    "pre_script_file": "pre script file 2",
                    "post_script_file": "post script file 2"
                }
            }
        ]
        template_set.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.first_returns = scenario["first_returns"]
            MockTemplateData.data_dict = scenario["data_dict"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                template_set.FacadeTemplateSet.get_master_files(None), expected_output)
