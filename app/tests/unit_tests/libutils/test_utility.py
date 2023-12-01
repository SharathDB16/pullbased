import os
import string
import random
import sys
import tempfile
import unittest

sys.path.append("src")

from src.libutils import utility
from tests import utilities

def get_random_string():
    letters = [random.choice(string.printable) for i in range(20)]
    return "".join(letters)

class test_utility(unittest.TestCase):
    def test_non_empty_string(self):
        test_scenarios = {
            "standard":[
                get_random_string(),
                get_random_string(),
                get_random_string()
            ],
            "exception": [
                "", 
                None,
                0,
                []
            ]
        }
        for scenario_string in test_scenarios["standard"]:
            self.assertEqual(utility.non_empty_string(scenario_string), scenario_string)
        for scenario_string in test_scenarios["exception"]:
            with self.assertRaises(ValueError):
                utility.non_empty_string(scenario_string) 

    def test_validate_edge_id(self):
        test_scenarios = {
            "standard":[
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower(),
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower(),
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower(),
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower(),
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower(),
                "".join([random.choice(string.hexdigits) for i in range(6)]).lower()
            ],
            "exception":[
                dict(edge_id="", error=ValueError),
                dict(edge_id="123", error=ValueError),
                dict(edge_id="1234567", error=ValueError),
                dict(edge_id="dfgera", error=ValueError),
                dict(edge_id=None, error=TypeError),
            ]
        }
        for scenario_string in test_scenarios["standard"]:
            self.assertEqual(utility.validate_edge_id(scenario_string), scenario_string)
        for scenario in test_scenarios["exception"]:
            with self.assertRaises(scenario["error"]):
                utility.validate_edge_id(scenario["edge_id"])

    def test_edge_type_subtype(self):
        test_scenarios = {
            "standard":[
                {
                    "server_configs": {
                        "edge-details":{
                            "template" : "accurate_responses/edge-details1.json",
                            "jinja2" : {
                                "edge_type":"static",
                                "edge_sub_type":"default",
                                "switch_type" : 1
                            },
                            "return_code" : 200
                        }
                    },
                    "edge_id":"125216",
                    "output": ("static", "default", 1)
                },
                {
                    "server_configs": {
                        "edge-details":{
                            "template" : "accurate_responses/edge-details1.json",
                            "jinja2" : {
                                "edge_type":"mid",
                                "edge_sub_type":"default",
                                "switch_type":2
                            },
                            "return_code" : 200
                        }
                    },
                    "edge_id":"125216",
                    "output": ("mid", "default", 2)
                }
            ],
            "exception":[
                {
                    "server_configs": {
                        "edge-details":{
                            "template" : "accurate_responses/edge-details2.json",
                            "return_code" : 404
                        }
                    },
                    "edge_id":"125216",
                    "exception" : utility.HTTPExceptionFactory
                },
                {
                    "server_configs": {
                        "edge-details":{
                            "template" : "response404.json",
                            "return_code" : 404
                        }
                    },
                    "edge_id":"423216",
                    "exception" : utility.HTTPExceptionFactory
                },
                {
                    "server_configs": {
                        "edge-details":None
                    },
                    "edge_id":"234561",
                    "exception" : utility.HTTPExceptionFactory
                }
            ]
        }
        for scenario in test_scenarios["standard"]:
            server_configs = scenario["server_configs"]
            utilities.update_ipam_db_server_configs(server_configs)
            self.assertEqual(utility.edge_type_subtype(scenario["edge_id"]), scenario["output"])
        
        for scenario in test_scenarios["exception"]:
            server_configs = scenario["server_configs"]
            utilities.update_ipam_db_server_configs(server_configs)
            with self.assertRaises(scenario["exception"]):
                utility.edge_type_subtype(scenario["edge_id"])


    def test_version_incrementer(self):
        test_scenarios =[
            (None, 0.01),
            (0.34, 0.35),
            (2.99, 3)
        ]
        for scenario in test_scenarios:
            self.assertEqual(utility.version_incrementer(scenario[0]), scenario[1])

    def test_create_path_if_not_exists(self):
        temp_dir = tempfile.TemporaryDirectory("unit_test")
        test_scenarios = {
            "standard" :[
            (None, f"{temp_dir.name}/scenario1/test1.txt", True),
            (None, f"{temp_dir.name}/scenario2/sub1/sub2/test2.txt", True),
            (f"{temp_dir.name}/scenario3", f"{temp_dir.name}/scenario3/sub1/sub2/test3.txt", False),
            (None, "", False)
            ],
            "exception":[
                (None, TypeError)
            ]
        }
        #Run standard test scenarios
        for scenario in test_scenarios["standard"]:
            temp_file = scenario[0]
            if temp_file is not None:
                with open(temp_file, "w") as file_pointer:
                    file_pointer.write("This is a unit test")
            path = scenario[1]
            folder_created = scenario[2]
            utility.create_path_if_not_exists(path)
            folder_exists = False
            if path is not None:
                folder_exists = os.path.exists(os.path.dirname(path))
            self.assertEqual(folder_exists, folder_created, path)
            
        #Run test scenarios which raise an exception
        for scenario in test_scenarios["exception"]:
            path = scenario[0]
            raises = scenario[1]
            with self.assertRaises(raises):
                utility.create_path_if_not_exists(path)
        temp_dir.cleanup()

    def test_get_context(self):
        test_scenarios = [
            (get_random_string(), get_random_string(), None),
            ("static", get_random_string(), utility.Static),
            ("mid", get_random_string(), utility.Mid),
            ("mobile", get_random_string(), utility.Mobile),
            ("static", "default", utility.Static),
            ("mid", "default", utility.Mid),
            ("mobile", "default", utility.Mobile),
            ("static", "nuc", utility.Nuc),
            ("mid", "default", utility.Mid),
            ("mobile", "default", utility.Mobile)
        ]
        for entry in test_scenarios:
            edge_type = entry[0]
            edge_sub_type = entry[1]
            context_class = entry[2]
            self.assertIs(utility.get_context(edge_type, edge_sub_type), context_class)
