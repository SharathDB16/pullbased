import requests
from netaddr import IPAddress
from libutils.base.config.configuration import config_obj


class ExternalIP:
    def __init__(self, edge_id):
        self.ext_values = dict()
        self.edge_id = edge_id.strip()

    def get_external_ip_details(self):
        ext_details = requests.get(config_obj.external_ip_details_url + self.edge_id).json()
        if ext_details['meta']['code'] == 200:
            for data in ext_details['data']:
                if data['ipType'] == 'LANIP':
                    self.ext_values["lan_edge_ip1"] = data['ipStart']
                    self.ext_values["lan_edge_ip2"] = str(IPAddress(data['ipStart']) + 1)
                    self.ext_values["lan_edge_bitmask"] = data['subnet']
                    self.ext_values["lan_edge_gateway"] = data['gatewayIp']
                    return self.ext_values
