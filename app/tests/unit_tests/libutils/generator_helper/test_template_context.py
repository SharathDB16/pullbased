import sys
import unittest

sys.path.append("src")

from src.libutils.generator_helper import template_context

class MockDPController():
    dpverse_details = {}

    def __init__(self, edge_id):
        pass

    def get_dp_verse_details(self):
        return MockDPController.dpverse_details


class MockIPAMController():
    ip_details = {}

    def __init__(self, edge_id):
        pass

    def get_all_ip(self):
        return MockIPAMController.ip_details


class MockExternalIP():
    external_ip_details = {}

    def __init__(self, edge_id):
        pass

    def get_external_ip_details(self):
        return MockExternalIP.external_ip_details


class MockConfig():
    def __init__(self):
        self.environment_type = ""


class TestBaseContext(unittest.TestCase):
    base_data = {"wan_interface_name": "lxcbr0",
                   "container1_ip": "5.5.5.5",
                   "container1_name": "dumb01",
                   "dns_server1": "103.195.71.118",
                   "dns_server2": "103.195.71.119",
                   "agent_version": "",
                   "cores": "",
                   "radius_server_name": "edge.sboxnw.com",
                   "lan_interface_name": "enp3s0",
                   "ap_interface_name": "enp3s0.21",
                   "cpe_interface_name": "enp2s0.30"}
    class_data = {}
    
    def setUp(self):
        template_context.DPController = MockDPController
        template_context.Controller = MockIPAMController
        self.test_scenarios = [
            {
                "dpverse_details": {"test_dp_details": "This is to check if dp details are updated"},
                "ip_details": {"test_ip_details": "This is to check if ip details are updated"},
                "environment_type": "staging",
                "edge_id": "125216",
                "expected_extra_data": {
                    "cls_env": "cls01.stg.sboxdc.com", "pds_env": "pds01.stg.sboxdc.com",
                    "sms_env": "sms01.stg.sboxdc.com", "apphost_env": "apphosting01.stg.sboxdc.com",
                    "cps_env": "cps01.stg.sboxdc.com", "env_type": "staging",
                    "host_list": ["kfk01.stg.sboxdc.com:9092", "kfk02.stg.sboxdc.com:9092",
                                  "kfk03.stg.sboxdc.com:9092"]
                }
            },
            {
                "dpverse_details": {"test_dp_details": "This is to check if dp details are updated"},
                "ip_details": {"test_ip_details": "This is to check if ip details are updated"},
                "environment_type": "other",
                "edge_id": "125216",
                "expected_extra_data": {
                    "cls_env": "cls02.sboxdc.com", "pds_env": "pds01.sboxdc.com",
                    "sms_env": "sms01.sboxdc.com", "apphost_env": "apphosting01.sboxdc.com",
                    "cps_env": "cps01.sboxdc.com", "env_type": "production",
                    "host_list": ["kfk04.sboxdc.com:9092", "kfk05.sboxdc.com:9092",
                                  "kfk06.sboxdc.com:9092"]
                }
            }
        ]
        self.use_external_ip = False
        self.test_class = template_context.Base
        return super().setUp()

    def test_get_context(self):
        for scenario in self.test_scenarios:
            exptected_data = {}
            MockDPController.dpverse_details = scenario["dpverse_details"]
            exptected_data.update(MockDPController.dpverse_details)

            if(self.use_external_ip):
                MockExternalIP.external_ip_details = scenario["external_ip_details"]
                exptected_data.update(MockExternalIP.external_ip_details)

            MockIPAMController.ip_details = scenario["ip_details"]
            exptected_data.update(MockIPAMController.ip_details)
            exptected_data.update(self.base_data)
            exptected_data.update(self.class_data)
            exptected_data.update(scenario["expected_extra_data"])

            template_context.config_obj.environment_type = scenario["environment_type"]

            context = self.test_class(scenario["edge_id"])
            get_context = getattr(context, "get_context", None)
            if get_context and hasattr(get_context, '__call__'):
                data = get_context()
            else:
                data = context.context
            
            self.assertEqual(data, exptected_data)


class TestStaticContext(TestBaseContext):
    class_data = {
        "edge_type": "static",
        "edge_sub_type": "default",
        "nagios_server_name": "statnag01.sboxdc.com"
    }
    def setUp(self):
        return_data = super().setUp()
        self.test_class = template_context.Static
        self.test_scenarios[0]["ip_details"].update({
                    "wan_first_ip": "192.168.2.5",
                    "wan_last_ip": "192.168.2.254"
                }
        )
        self.test_scenarios[0]["expected_extra_data"].update({
                    "wan_list": list(template_context.iter_iprange(str(template_context.IPAddress("192.168.2.5") + 2),
                                     "192.168.2.254"))
                }
        )
        self.test_scenarios[1]["ip_details"].update({
                    "wan_first_ip": "192.168.4.5",
                    "wan_last_ip": "192.168.4.254"
                }
        )
        self.test_scenarios[1]["expected_extra_data"].update({
                    "wan_list": list(template_context.iter_iprange(str(template_context.IPAddress("192.168.4.5") + 2),
                                     "192.168.4.254"))
                }
        )
        self.maxDiff = None
        self.test_class = template_context.Static
        return return_data


