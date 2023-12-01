import sys
import unittest

sys.path.append("src")

from src.libutils.generator_helper import ipam
from src.libutils import generator_helper
from tests import utilities


class TestIPAM(unittest.TestCase):
    test_scenarios = {
        "standard":
            [
                {
                    "edge_id": "125216",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "static",
                                "edge_sub_type": "default"
                            },
                            "return_code": 200
                        },
                        "search": {
                            "template": "accurate_responses/search_static_default.json",
                            "methods": ["POST"],
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "output": ("static", "default")
                        },
                        "set_subscriber_pool": {
                            "input": None,
                            "output": generator_helper.STATIC_MID_SUBSCRIBER_LAN_POOLS[1024]
                        },
                        "set_vpn_pool": {
                            "input": None,
                            "output": generator_helper.STATIC_MID_VPN_POOL
                        },
                        "set_ap_pool": {
                            "input": None,
                            "output": generator_helper.STATIC_MID_MGMT_POOLS
                        },
                        "set_cpe_pool" :{
                            "input": None,
                            "output" : None
                        },
                        "set_switch_pool": {
                            "input": None,
                            "output": ['172.29.0.0/18', '172.29.64.0/18', '172.29.128.0/17']
                        },
                        "get_subnet" : {
                            "input" : {
                                "subnetDto" : {
                                    "subnet" : "test subnet"
                                }
                            },
                            "output": "test subnet"
                        },
                        "get_first_ip": {
                            "input" : {
                                "subnetDto" : {
                                    "subnet" : "192.168.2.1"
                                }
                            },
                            "output": "192.168.2.2"
                        },
                        "get_second_ip": {
                            "input" : {
                                "subnetDto" : {
                                    "subnet" : "192.168.2.1"
                                }
                            },
                            "output": "192.168.2.3"
                        },
                        "get_last_ip": {
                            "input" : {
                                "subnetDto" : {
                                    "subnet" : "192.168.2.1",
                                    "mask" : 8
                                }
                            },
                            "output": "192.255.255.254"
                        },
                        "get_netmask": {
                            "input": {
                                "subnetDto": {
                                    "subnet": "192.168.2.1",
                                    "mask": 8
                                }
                            },
                            "output": ipam.IPAddress("255.0.0.0")
                        },
                        "get_bitmask": {
                            "input": {
                                "subnetDto": {
                                    "mask": 8
                                }
                            },
                            "output": '8'
                        },
                        "get_vpn_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.17.0.0",
                                        "mask": 17
                                    },
                                    "subnetDto": {
                                        "subnet": "This is the subnet"
                                    }
                                }
                            ],
                            "output": (True, "This is the subnet")
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.26.0.0",
                                        "mask": 15
                                    },
                                    "subnetDto": {
                                        "subnet": "192.168.4.5",
                                        "mask":12
                                    }
                                }
                            ],
                            "output": {
                                "wan_set": True, 
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('255.240.0.0'),
                                "wan_first_ip": "192.168.4.6",
                                "wan_ip_subnet_ap": "192.168.4.5",
                                "wan_ip_subnet_bitmask": "12",
                                "wan_last_ip": "192.175.255.254",
                                "wan_network_ip": "192.168.4.5",
                                "wan_second_ip_ap": "192.168.4.7",
                                "wan_start_ip": "192.168.4.8"
                            }
                        },
                        "get_lan_details" :{
                            "input" : {
                                "edge_ipam_details":[{
                                    "masterSubnetDto" :{
                                        "pool": "100.64.0.0",
                                        "mask": 10
                                    },
                                    "subnetDto": {
                                        "subnet": "192.168.4.5",
                                        "mask": 12
                                    }
                                }],
                                "subscriber_lan_pool": ["100.64.0.0/10"]
                            },
                            "output":{
                                "lan_set": True,
                                "lan_ip_subnet_netmask": ipam.IPAddress('255.240.0.0'),
                                "lan_first_ip": "192.168.4.6",
                                "lan_ip_subnet": "192.168.4.5",
                                "lan_ip_subnet_bitmask": "12",
                                "lan_last_ip": "192.175.255.254",
                                "lan_second_ip": "192.168.4.7",
                                "lan_wifi_nw": "192.168.4.5/12"
                            }
                        },
                        "get_pseudo_tp_lan_details" :{
                            "input" :{
                                "edge_details":{
                                    "edgeSubType": "parent_pseudo_tp",
                                    "pseudoTps" : [
                                    ]
                                },
                                "edge_ipam_details":[
                                    {
                                        "subnetDto": {
                                            "subnet": "192.168.4.5",
                                            "mask": 12
                                        }
                                    },
                                    {
                                        "subnetDto": {
                                            "subnet": "122.168.4.5",
                                            "mask": 22
                                        }
                                    }
                                ]
                            },
                            "output" : {
                                "interfaces":[
                                    {
                                        "address": "192.168.4.6",
                                        "netmask": ipam.IPAddress('255.240.0.0'),
                                        "gateway": ipam.IPAddress('255.240.0.0'),
                                        "dns-nameservers-1": "192.168.4.6",
                                        "dns-nameservers-2": "192.168.4.7",
                                    },
                                    {
                                        "num":"101",
                                        "address": "122.168.4.5",
                                        "netmask": ipam.IPAddress('255.255.252.0'),
                                    }
                                ],
                                "dnsmasq_conf": [
                                    {
                                        "subnet": "subnet0",
                                        "lan_first_ip": "192.168.4.6",
                                        "lan_second_ip": "192.168.4.7",
                                        "lan_last_ip": "192.175.255.254",
                                        "hour": "0h"
                                    },
                                    {
                                        "subnet": "subnet1",
                                        "lan_first_ip": "122.168.4.6",
                                        "lan_second_ip": "122.168.4.7",
                                        "lan_last_ip": "122.168.7.254",
                                        "hour": "1h"
                                    }
                                ],
                                "dnsmasq_apple_options_conf": [
                                    {
                                        "subnet_num": "subnet0",
                                        "first_ip": "192.168.4.6",
                                        "subnet_ip": "192.168.4.5/12"
                                    },
                                    {
                                        "subnet_num": "subnet1",
                                        "first_ip": "122.168.4.6",
                                        "subnet_ip": "122.168.4.5/22"
                                    }
                                ]
                            }
                        },
                        "get_cpe_details": {
                            "input": {
                                "cpe_pool": None,
                                "edge_ipam_details": []
                            },
                            "output":{}
                        },
                        "get_switch_details": {
                            "input": {
                                "switch_pool": ['172.29.0.0/18'],
                                "edge_ipam_details": []
                            },
                            "output":{
                                "switch_set": False
                            }
                        },
                        "get_all_ip":{
                            "input": None,
                            "output": {
                                "lan_first_ip": "100.64.2.1",
                                "lan_ip_subnet": "100.64.2.0",
                                "lan_ip_subnet_bitmask": "10",
                                "lan_ip_subnet_netmask": ipam.IPAddress("255.192.0.0"),
                                "lan_last_ip": "100.127.255.254",
                                "lan_second_ip": "100.64.2.2",
                                "lan_set": True,
                                "lan_wifi_nw": "100.64.2.0/10",
                                "switch_set": False,
                                "vpn_set": False,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress("255.192.0.0"),
                                "wan_first_ip": "100.64.2.1",
                                "wan_ip_subnet_ap": "100.64.2.0",
                                "wan_ip_subnet_bitmask": "10",
                                "wan_last_ip": "100.127.255.254",
                                "wan_network_ip": "100.64.2.0",
                                "wan_second_ip_ap": "100.64.2.2",
                                "wan_set": True,
                                "wan_start_ip": "100.64.2.3"
                            }
                        },
                        "get_edge_pool": {
                            "input": {
                                "master_subnet": '172.21.0.0/16',
                                "edge_ipam_details": [
                                    {
                                        "masterSubnetDto": {
                                            "pool": "172.21.0.0",
                                            "mask": "16"
                                        }
                                    }
                                ]
                            },
                            "output": {
                                "masterSubnetDto": {
                                    "pool": "172.21.0.0",
                                    "mask": "16"
                                }
                            }
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "mid",
                                "edge_sub_type": "trial"
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "output": ("mid", "trial")
                        },
                        "set_subscriber_pool": {
                            "input": None,
                            "output": generator_helper.STATIC_MID_SUBSCRIBER_LAN_POOLS[1024]
                        },
                        "set_ap_pool": {
                            "input": None,
                            "output": generator_helper.STATIC_MID_MGMT_POOLS
                        },
                        "set_cpe_pool": {
                            "input": None,
                            "output": generator_helper.MID_CPE_POOLS[0]
                        },
                        "set_switch_pool": {
                            "input": None,
                            "output": ['172.29.0.0/18','172.29.64.0/18','172.29.128.0/17']
                        },
                        "get_last_ip": {
                            "input": {
                                "subnetDto": {
                                    "subnet": "192.168.2.5",
                                    "mask": 8
                                }
                            },
                            "output": "192.255.255.254"
                        },
                        "get_netmask": {
                            "input": {
                                "subnetDto": {
                                    "subnet": "192.168.2.1",
                                    "mask": 14
                                }
                            },
                            "output": ipam.IPAddress("255.252.0.0")
                        },
                        "get_bitmask": {
                            "input": {
                                "subnetDto": {
                                    "mask": 14
                                }
                            },
                            "output": '14'
                        },
                        "get_vpn_details": {
                            "input": [],
                            "output": (False, None)
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.26.0.0",
                                        "mask": 15
                                    },
                                    "subnetDto": {
                                        "subnet": "192.164.4.8",
                                        "mask": 5
                                    }
                                }
                            ],
                            "output": {
                                "wan_set": True,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('248.0.0.0'),
                                "wan_first_ip": "192.164.4.9",
                                "wan_ip_subnet_ap": "192.164.4.8",
                                "wan_ip_subnet_bitmask": "5",
                                "wan_last_ip": "199.255.255.254",
                                "wan_network_ip": "192.164.4.8",
                                "wan_second_ip_ap": "192.164.4.10",
                                "wan_start_ip": "192.164.4.11"
                            }
                        },
                        "get_lan_details": {
                            "input": {
                                "edge_ipam_details": [{
                                    "masterSubnetDto": {
                                        "pool": "100.64.0.0",
                                        "mask": 11
                                    },
                                    "subnetDto": {
                                        "subnet": "192.168.4.5",
                                        "mask": 12
                                    }
                                }],
                                "subscriber_lan_pool": ["100.64.0.0/10"]
                            },
                            "output":{
                                "lan_set": False
                            }
                        },
                        "get_pseudo_tp_lan_details": {
                            "input": {
                                "edge_details": {
                                    "edgeSubType": "trial"
                                },
                                "edge_ipam_details":[
                                ]
                            },
                            "output": {}
                        },
                        "get_cpe_details": {
                            "input": {
                                "cpe_pool": '172.21.0.0/16',
                                "edge_ipam_details": [
                                    {
                                        "masterSubnetDto": {
                                            "pool": "172.21.0.0",
                                            "mask": "16"
                                        },
                                        "subnetDto": {
                                            "subnet": "144.168.4.5",
                                            "mask": 12
                                        }
                                    }
                                ]
                            },
                            "output":{
                                "wan_vpn_set": True,
                                "wan_first_ip_cpe": "144.168.4.6",
                                "wan_second_ip_cpe":"144.168.4.7",
                                "wan_last_ip_cpe": "144.175.255.254",
                                "wan_cpe_ip_subnet_netmask": ipam.IPAddress('255.240.0.0'),
                                "wan_ip_subnet_cpe": "144.168.4.5",
                                "wan_cpe_ip_subnet_bitmask": "12"
                            }
                        },
                        "get_switch_details": {
                            "input": {
                                "switch_pool": ['172.29.0.0/18'],
                                "edge_ipam_details": [
                                    {
                                        "masterSubnetDto": {
                                            "pool": "172.29.0.0",
                                            "mask": "18"
                                        },
                                        "subnetDto": {
                                            "subnet": "144.128.4.5",
                                            "mask": 20
                                        }
                                    }
                                ]
                            },
                            "output":{
                                "switch_first_ip": "144.128.4.6",
                                "switch_ip_subnet_bitmask":"20"
                            }
                        },
                        "get_edge_pool": {
                            "input": {
                                "master_subnet": '172.21.0.0/16',
                                "edge_ipam_details": [
                                    {
                                        "masterSubnetDto": {
                                            "pool": "172.21.0.1",
                                            "mask": "16"
                                        }
                                    }
                                ]
                            },
                            "output": False
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "mobile",
                                "edge_sub_type": "trial",
                                "subscribers": 128
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "output": ("mobile", "trial")
                        },
                        "set_subscriber_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_SUBSCRIBER_LAN_POOLS[128]
                        },
                        "set_vpn_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_VPN_POOL
                        },
                        "set_ap_pool": {
                            "input": None,
                            "output": ['172.22.0.0/16','172.23.0.0/16','172.20.0.0/16','172.26.0.0/15']
                        },
                        "set_cpe_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_CPE_POOLS[0]
                        },
                        "set_switch_pool": {
                            "input": None,
                            "output": []
                        },
                        "get_vpn_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.17.128.0",
                                        "mask": 17
                                    },
                                    "subnetDto": {
                                        "subnet": "This is the subnet"
                                    }
                                }
                            ],
                            "output": (True, "This is the subnet")
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.22.0.0",
                                        "mask": 16
                                    },
                                    "subnetDto": {
                                        "subnet": "123.221.43.7",
                                        "mask": 28
                                    }
                                }
                            ],
                            "output": {
                                "wan_set": True,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('255.255.255.240'),
                                "wan_first_ip": "123.221.43.8",
                                "wan_ip_subnet_ap": "123.221.43.7",
                                "wan_ip_subnet_bitmask": "28",
                                "wan_last_ip": "123.221.43.14",
                                "wan_network_ip": "123.221.43.7",
                                "wan_second_ip_ap": "123.221.43.9",
                                "wan_start_ip": "123.221.43.10"
                            }
                        },
                        "get_cpe_details": {
                            "input": {
                                "cpe_pool": '172.21.0.0/16',
                                "edge_ipam_details": []
                            },
                            "output":{
                                "wan_vpn_set":False
                            }
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "trial",
                                "edge_sub_type": "nuc",
                                "subscribers": 12
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "output": ("trial", "nuc")
                        },
                        "set_subscriber_pool": {
                            "input": None,
                            "output": generator_helper.NUC_SUBSCRIBER_LAN_POOLS[12]
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "mobile",
                                "edge_sub_type": "kontronmetro"
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "set_vpn_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_VPN_POOL_KONTRON_METRO
                        },
                        "set_ap_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_AP_POOLS[29]
                        },
                        "get_vpn_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.23.0.0",
                                        "mask": 16
                                    },
                                    "subnetDto": {
                                        "subnet": "This is the subnet"
                                    }
                                }
                            ],
                            "output": (True, "This is the subnet")
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.23.0.0",
                                        "mask": 16
                                    },
                                    "subnetDto": {
                                        "subnet": "148.221.43.22",
                                        "mask": 26
                                    },
                                    "ipAddressDto" : [ {
                                        "hostname" : "test_ap_1",
                                        "ipAddress": "this is where ip address go"
                                    }]
                                }
                            ],
                            "output": {
                                "wan_set": True,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('255.255.255.192'),
                                "wan_first_ip": "148.221.43.23",
                                "wan_ip_subnet_ap": "148.221.43.22",
                                "wan_ip_subnet_bitmask": "26",
                                "wan_last_ip": "148.221.43.62",
                                "wan_network_ip": "148.221.43.22",
                                "wan_second_ip_ap": "148.221.43.24",
                                "wan_start_ip": "148.221.43.25",
                                "ap_last_ip": "this is where ip address go",
                                "ap_1_ip": "this is where ip address go"
                            }
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "mobile",
                                "edge_sub_type": "railtel_pilot_ec"
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "set_vpn_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_VPN_POOL_KONTRON_METRO
                        },
                        "set_ap_pool": {
                            "input": None,
                            "output": generator_helper.MOBILE_AP_POOLS[27]
                        },
                        "get_vpn_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.23.0.0",
                                        "mask": 16
                                    },
                                    "subnetDto": {
                                        "subnet": "This is the subnet"
                                    }
                                }
                            ],
                            "output": (True, "This is the subnet")
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.26.0.0",
                                        "mask": 15
                                    },
                                    "subnetDto": {
                                        "subnet": "48.21.3.82",
                                        "mask": 22
                                    },
                                    "ipAddressDto": [{
                                        "hostname": "test_ap_2",
                                        "ipAddress": "this is where ip address go"
                                    }]
                                }
                            ],
                            "output": {
                                "wan_set": True,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('255.255.252.0'),
                                "wan_first_ip": "48.21.3.83",
                                "wan_ip_subnet_ap": "48.21.3.82",
                                "wan_ip_subnet_bitmask": "22",
                                "wan_last_ip": "48.21.3.254",
                                "wan_network_ip": "48.21.3.82",
                                "wan_second_ip_ap": "48.21.3.84",
                                "wan_start_ip": "48.21.3.85",
                                "ap_last_ip": "this is where ip address go",
                                "ap_2_ip": "this is where ip address go"
                            }
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "jinja2": {
                                "edge_type": "mid",
                                "edge_sub_type": "ct_static"
                            },
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "set_ap_pool": {
                            "input": None,
                            "output": generator_helper.CT_STATIC_MID_MGMT_POOLS
                        },
                        "get_wan_details": {
                            "input": [
                                {
                                    "masterSubnetDto": {
                                        "pool": "172.29.128.0",
                                        "mask": 17
                                    },
                                    "subnetDto": {
                                        "subnet": "221.37.44.96",
                                        "mask": 20
                                    }
                                }
                            ],
                            "output": {
                                "wan_set": True,
                                "wan_ap_ip_subnet_netmask": ipam.IPAddress('255.255.240.0'),
                                "wan_first_ip": "221.37.44.97",
                                "wan_ip_subnet_ap": "221.37.44.96",
                                "wan_ip_subnet_bitmask": "20",
                                "wan_last_ip": "221.37.47.254",
                                "wan_network_ip": "221.37.44.96",
                                "wan_second_ip_ap": "221.37.44.98",
                                "wan_start_ip": "221.37.44.99"
                            }
                        }
                    }
                }
            ],
        "exception": [
                {
                    "edge_id": "123456",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details1.json",
                            "return_code": 404
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "expected_exception" : ipam.HTTPExceptionFactory
                        }
                    }
                },
                {
                    "edge_id": "245678",
                    "server_configs": {
                        "edge-details": {
                            "template": "inaccurate_responses/edge-details.json",
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_edge_type_subtype": {
                            "input": None,
                            "expected_exception": ipam.HTTPExceptionFactory
                        }
                    }
                },
                {
                    "edge_id": "123456",
                    "server_configs": {
                        "edge-details": {
                            "template": "accurate_responses/edge-details3.json",
                            "return_code": 200
                        }
                    },
                    "methods": {
                        "get_subnet": {
                            "input": {},
                            "expected_exception": KeyError
                        },
                        "get_first_ip": {
                            "input": {},
                            "expected_exception": KeyError
                        },
                        "get_second_ip": {
                            "input": {},
                            "expected_exception": KeyError
                        },
                        "get_last_ip": {
                            "input": {},
                            "expected_exception": KeyError
                        },
                        "get_netmask": {
                            "input": {},
                            "expected_exception": KeyError
                        },
                        "get_bitmask": {
                            "input": {},
                            "expected_exception": KeyError
                        }
                    }
                }
            ]
        }

    def iterate_over_scenarios(self, test_method, callback):
        for scenario in TestIPAM.test_scenarios["standard"]:
            methods = scenario["methods"]
            if test_method not in methods:
                continue
            edge_id = scenario["edge_id"]
            server_configs = scenario["server_configs"]
            method_details = methods[test_method]
            input = method_details["input"]
            output = method_details["output"]
            utilities.update_ipam_db_server_configs(server_configs)
            self.assertEqual(
                callback(edge_id,input), output)

        for scenario in TestIPAM.test_scenarios["exception"]:
            methods = scenario["methods"]
            if test_method not in methods:
                continue
            edge_id = scenario["edge_id"]
            server_configs = scenario["server_configs"]
            method_details = methods[test_method]
            input = method_details["input"]
            expected_exception = method_details["expected_exception"]
            utilities.update_ipam_db_server_configs(server_configs)
            with self.assertRaises(expected_exception):
                callback(edge_id, input)

    def test_get_edge_type_sub_type(self):
        test_method = "get_edge_type_subtype"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_edge_type_subtype()
        self.iterate_over_scenarios(test_method, callback)

    def test_set_subscriber_pool(self):
        test_method = "set_subscriber_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.set_subscriber_pool()
            return ipam_controller.subscriber_lan_pool
        self.iterate_over_scenarios(test_method, callback)

    def test_set_vpn_pool(self):
        test_method = "set_vpn_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.set_vpn_pool()
            return ipam_controller.vpn_pool
        self.iterate_over_scenarios(test_method, callback)

    def test_set_ap_pool(self):
        test_method = "set_ap_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.set_ap_pool()
            return ipam_controller.ap_pool
        self.iterate_over_scenarios(test_method, callback)

    def test_set_cpe_pool(self):
        test_method = "set_cpe_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.set_cpe_pool()
            return ipam_controller.cpe_pool
        self.iterate_over_scenarios(test_method, callback)

    def test_set_switch_pool(self):
        test_method = "set_switch_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.set_switch_pool()
            return ipam_controller.switch_pool
        self.iterate_over_scenarios(test_method, callback)

    def test_get_subnet(self):
        test_method = "get_subnet"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_subnet(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_network(self):
        # The get subnet function and the get network functions are the same. 
        # test_method sets the test scenarios used. Since the functions are virtually the same, the same test scenarios work.
        test_method = "get_subnet"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_network(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_first_ip(self):
        test_method = "get_first_ip"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_first_ip(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_second_ip(self):
        test_method = "get_second_ip"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_second_ip(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_last_ip(self):
        test_method = "get_last_ip"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_last_ip(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_netmask(self):
        test_method = "get_netmask"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_netmask(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_bitmask(self):
        test_method = "get_bitmask"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_bitmask(input)
        self.iterate_over_scenarios(test_method, callback)

    def test_get_vpn_details(self):
        test_method = "get_vpn_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input
            ipam_controller.get_vpn_details()
            return ipam_controller.ip_values["vpn_set"], ipam_controller.ip_values.get("vpn_ip")
        self.iterate_over_scenarios(test_method, callback)

    def test_get_wan_details(self):
        test_method = "get_wan_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input
            ipam_controller.get_wan_details()
            return ipam_controller.ip_values
        self.iterate_over_scenarios(test_method, callback)

    def test_get_lan_details(self):
        test_method = "get_lan_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input["edge_ipam_details"]
            ipam_controller.subscriber_lan_pool = input["subscriber_lan_pool"]
            ipam_controller.get_lan_details()
            return ipam_controller.ip_values
        self.iterate_over_scenarios(test_method, callback)

    def test_get_pseudo_tp_lan_details(self):
        test_method = "get_pseudo_tp_lan_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input["edge_ipam_details"]
            ipam_controller.edge_details = input["edge_details"]
            ipam_controller.get_pseudo_tp_lan_details()
            return ipam_controller.ip_values
        self.iterate_over_scenarios(test_method, callback)

    def test_get_cpe_details(self):
        test_method = "get_cpe_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input["edge_ipam_details"]
            ipam_controller.cpe_pool = input["cpe_pool"]
            ipam_controller.get_cpe_details()
            return ipam_controller.ip_values
        self.iterate_over_scenarios(test_method, callback)

    def test_get_switch_details(self):
        test_method = "get_switch_details"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input["edge_ipam_details"]
            ipam_controller.switch_pool = input["switch_pool"]
            ipam_controller.get_switch_details()
            return ipam_controller.ip_values
        self.iterate_over_scenarios(test_method, callback)

    def test_get_all_ip(self):
        test_method = "get_all_ip"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            return ipam_controller.get_all_ip()
        self.iterate_over_scenarios(test_method, callback)

    def test_get_edge_pool(self):
        test_method = "get_edge_pool"

        def callback(edge_id, input):
            ipam_controller = ipam.Controller(edge_id)
            ipam_controller.edge_ipam_details = input["edge_ipam_details"]
            master_subnet = input["master_subnet"]
            return ipam_controller.get_edge_pool(master_subnet)
        self.iterate_over_scenarios(test_method, callback)
