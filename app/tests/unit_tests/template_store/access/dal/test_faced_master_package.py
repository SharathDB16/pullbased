import sys
import unittest
from unittest import mock
from unittest.mock import patch, Mock

sys.path.append("src")

from src.template_store.access.dal import master_package


def get_mocked_list(data):
    mocked_list = []
    for mockable in data:
        mocked = Mock()
        mocked.configure_mock(**mockable)
        mocked_list.append(mocked)
    return mocked_list

class TestFacedMasterPackage(unittest.TestCase):
    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_get_master_package_list(self, sql_alchemy_mock):
        test_scenarios = [
            {
                "master_template_list": [dict(id="id1", name="name1", description="description1", status="status1"), dict(id="id2", name="name2", description="description2", status="status2")],
                "expected_data":{
                    "data": [
                        {
                            "id":"id1",
                            "name":"name1",
                            "description":"description1",
                            "status":"status1"
                        },
                        {
                            "id": "id2",
                            "name": "name2",
                            "description": "description2",
                            "status": "status2"
                        }
                    ]
                }
            },
            {
                "master_template_list": [],
                "expected_data":{
                    "data": []
                }
            }
        ]
        for scenario in test_scenarios:
            mocked_list = get_mocked_list(scenario["master_template_list"])
            sql_alchemy_mock.all = Mock(return_value=mocked_list )
            sql_alchemy_mock.query.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            returned_data = master_package.FacadeMasterPackage.get_master_package_list()
            expected_data = scenario["expected_data"]
            self.assertEqual(returned_data, expected_data)
            sql_alchemy_mock.session_scope.assert_called()
            sql_alchemy_mock.query.assert_called_with(master_package.MasterPackage)
            sql_alchemy_mock.all.assert_called()

    @patch("src.template_store.access.dal.master_package.MasterPackage")
    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_add_master_package(self, sql_alchemy_mock, master_package_mock):
        test_scenarios = [
            dict(name=None, description=None, path=None, user=None, group=None, permission=None,
                 uninstall_file=None, pre_script_file=None, post_script_file=None),
            dict(name="name1", description="description1", path="path1", user="user1", group="group1", permission="permissions1",
                 uninstall_file="uninstall_file1", pre_script_file="pre_script_file1", post_script_file="post_script_file1")
        ]
        for scenario in test_scenarios:
            master_package_mock.side_effect = [master_package_mock]
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            self.assertTrue(
                master_package.FacadeMasterPackage.add_master_package(**scenario))
            master_package_mock.assert_called_with(**scenario)
            sql_alchemy_mock.session_scope.assert_called()
            sql_alchemy_mock.add.assert_called_with(master_package_mock)

    @patch("src.template_store.access.dal.master_package.EdgePackage")
    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_assign_package_to_edge(self, sql_alchemy_mock, edge_package_mock):
        test_scenarios = [
            {
                "input": dict(master_package_id=None, edge_type=None, edge_sub_type=None),
                "firsts": [["edge_id_1"], None],
                "expected": (True, False)
            },
            {
                "input": dict(master_package_id="master_package_id1", edge_type="edge_type1", edge_sub_type="edge_sub_type1"),
                "firsts": [["edge_id_3"], "Not None"],
                "expected": (False, True)
            },
            {
                "input": dict(master_package_id="master_package_id1", edge_type="edge_type1", edge_sub_type="edge_sub_type1"),
                "firsts": [None, "Not None"],
                "expected": (False, False)
            }
        ]
        for scenario in test_scenarios:
            edge_package_mock.side_effect = [edge_package_mock]
            edge_package_mock.id = edge_package_mock
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.filter.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.query.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.first.side_effect = scenario["firsts"]

            expected = scenario["expected"]
            returned = master_package.FacadeMasterPackage.assign_package_to_edge(
                **scenario["input"])
            self.assertEqual(expected, returned)
            sql_alchemy_mock.query.assert_called_with(
                edge_package_mock.id)

    @patch("src.template_store.access.dal.master_package.EdgePackage")
    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_delete_package_from_edge(self, sql_alchemy_mock, edge_package_mock):
        test_scenarios = [
            {
                "input": dict(master_package_id=None, edge_type=None, edge_sub_type=None),
                "firsts": [["edge_id_1"], None],
                "expected": (False, True)
            },
            {
                "input": dict(master_package_id="master_package_id1", edge_type="edge_type1", edge_sub_type="edge_sub_type1"),
                "firsts": [["edge_id_3"], "Not None"],
                "expected": (True, False)
            },
            {
                "input": dict(master_package_id="master_package_id1", edge_type="edge_type1", edge_sub_type="edge_sub_type1"),
                "firsts": [None, "Not None"],
                "expected": (False, False)
            }
        ]
        for scenario in test_scenarios:
            edge_package_mock.side_effect = [edge_package_mock]
            edge_package_mock.id = edge_package_mock
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.filter.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.query.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.first.side_effect = scenario["firsts"]

            expected = scenario["expected"]
            returned = master_package.FacadeMasterPackage.delete_package_from_edge(
                **scenario["input"])
            self.assertEqual(expected, returned)
            sql_alchemy_mock.query.assert_called_with(
                edge_package_mock.id)

    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_update_master_package(self, sql_alchemy_mock):
        test_scenarios = [
            {
                "input": dict(args="args", master_id="master_id"),
                "update_returns": ["This is a test"],
                "expected":"This is a test"
            },
            {
                "input": dict(args="args", master_id="master_id"),
                "update_returns": Exception,
                "expected":False
            }
        ]
        for scenario in test_scenarios:
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.filter.side_effect = [
                sql_alchemy_mock]
            sql_alchemy_mock.query.side_effect = [
                sql_alchemy_mock]
            sql_alchemy_mock.update.side_effect = scenario["update_returns"]

            expected = scenario["expected"]
            input = scenario["input"]
            returned = master_package.FacadeMasterPackage.update_master_package(
                **input)
            self.assertEqual(expected, returned)
            sql_alchemy_mock.update.assert_called_with(input.get("args", None))

    @patch("src.template_store.access.dal.master_package.FacadeTemplatePreview")
    @patch("src.template_store.access.dal.master_package.SqlAlchemyConnection")
    def test_delete_master_package(self, sql_alchemy_mock, preview_mock):
        test_scenarios = [
            {
                "input": dict(master_id=None),
                "firsts": [None, ["template_file1"]],
                "template_version":None,
                "expected": False
            },
            {
                "input": dict(master_id="master_test"),
                "firsts": [["edge_id_1"], ["template_file1"]],
                "template_version":dict(config_template_id="edge_id_1", comment="Uninstall", template_file="template_file1"),
                "expected": True
            }
        ]
        for scenario in test_scenarios:
            sql_alchemy_mock.__enter__.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.session_scope.side_effect = [sql_alchemy_mock]
            sql_alchemy_mock.filter.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.order_by.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.query.side_effect = [
                sql_alchemy_mock, sql_alchemy_mock, sql_alchemy_mock]
            sql_alchemy_mock.first.side_effect = scenario["firsts"]

            expected = scenario["expected"]
            returned = master_package.FacadeMasterPackage.delete_master_package(
                **scenario["input"])
            self.assertEqual(expected, returned)
            if scenario["template_version"]:
                preview_mock.add_template_version.assert_called_with(
                    **scenario["template_version"])
            sql_alchemy_mock.update.assert_called_with({"status": 0})
