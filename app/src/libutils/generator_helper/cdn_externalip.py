import requests
from libutils.base.config.configuration import config_obj


class CdnExternalIP:
    def __init__(self, edge_id):
        self.ext_values = dict()
        self.edge_id = edge_id.strip()

    def get_cdn_external_ip_details(self):
        ext_details = requests.get(config_obj.cdn_external_ip_details_url + self.edge_id).json()
        if ext_details['meta']['code'] == 200:
            self.ext_values["wg_tier"] = ext_details['data']['tier']
            self.ext_values["cdn_external_ip"] = ext_details['data']['cdnExternalIp']
            self.ext_values["cdn_dns_name"] = ext_details['data']['dnsName']
            self.ext_values["host_name"] = ext_details['data']['hostName']
            self.ext_values["wg_vpn_ip"] = ext_details['data']['wireguardDetails']['wgVpnIP']
            self.ext_values["wg_private_key"] = ext_details['data']['wireguardDetails']['wgPrivateKey']
            if ext_details['data']['parentTierDetails']:
                self.ext_values["cdn_parent_ip"] = ext_details['data']['parentTierDetails'][0]['cndExternalIp']
                self.ext_values["cdn_parent_hostname"] = "{}.sboxcdn.com".format(ext_details['data']['parentTierDetails'][0]['hostName'])
            else:
                self.ext_values["cdn_parent_ip"] = "NA"
                self.ext_values["cdn_parent_hostname"] = "NA"
            return self.ext_values
