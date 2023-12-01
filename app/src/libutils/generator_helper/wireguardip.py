import requests
from libutils.base.config.configuration import config_obj


class WireGuardIP:
    def __init__(self, edge_id):
        self.ext_values = dict()
        self.edge_id = edge_id.strip()

    def get_wireguard_details(self):
        ext_details = requests.get(config_obj.wireguard_details_url + self.edge_id).json()
        if ext_details['meta']['code'] == 200:
            self.ext_values["wg_vpn_ip"] = ext_details['data']['wgVpnIP']
            self.ext_values["wg_private_key"] = ext_details['data']['wgPrivateKey']
            return self.ext_values
