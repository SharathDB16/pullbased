import requests
from libutils.base.config.configuration import config_obj


class DPController:
    def __init__(self, edge_id):
        self.dp_values = dict()
        self.edge_id = edge_id.strip()

    def get_dp_verse_details(self):
        dp_details = requests.get(config_obj.edge_details_url + self.edge_id).json()
        dp_name = dp_details['data']['dpName']
        self.dp_values["dp_name"] = dp_name
        if dp_name == "HMRL":
            self.dp_values["ubnt_ip"] = "172.16.249.224"
        elif dp_name == "CMRL":
            self.dp_values["ubnt_ip"] = "172.16.249.225"
        else:
            self.dp_values["ubnt_ip"] = "172.16.249.224"
        self.dp_values["ap_count"] = dp_details['data']['ap']
        self.dp_values["wdvpn_ip"] = dp_details['data']['wdvpnIp']
        self.dp_values["tp_name"] = dp_details['data']['touchPointName']
        self.dp_values["state_name"] = dp_details['data']['stateName']
        self.dp_values["state_code"] = dp_details['data']['stateCode']
        self.dp_values["template_id"] = dp_details['data']['templateId']
        self.dp_values["template_name"] = dp_details['data']['templateName']
        self.dp_values["community_string"] = dp_details['data']['snmpCommunityString']
        self.dp_values["is_login_require"] = dp_details['data']['isLoginRequire']
        self.dp_values["is_premium_content_available"] = dp_details['data']['isPremiumContentAvailable']
        fup_dict = {"wg0_dlimit": -1, "cpe0_dlimit": -1, "wlo1_dlimit": -1, "eno2_dlimit": -1, "enp2s0_dlimit": -1,
                    "dongle0_dlimit": -1, "wg0_mlimit": -1, "cpe0_mlimit": -1, "wlo1_mlimit": -1, "eno2_mlimit": -1,
                    "enp2s0_mlimit": -1, "dongle0_mlimit": -1}
        if dp_details['data']['fupDto']:
            self.dp_values["fup_dto"] = dp_details['data']['fupDto']
            for data in dp_details['data']['fupDto']:
                interface = data["interfaceName"]["value"]
                fup_dict.update({f"{interface.lower()}_dlimit": data["dailyLimit"],
                                 f"{interface.lower()}_mlimit": data["monthlyLimit"]})
        self.dp_values.update(fup_dict)
        self.dp_values["aims_tag_id"] = None
        if dp_details['data']['classificationTags']:
            for tag in dp_details['data']['classificationTags']:
                if tag['value'].startswith("AIMS"):
                    self.dp_values["aims_tag_id"] = tag['key']
        return self.dp_values
