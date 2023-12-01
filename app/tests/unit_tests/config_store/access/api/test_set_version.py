import sys
import unittest

sys.path.append("src")

from src.config_store.access.api import set_version

class MockRequirements:
    set_version = None
    @staticmethod
    def get_all_latest_set_version(*args):
        return MockRequirements.set_version


class TestSetVersionResource(unittest.TestCase):
    def test_get(self):
        test_scenarios=[
            "",
            None,
            0,
            "Test1",
            "test2",
            "1.2.3"
        ]
        set_version.SetVersion = MockRequirements
        for scenarios in test_scenarios:
            MockRequirements.set_version = scenarios
            test_obj = set_version.SetVersionResource()
            if scenarios:
                self.assertEqual(test_obj.get(), (scenarios,
                                 set_version.status.HTTP_200_OK))
            else:
                self.assertEqual(test_obj.get(), (scenarios,
                                 set_version.status.HTTP_204_NO_CONTENT))
