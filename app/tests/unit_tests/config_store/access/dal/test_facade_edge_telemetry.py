import sys
import unittest

sys.path.append("src")

from src.config_store.access.dal import edge_telemetry

# ToDo imporove testability and add test cases

class MockListItem:
    def __init__(self, edge_id):
        self.edge_id = edge_id
    
    @staticmethod
    def get_mock_item_list(data):
        return [MockListItem(value) for value in data]

class MockRequirements:
    edge_id = None
    added_record = None
    query_record = None
    distinct_returns = None
    throw_exception_on_add = ""
    @staticmethod
    def edge_telemetry_info_mock(**nargs):
        return nargs
    
    @staticmethod
    def session_scope():
        return MockRequirements()
    
    def add(self, *uargs, **nargs):
        if MockRequirements.throw_exception_on_add:
            raise Exception(MockRequirements.throw_exception_on_add)
        MockRequirements.added_record = (uargs, nargs)
    
    def query(self, *uargs, **nargs):
        MockRequirements.query_record = (uargs, nargs)
        return self
    
    def distinct(self):
        return MockRequirements.distinct_returns
    
    def __enter__(self):
        return self

    def __exit__(self, *uargs, **nargs):
        pass



class TestFacadeEdgeTelemetry(unittest.TestCase):
    
    def test_add_telemetry_info(self):
        test_scenarios = [
            {
                "input": dict(code_id=None, edge_id=None, package_name=None, template_set_version=None,
                              report_status=None),
                "throw_exception_on_add": "",
                "expected_output": True,
                "added_record": dict(code_id=None, edge_id=None, package_name=None,
                                     template_set_version=None,
                                     report_status=str(None))
            },
            {
                "input": dict(code_id="code_id", edge_id="edge_id", package_name=None, template_set_version=None,
                              report_status=2324),
                "throw_exception_on_add": "",
                "expected_output": True,
                "added_record": dict(code_id="code_id", edge_id="edge_id", package_name=None,
                                     template_set_version=None,
                                     report_status=str(2324))
            },
            {
                "input": dict(code_id="code_id", edge_id="edge_id", package_name=None, template_set_version=None,
                              report_status=2324),
                "throw_exception_on_add": "This is an exception test",
                "expected_output": False,
                "added_record": ""
            }
        ]
        edge_telemetry.EdgeTelemetryInfo= MockRequirements.edge_telemetry_info_mock
        edge_telemetry.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenarios:
            input = scenario["input"]
            MockRequirements.added_record = (("",),{})
            MockRequirements.throw_exception_on_add = scenario["throw_exception_on_add"]
            expected_output = scenario["expected_output"]
            added_record = scenario["added_record"]
            self.assertEqual(edge_telemetry.FacadeEdgeTelemetry.add_telemetry_info(**input), expected_output)
            self.assertEqual(MockRequirements.added_record, ((added_record,),{}))
            self.maxDiff = None
    
    def test_get_edge_telemetry_list(self):
        test_scenarios = [
            {
                "distinct_returns": MockListItem.get_mock_item_list([1, 2, 3, 4, 5]),
                "query_record": "125216",
                "expected_output": {
                    "data": {
                        "edge_id_list": [1, 2, 3, 4, 5]
                    }
                }
            },
            {
                "distinct_returns": MockListItem.get_mock_item_list([None, "test", 3, "trial", 5]),
                "query_record": "225345",
                "expected_output": {
                    "data": {
                        "edge_id_list": [None, "test", 3, "trial", 5]
                    }
                }
            }
        ]
        edge_telemetry.SqlAlchemyConnection = MockRequirements
        edge_telemetry.EdgeTelemetryInfo = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.distinct_returns = scenario["distinct_returns"]
            MockRequirements.query_record = None
            query_record = scenario["query_record"]
            MockRequirements.edge_id = query_record
            expected_output = scenario["expected_output"]
            self.assertEqual(edge_telemetry.FacadeEdgeTelemetry.get_edge_telemetry_list(), expected_output)
            self.assertEqual(MockRequirements.query_record, ((query_record,),{}))

