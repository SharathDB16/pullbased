import json
import sys
import unittest

sys.path.append("src")

from src.config_store.access.api import edge_telemetry

class MockRequirements:
    environ = dict()
    data = b"{}"
    set_package_download_telemetry_returns = (True, True)
    set_package_consumption_telemetry_returns = (True, True)

    static_function_return = None
    
    def __init__(self):
        self.args_dict = dict()
    
    def add_argument(self, argument, *args, **named_args):
        self.args_dict[argument] = named_args
    
    def parse_args(self):
        return_dict = dict()
        for key in self.args_dict:
            return_dict[key]=""
        return return_dict

    @staticmethod
    def set_package_download_telemetry(*args, **named_args):
        return MockRequirements.set_package_download_telemetry_returns
    
    @staticmethod
    def set_package_consumption_telemetry(*args, **named_args):
        return MockRequirements.set_package_consumption_telemetry_returns

    @staticmethod
    def get_edge_telemetry_list():
        return MockRequirements.static_function_return

    @staticmethod
    def get_edge_telemetry(edge_id):
        return MockRequirements.static_function_return

    @staticmethod
    def get_edge_telemetry_info_list(page_num):
        return MockRequirements.static_function_return

    @staticmethod
    def get_edge_telemetry_info(edge_id):
        return MockRequirements.static_function_return

class TestEdgePackageDownloadTelemetry(unittest.TestCase):
    def test_init(self):
        edge_telemetry.reqparse.RequestParser = MockRequirements
        test_obj = edge_telemetry.EdgePackageDownloadTelemetry()
        expected_dict = {
            'edge_id': dict(type=edge_telemetry.validate_edge_id, required=True,
                            help='Invalid edge id',
                            nullable=False),
            'package_name': dict(type=edge_telemetry.non_empty_string, required=True,
                                 help='Invalid package name',
                                 nullable=False),
            'template_set_version': dict(type=edge_telemetry.non_empty_string, required=True,
                                         help='Template set version not provided',
                                         nullable=False)
        }
        self.assertEqual(test_obj.reqparse.args_dict, expected_dict)

    def test_post(self):
        test_scenarios = [{
            "environ": {
                "HTTP_X_FORWARDED_FOR": "23.23.23.23"
            },
            "data": str.encode(json.dumps({})),
            "set_package_download_telemetry_returns": (
                False,
                "This is the true output"
            ),
            "expected_output": (
                {"message": "Something went wrong",
                    "description": "Something went wrong"},
                edge_telemetry.status.HTTP_400_BAD_REQUEST
            )
        }, {
            "environ": {
                "HTTP_X_FORWARDED_FOR": "23.23.23.23"
            },
            "data": str.encode(json.dumps({})),
            "set_package_download_telemetry_returns": (
                True,
                "Test true output"
            ),
            "expected_output": (
                {"message": "success",
                    "description": "Test true output"},
                edge_telemetry.status.HTTP_200_OK
            )
        }]
        edge_telemetry.request = MockRequirements
        edge_telemetry.reqparse.RequestParser = MockRequirements
        edge_telemetry.EdgePackageTelemetry = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.environ = scenario["environ"]
            MockRequirements.data = scenario["data"]
            MockRequirements.set_package_download_telemetry_returns = scenario[
                "set_package_download_telemetry_returns"]
            expected_output = scenario["expected_output"]
            test_obj = edge_telemetry.EdgePackageDownloadTelemetry()
            self.assertEqual(test_obj.post("test", "trial"), expected_output)


class TestEdgePackageConsumptionTelemetry(unittest.TestCase):
    def test_init(self):
        edge_telemetry.reqparse.RequestParser = MockRequirements
        test_obj = edge_telemetry.EdgePackageConsumptionTelemetry()
        expected_dict = {
            'edge_id': dict(type=edge_telemetry.validate_edge_id, required=True,
                            help='Invalid edge id',
                            nullable=False),
            'package_name': dict(type=edge_telemetry.non_empty_string, required=True,
                                 help='Invalid package name',
                                 nullable=False),
            'template_set_version': dict(type=edge_telemetry.non_empty_string, required=True,
                                         help='Template set version not provided',
                                         nullable=False)
        }
        self.assertEqual(test_obj.reqparse.args_dict, expected_dict)

    def test_post(self):
        test_scenarios = [{
            "environ": {
                "HTTP_X_FORWARDED_FOR": "23.23.23.23"
            },
            "data": str.encode(json.dumps({})),
            "set_package_consumption_telemetry_returns": (
                False,
                "This is the true output"
            ),
            "expected_output": (
                {"message": "Something went wrong",
                    "description": "Something went wrong"},
                edge_telemetry.status.HTTP_400_BAD_REQUEST
            )
        }, {
            "environ": {
                "HTTP_X_FORWARDED_FOR": "23.23.23.23"
            },
            "data": str.encode(json.dumps({})),
            "set_package_consumption_telemetry_returns": (
                True,
                "Test true output"
            ),
            "expected_output": (
                {"message": "success",
                    "description": "Test true output"},
                edge_telemetry.status.HTTP_200_OK
            )
        }]
        edge_telemetry.request = MockRequirements
        edge_telemetry.reqparse.RequestParser = MockRequirements
        edge_telemetry.EdgePackageTelemetry = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.environ = scenario["environ"]
            MockRequirements.data = scenario["data"]
            MockRequirements.set_package_consumption_telemetry_returns = scenario[
                "set_package_consumption_telemetry_returns"]
            expected_output = scenario["expected_output"]
            test_obj = edge_telemetry.EdgePackageConsumptionTelemetry()
            self.assertEqual(test_obj.post("test", "trial"), expected_output)


class TestEdgeTelemetryReportList(unittest.TestCase):
    test_class = edge_telemetry.EdgeTelemetryReportList
    passed_data = []

    def test_get(self):
        test_scenarios = [
            "This is test string 1",
            "This is None",
            None,
            2324
        ]
        for scenario in test_scenarios:
            MockRequirements.static_function_return = scenario
            test_obj = self.test_class()
            self.assertEqual(test_obj.get(*self.passed_data), scenario)


class TestEdgeTelemetryReport(TestEdgeTelemetryReportList):
    test_class = edge_telemetry.EdgeTelemetryReport
    passed_data = ["test"]
    pass


class TestEdgeTelemetryReportInfoList(TestEdgeTelemetryReportList):
    test_class = edge_telemetry.EdgeTelemetryReportInfoList
    passed_data = ["test"]
    pass


class TestEdgeTelemetryReportInfo(TestEdgeTelemetryReportList):
    test_class = edge_telemetry.EdgeTelemetryReportInfo
    passed_data = ["test"]
    pass

