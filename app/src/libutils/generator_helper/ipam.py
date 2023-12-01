import json
import requests
import libutils.generator_helper
from libutils.base.config.configuration import config_obj
from netaddr import IPAddress, IPNetwork


class Controller:

    def __init__(self, edge_id):
        self.edge_details_url = config_obj.edge_details_url
        self.edge_id = edge_id.strip()
        self.edge_type = None
        self.edge_sub_type = None
        self.edge_details = None
        self.edge_ipam_details = None
        self.subscriber_lan_pool = None
        self.vpn_pool = None
        self.ap_pool = []
        self.switch_pool = []
        self.cpe_pool = None
        self.ip_values = dict()
        self.ip_details_url = f"{config_obj.ip_details_url}"
        self.subnet_search_url = f"{config_obj.ipam_subnet_search_url}"
        self.get_edge_details()

    def get_edge_details(self):
        response = requests.get("{}{}".format(self.edge_details_url, self.edge_id)).json()
        self.edge_details = response["data"]
        self.edge_type = self.edge_details["edgeType"].lower()
        self.edge_sub_type = self.edge_details["edgeSubType"].lower()
        self.set_subscriber_pool()
        self.set_ap_pool()
        self.set_cpe_pool()
        self.set_vpn_pool()
        self.set_switch_pool()

    def get_edge_type_subtype(self):
        return self.edge_type, self.edge_sub_type

    def is_cr_server(self):
        cr_subtypes = ["railtel_pilot_ec", "cr_poc"]
        if self.edge_sub_type in cr_subtypes:
            return True

    def set_subscriber_pool(self):
        self.subscriber_lan_pool = libutils.generator_helper.DEFAULT_LAN_POOL

    def set_vpn_pool(self):
        if self.edge_type == "mobile":
            self.vpn_pool = libutils.generator_helper.MOBILE_VPN_POOL
            if self.edge_sub_type == "kontronmetro" or self.is_cr_server():
                self.vpn_pool = libutils.generator_helper.MOBILE_VPN_POOL_KONTRON_METRO
        else:
            self.vpn_pool = libutils.generator_helper.STATIC_MID_VPN_POOL

    def set_ap_pool(self):
        if self.edge_type == "mobile":
            for key, list_value in libutils.generator_helper.MOBILE_AP_POOLS.items():
                for value in list_value:
                    self.ap_pool.append(value)
            if self.edge_sub_type == "kontronmetro":
                self.ap_pool = libutils.generator_helper.MOBILE_AP_POOLS[29]
            elif self.is_cr_server():
                self.ap_pool = libutils.generator_helper.MOBILE_AP_POOLS[27]
        elif self.edge_type == "static" or self.edge_type == "mid":
            self.ap_pool = libutils.generator_helper.STATIC_MID_MGMT_POOLS
            if self.edge_sub_type == "ct_static":
                self.ap_pool = libutils.generator_helper.CT_STATIC_MID_MGMT_POOLS
            if self.edge_sub_type == "rural_wg_csc" or self.edge_sub_type == "firefly":
                self.ap_pool = libutils.generator_helper.DEFAULT_MGMT_POOL

    def set_cpe_pool(self):
        if self.edge_type == "mobile":
            self.cpe_pool = libutils.generator_helper.MOBILE_CPE_POOLS[0]
        elif self.edge_type == "mid":
            self.cpe_pool = libutils.generator_helper.MID_CPE_POOLS[0]

    def set_switch_pool(self):
        if self.edge_type == "static" or self.edge_type == "mid":
            for key, list_value in libutils.generator_helper.SWITCH_MGMT_POOLS.items():
                for value in list_value:
                    self.switch_pool.append(value)

    def get_subnet(self, subnet):
        return subnet

    def get_first_ip(self, subnet):
        return str(IPAddress(subnet) + 1)

    def get_second_ip(self, subnet):
        return str(IPAddress(subnet) + 2)

    def get_last_ip(self, subnet, mask):
        ip = IPNetwork(subnet+'/'+str(mask))
        allips = list(ip.iter_hosts())
        if len(allips) > 1:
            return str(allips[len(allips)-1])
        return None

    def get_netmask(self, subnet, mask):
        ip = IPNetwork(subnet+'/'+str(mask))
        return ip.netmask

    def get_bitmask(self, mask):
        return str(mask)

    def get_vpn_details(self):
        details = self.get_edge_pool(self.vpn_pool)
        if details:
            subnet_val = details["subnetDto"]["subnet"]
            self.ip_values["vpn_set"] = True
            self.ip_values['vpn_ip'] = self.get_subnet(subnet_val)
        else:
            self.ip_values["vpn_set"] = False

    def get_wan_details(self, pyipam):
        if not pyipam:
            for pool in self.ap_pool:
                details = self.get_edge_pool(pool)
                if details:
                    subnet_val = details["subnetDto"]["subnet"]
                    mask_val = details["subnetDto"]["mask"]
                    break
        else:
            details = True
            subnet_val = libutils.generator_helper.COMMON_MGMT_POOL.split("/")[0]
            mask_val = libutils.generator_helper.COMMON_MGMT_POOL.split("/")[1]

        if details:
            self.ip_values["wan_set"] = True
            self.ip_values["wan_first_ip"] = self.get_first_ip(subnet_val)
            self.ip_values['wan_second_ip_ap'] = self.get_second_ip(subnet_val)
            self.ip_values['wan_last_ip'] = self.get_last_ip(subnet_val, mask_val)
            self.ip_values['wan_ap_ip_subnet_netmask'] = self.get_netmask(subnet_val, mask_val)
            self.ip_values['wan_ip_subnet_bitmask'] = self.get_bitmask(mask_val)
            self.ip_values['wan_network_ip'] = self.get_subnet(subnet_val)
            self.ip_values['wan_ip_subnet_ap'] = self.get_subnet(subnet_val)

            # Specific to Mikrotik
            self.ip_values['wan_start_ip'] = str(IPAddress(self.get_first_ip(subnet_val)) + 2)

            if self.is_cr_server():
                for ipAddr in details["ipAddressDto"]:
                    hostname = ipAddr['hostname']
                    pos = hostname.find('ap')
                    if pos != -1:
                        ap_ = hostname[pos + 2:pos + 4]
                        self.ip_values['ap' + ap_ + "_ip"] = ipAddr['ipAddress']
                        self.ip_values['ap_last_ip'] = ipAddr['ipAddress']
        else:
            self.ip_values["wan_set"] = False

    def get_lan_details(self, pyipam):
        self.ip_values["lan_set"] = False
        if not pyipam:
            for pool in self.subscriber_lan_pool:
                details = self.get_edge_pool(pool)
                if details:
                    subnet_val = details["subnetDto"]["subnet"]
                    mask_val = details["subnetDto"]["mask"]
                    break
        else:
            details = True
            subnet_val = libutils.generator_helper.COMMON_SUB_POOL.split("/")[0]
            mask_val = libutils.generator_helper.COMMON_SUB_POOL.split("/")[1]

        if details:
            self.ip_values["lan_set"] = True
            self.ip_values["lan_first_ip"] = self.get_first_ip(subnet_val)
            self.ip_values['lan_second_ip'] = self.get_second_ip(subnet_val)
            self.ip_values['lan_last_ip'] = self.get_last_ip(subnet_val, mask_val)
            self.ip_values['lan_ip_subnet_netmask'] = self.get_netmask(subnet_val, mask_val)
            self.ip_values['lan_ip_subnet_bitmask'] = self.get_bitmask(mask_val)
            self.ip_values['lan_ip_subnet'] = self.get_subnet(subnet_val)
            ip = IPNetwork(self.get_subnet(subnet_val) + '/' + str(self.get_netmask(subnet_val, mask_val)))
            self.ip_values['lan_wifi_nw'] = self.get_subnet(subnet_val) + '/' + str(ip.prefixlen)
        else:
            self.ip_values["lan_set"] = False

    def fetch_pseudo_tp_values(self, pseudo_data):
        mask_val = pseudo_data["mask"]
        edge_id = pseudo_data["edge_id"]
        subnet_val = pseudo_data["subnet"]
        lan_vlan_number = pseudo_data["vlan_id"]
        lan_ip_subnet = self.get_subnet(subnet_val)
        lan_first_ip = self.get_first_ip(subnet_val)
        lan_second_ip = self.get_second_ip(subnet_val)
        lan_last_ip = self.get_last_ip(subnet_val, mask_val)
        lan_ip_subnet_bitmask = self.get_bitmask(mask_val)
        lan_ip_subnet_netmask = self.get_netmask(subnet_val, mask_val)
        return {"edge_id": edge_id, "lan_first_ip": lan_first_ip, "lan_second_ip": lan_second_ip,
                "lan_last_ip": lan_last_ip, "lan_ip_subnet_netmask": lan_ip_subnet_netmask,
                "lan_ip_subnet": lan_ip_subnet, "lan_ip_subnet_bitmask": lan_ip_subnet_bitmask,
                "lan_vlan_number": lan_vlan_number}

    def get_pseudo_tp_details(self):
        pseudo_tp_ip_values = []
        pseudo_vlan_details = requests.get(f"{self.ip_details_url}{self.edge_id}").json()["data"]
        self.ip_values['wan_network_ip'] = pseudo_vlan_details["parent_details"]["ip_address"]
        self.ip_values['wan_ip_subnet_bitmask'] = pseudo_vlan_details["parent_details"]["mask"]
        parent_subnet = IPNetwork(f"{self.ip_values['wan_network_ip']}/{self.ip_values['wan_ip_subnet_bitmask']}")
        self.ip_values['wan_first_ip'] = self.get_first_ip(parent_subnet.network)
        self.ip_values['wan_ap_ip_subnet_netmask'] = self.get_netmask(self.ip_values['wan_network_ip'],
                                                                      self.ip_values['wan_ip_subnet_bitmask'])
        for pseudo_vlan in pseudo_vlan_details['vlan_details']:
            pseudo_tp_ip_values.append(self.fetch_pseudo_tp_values(pseudo_vlan))
        self.ip_values["pseudo_tp_ip_values"] = pseudo_tp_ip_values
        return self.ip_values

    def get_cpe_details(self):
        if self.cpe_pool is not None:
            details = self.get_edge_pool(self.cpe_pool)
            if details:
                subnet_val = details["subnetDto"]["subnet"]
                mask_val = details["subnetDto"]["mask"]
                self.ip_values["wan_vpn_set"] = True
                self.ip_values['wan_first_ip_cpe'] = self.get_first_ip(subnet_val)
                self.ip_values['wan_second_ip_cpe'] = self.get_second_ip(subnet_val)
                self.ip_values['wan_last_ip_cpe'] = self.get_last_ip(subnet_val, mask_val)
                self.ip_values['wan_cpe_ip_subnet_netmask'] = self.get_netmask(subnet_val, mask_val)
                self.ip_values['wan_ip_subnet_cpe'] = self.get_subnet(subnet_val)
                self.ip_values['wan_cpe_ip_subnet_bitmask'] = self.get_bitmask(mask_val)
            else:
                self.ip_values["wan_vpn_set"] = False

    def get_switch_details(self):
        for pool in self.switch_pool:
            details = self.get_edge_pool(pool)
            if details:
                break

        if details:
            subnet_val = details["subnetDto"]["subnet"]
            mask_val = details["subnetDto"]["mask"]
            self.ip_values['switch_first_ip'] = self.get_first_ip(subnet_val)
            self.ip_values['switch_ip_subnet_bitmask'] = self.get_bitmask(mask_val)
        else:
            self.ip_values["switch_set"] = False

    def get_all_ip(self):
        if self.edge_sub_type != "parent_pseudo_tp" and self.edge_sub_type != "portable_mid":
            if self.edge_sub_type != "kontronmetro" and self.edge_sub_type != "rural_wg_csc" and self.edge_sub_type != "cargo_ship":
                pyipam = False
                values = json.dumps({'searchKey': "edgeid", 'value': self.edge_id})
                self.edge_ipam_details = requests.post(self.subnet_search_url, data=values,
                                                    headers={'content-type': 'application/json'}).json()["data"]
                self.get_vpn_details()
                self.get_cpe_details()
            else:
                pyipam = True
                #self.edge_ipam_details = requests.get().json()["data"]

            self.get_lan_details(pyipam)
            self.get_wan_details(pyipam)

            if self.edge_type == "mid":
                self.get_switch_details()

        return self.ip_values

    def get_edge_pool(self, master_subnet):
        """
        Fetch Data about the subnet from the IPAM cached data
        """
        for pool in self.edge_ipam_details:
            ip = pool["masterSubnetDto"]["pool"]
            mask = pool["masterSubnetDto"]["mask"]
            if (ip+'/'+str(mask)) == master_subnet:
                return pool
        return False