class TestMidContext(TestStaticContext):
    class_data = {
                   "edge_type": "mid",
                   "edge_sub_type": "default",
                   'nagios_server_name': 'statnag01.sboxdc.com'
                }

    def setUp(self):
        return_data = super().setUp()
        self.test_class = template_context.Mid
        return return_data


class TestMobileContext(TestStaticContext):
    class_data = { "edge_type": "mobile",
                   "edge_sub_type": "default",
                   "nagios_server_name": "mobnag01.sboxdc.com",
                   "dongle_interface_name": ""
                 }

    def setUp(self):
        return_data = super().setUp()
        self.test_class = template_context.Mobile
        return return_data

class TestKontronmetroContext(TestStaticContext):
    class_data = {
                   "edge_type": "mobile",
                   "ap_interface_name": "ap0",
                   "cpe_interface_name": "cpe0",
                   "edge_sub_type": "kontronmetro",
                   "dongle_interface_name": "dongle0",
                   "nagios_server_name": "mobnag01.sboxdc.com"
                   }

    def setUp(self):
        return_data = super().setUp()
        self.test_scenarios[0]["expected_extra_data"].update({
            "wan_list": list(template_context.iter_iprange(str(template_context.IPAddress("192.168.2.5") + 1),
                                                           "192.168.2.254"))
        }
        )
        self.test_scenarios[1]["expected_extra_data"].update({
            "wan_list": list(template_context.iter_iprange(str(template_context.IPAddress("192.168.4.5") + 1),
                                                           "192.168.4.254"))
        }
        )
        self.test_class = template_context.Kontronmetro
        return return_data


class TestC2cbusContext(TestBaseContext):
    class_data = {
                   "edge_type": "mobile",
                   "ap_interface_name": "ap0",
                   "cpe_interface_name": "cpe0",
                   "edge_sub_type": "c2cbus",
                   "dongle_interface_name": "dongle0",
                   "nagios_server_name": "mobnag01.sboxdc.com",
                   'wan_list': '',
                   'wan_first_ip':''
                  }

    def setUp(self):
        return_data = super().setUp()
        self.test_scenarios[0]["ip_details"].update({
            "wan_first_ip": "192.168.2.5",
            "wan_last_ip": "192.168.2.254"
        }
        )
        self.test_class = template_context.C2cbus
        return return_data


class TestNucContext(TestC2cbusContext):
    class_data = {
                   "wan_first_ip": "",
                   "edge_type": "static",
                   "edge_sub_type": "nuc",
                   "nagios_server_name": "statnag01.sboxdc.com"
                   }

    def setUp(self):
        return_data = super().setUp()
        self.test_class = template_context.Nuc
        return return_data


class TestCtstaticContext(TestStaticContext):
    class_data = {
                   "edge_type": "static",
                   "edge_sub_type": "ct_static",
                   "nagios_server_name": "statnag01.sboxdc.com",
                   "lan_first_ip":'',
                   "public_dns_ip":'8.8.8.8'
                   }

    def setUp(self):
        return_data = super().setUp()
        template_context.ExternalIP = MockExternalIP
        self.test_scenarios[0].update({
            "external_ip_details": {"test_external_ip_details": "This is to check if external ip details are updated"},
        }
        )
        self.test_scenarios[1].update({
            "external_ip_details": {"test_external_ip_details": "This is to check if external ip details are updated"},
        }
        )
        self.use_external_ip = True
        self.test_class = template_context.Ctstatic
        
        return return_data


class TestRailtelpilotecContext(TestKontronmetroContext):
    class_data = {
        "edge_type": "mobile",
        "ap_interface_name": "enp2s0",
        "cpe_interface_name": "cpe0",
        "edge_sub_type": "railtel_pilot_ec",
        "dongle_interface_name": "dongle0",
        "nagios_server_name": "mobnag01.sboxdc.com"
    }

    def setUp(self):
        return_data = super().setUp()
        self.test_scenarios[0]["expected_extra_data"].update({
            "wan_ap_first_ip": template_context.IPAddress("192.168.2.6"),
            "wan_ap_last_ip": template_context.IPAddress("192.168.2.254")
        }
        )
        self.test_scenarios[1]["expected_extra_data"].update({
            "wan_ap_first_ip": template_context.IPAddress("192.168.4.6"),
            "wan_ap_last_ip": template_context.IPAddress("192.168.4.254")
        }
        )
        self.test_class = template_context.Railtelpilotec
        self.maxDiff = None
        return return_data
