import sys
import unittest

sys.path.append("src")

from src.config_store.access.bl import edge_telemetry

class MockRequirements:
    add_telemetry_info_returns = None
    @staticmethod
    def add_telemetry_info(*uargs, **nargs):
        return MockRequirements.add_telemetry_info_returns


class TestEdgePackageTelemetry(unittest.TestCase):
    def test_set_package_download_telemetry(self):
        test_scenarios = [
            {
                "add_telemetry_info_returns": None,
                "input": (
                    {
                        "edge_id": None,
                        "package_name": None,
                        "template_set_version": None
                    },
                    "success",
                    None
                ),
                "expected_output": (
                    None,
                    "Package Download Successful"
                )
            },
            {
                "add_telemetry_info_returns": "test",
                "input": (
                    {
                        "edge_id": None,
                        "package_name": None,
                        "template_set_version": None
                    },
                    "other",
                    None
                ),
                "expected_output": (
                    "test",
                    "Package Download Failed"
                )
            }
        ]
        edge_telemetry.FacadeEdgeTelemetry = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.add_telemetry_info_returns = scenario["add_telemetry_info_returns"]
            input = scenario["input"]
            expected_output = scenario["expected_output"]
            self.assertEqual(edge_telemetry.EdgePackageTelemetry.set_package_download_telemetry(
                *input), expected_output)

    def test_set_package_consumption_telemetry(self):
        test_scenarios = [
            {
                "add_telemetry_info_returns": None,
                "input": (
                    {
                        "edge_id": None,
                        "package_name": None,
                        "template_set_version": None
                    },
                    "success",
                    None
                ),
                "expected_output": (
                    None,
                    "Package Consumption Successful"
                )
            },
            {
                "add_telemetry_info_returns": "test",
                "input": (
                    {
                        "edge_id": None,
                        "package_name": None,
                        "template_set_version": None
                    },
                    "other",
                    None
                ),
                "expected_output": (
                    "test",
                    "Package Consumption Failed"
                )
            }
        ]
        edge_telemetry.FacadeEdgeTelemetry = MockRequirements
        for scenario in test_scenarios:
            MockRequirements.add_telemetry_info_returns = scenario["add_telemetry_info_returns"]
            input = scenario["input"]
            expected_output = scenario["expected_output"]
            self.assertEqual(edge_telemetry.EdgePackageTelemetry.set_package_consumption_telemetry(
                *input), expected_output)
