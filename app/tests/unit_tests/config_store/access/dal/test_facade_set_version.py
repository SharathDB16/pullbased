import sys
import unittest

sys.path.append("src")

from src.config_store.access.dal import set_version


# ToDo: Modify the code to be better testable

class MockRequirements:
    query_record = None
    select_from_record = None
    join_record = None
    add_column_record = None
    group_by_record = None
    limit_record = None

    group_by_returns = None
    limit_returns = None
    one_returns = None
    order_by_record = None

    def __enter__(self):
        return self

    def __exit__(self, *uargs, **nargs):
        pass

    def query(self, *uargs, **nargs):
        MockRequirements.query_record = (uargs, nargs)
        return self

    def select_from(self, *uargs, **nargs):
        MockRequirements.select_from_record = (uargs, nargs)
        return self

    def join(self, *uargs, **nargs):
        MockRequirements.join_record = (uargs, nargs)
        return self

    def filter(self, *uargs, **nargs):
        MockRequirements.filter_record = (uargs, nargs)
        return self

    def order_by(self, *uargs, **nargs):
        MockRequirements.order_by_record = (uargs, nargs)
        return self

    def add_columns(self, *uargs, **nargs):
        MockRequirements.add_column_record = (uargs, nargs)
        return self

    def group_by(self, *uargs, **nargs):
        MockRequirements.group_by_record = (uargs, nargs)
        return MockRequirements.group_by_returns

    def limit(self, *uargs, **nargs):
        MockRequirements.limit_record = (uargs, nargs)
        return MockRequirements.limit_returns

    def one(self):
        return MockRequirements.one_returns

    @staticmethod
    def session_scope():
        return MockRequirements()

class TestFacadeSetVersion(unittest.TestCase):
    def test_get_all_latest_set_version(self):
        test_scenario = [
            {
                "group_by_returns": [
                ],
                "limit_returns":{},
                "one_returns": [],
                "expected_output":[]
            },
            {
                "group_by_returns": [
                    [
                        "test",
                        "trial",
                        "this,is,a,test"
                    ]
                ],
                "limit_returns":[],
                "one_returns": [],
                "expected_output":[]
            },
            {
                "group_by_returns": [
                    [
                        "test",
                        "trial",
                        "this,is,a,test"
                    ]
                ],
                "limit_returns":[None],
                "one_returns": [
                    "test"
                ],
                "expected_output":[]
            },
            {
                "group_by_returns": [
                    [
                        "test",
                        "trial",
                        "this,is,a,test"
                    ]
                ],
                "limit_returns":[
                    [
                        "test1",
                        "test2"
                    ]
                ],
                "one_returns": [
                    "test"
                ],
                "expected_output":[{"edgeType": "test", "edgeSubType": "trial",
                                   "templateSetVersion": str("test1"), "createdDateTime": str("test2")}]
            },
            {
                "group_by_returns": [
                    [
                        "test",
                        "trial",
                        "this,is,a,test"
                    ],
                    [
                        "test2",
                        "trial2",
                        "this,is,a,test"
                    ]
                ],
                "limit_returns":[
                    [
                        "test3",
                        "test4"
                    ]
                ],
                "one_returns": [
                    "test"
                ],
                "expected_output":[{"edgeType": "test", "edgeSubType": "trial",
                                   "templateSetVersion": str("test3"), "createdDateTime": str("test4")},
                                   {"edgeType": "test2", "edgeSubType": "trial2",
                                   "templateSetVersion": str("test3"), "createdDateTime": str("test4")}]
            }
        ]
        set_version.SqlAlchemyConnection = MockRequirements
        for scenario in test_scenario:
            MockRequirements.group_by_returns = scenario["group_by_returns"]
            MockRequirements.limit_returns = scenario["limit_returns"]
            MockRequirements.one_returns = scenario["one_returns"]
            expected_output = scenario["expected_output"]
            self.assertEqual(
                set_version.FacadeSetVersion.get_all_latest_set_version(None), expected_output)
