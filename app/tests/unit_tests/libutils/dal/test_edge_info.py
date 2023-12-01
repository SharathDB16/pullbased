import sys
import unittest

sys.path.append("src")

from src.libutils.dal import edge_info
from tests import utilities


class TestEdgeInfo(unittest.TestCase):

    def setUp(self):
        utilities.update_db("tests/db_files/edge_info_test.sql")

    def test_get_edge_by_type_subtype(self):
        test_scenarios = [
            ("static", "default", {
                "id": 1,
                "edge_type": "static",
                "edge_sub_type": "default",
                "pre_gen_script_file": "file1 static default",
                "post_gen_script_file": "file2 static default"
            }),
            ("mid", "default", {
                "id": 2,
                "edge_type": "mid",
                "edge_sub_type": "default",
                "pre_gen_script_file": "file1 mid default",
                "post_gen_script_file": "file2 mid default"
            }),
            ("mobile", "kontronmetro", {
                "id": 3,
                "edge_type": "mobile",
                "edge_sub_type": "kontronmetro",
                "pre_gen_script_file": "file1 mobile kontronmetro",
                "post_gen_script_file": "file2 mobile kontronmetro"
            }),
            ("unknown", "unknown", None),
            (None, None, None)
        ]
        for index, scenario in enumerate(test_scenarios):
            edge_type = scenario[0]
            edge_sub_type = scenario[1]
            result = scenario[2]
            self.assertEqual(edge_info.FacadeEdgeInfo.get_edge_by_type_subtype(edge_type, edge_sub_type), result, f"Error in scenario {index}")
