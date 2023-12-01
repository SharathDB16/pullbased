from libutils.base.config.configuration import config_obj
from libutils.generator_helper.ipam import Controller
from libutils.generator_helper.dpverse import DPController
from libutils.generator_helper.externalip import ExternalIP
from libutils.generator_helper.wireguardip import WireGuardIP
from libutils.generator_helper.cdn_externalip import CdnExternalIP
from netaddr import iter_iprange, IPAddress


class Base:
    def __init__(self, edge_id):
        self.context = dict()
        i_pam_obj = Controller(edge_id)
        if i_pam_obj.get_all_ip():
            self.context.update(i_pam_obj.get_all_ip())
        dp_verse_obj = DPController(edge_id)
        if dp_verse_obj.get_dp_verse_details():
            self.context.update(dp_verse_obj.get_dp_verse_details())
        self.context["wan_interface_name"] = "lxcbr0"
        self.context["container1_ip"] = "5.5.5.5"
        self.context["container1_name"] = "dumb01"
        self.context["dns_server1"] = "103.195.71.118"
        self.context["dns_server2"] = "103.195.71.119"
        self.context["agent_version"] = ""
        self.context["cores"] = ""
        self.context["radius_server_name"] = "edge.sboxnw.com"
        self.context["lan_interface_name"] = "enp3s0"
        self.context["ap_interface_name"] = "enp3s0.21"
        self.context["cpe_interface_name"] = "enp2s0.30"

        if config_obj.environment_type == "staging":
            self.context.update({"cls_env": "cls01.stg.sboxdc.com", "pds_env": "pds01.stg.sboxdc.com",
                                 "sms_env": "sms01.stg.sboxdc.com", "apphost_env": "apphosting01.stg.sboxdc.com",
                                 "cps_env": "cps01.stg.sboxdc.com", "apigw_env": "apigw01.stg.sboxdc.com",
                                 "repo_env": "repo.stg.sboxdc.com", "env_type": "staging",
                                 "host_list": ["kfk01.stg.sboxdc.com:9092", "kfk02.stg.sboxdc.com:9092",
                                               "kfk03.stg.sboxdc.com:9092"]})
        else:
            self.context.update({"cls_env": "cls02.sboxdc.com", "pds_env": "pds01.sboxdc.com",
                                 "sms_env": "sms01.sboxdc.com", "apphost_env": "apphosting01.sboxdc.com",
                                 "cps_env": "cps01.sboxdc.com", "apigw_env": "apigw01.sboxdc.com",
                                 "repo_env": "repo.sboxdc.com", "env_type": "production",
                                 "host_list": ["kfk04.sboxdc.com:9092", "kfk05.sboxdc.com:9092",
                                               "kfk06.sboxdc.com:9092"]})


class Generic(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"gsm_enabled": "false"})
        self.context.update({"download_stratergy": "origin"})
        if edge_type == "static":
            self.context.update({"caching_stratergy": "static"})
            self.context.update({"expose_remote_api": "False"})
            self.context.update({"keep_tar": "False"})
            self.context.update({"req_resolution": "576"})
        elif edge_type == "mid":
            self.context.update({"caching_stratergy": "mid"})
            self.context.update({"expose_remote_api": "True"})
            self.context.update({"keep_tar": "True"})
            self.context.update({"req_resolution": "576"})
        else:
            self.context.update({"caching_stratergy": "mobile"})
            self.context.update({"expose_remote_api": "False"})
            self.context.update({"keep_tar": "False"})
            self.context.update({"req_resolution": "576"})
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 2),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})

    def get_context(self):
        return self.context


class Nuc(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"wan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})

    def get_context(self):
        return self.context


class Kontronmetro(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        wg_ip_obj = WireGuardIP(edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"ap_interface_name": "ap0"})
        self.context.update({"cpe_interface_name": "cpe0"})
        self.context.update({"dongle_interface_name": "dongle0"})
        self.context.update({"download_stratergy": "mid"})
        self.context.update({"caching_stratergy": "mobile"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "true"})
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 1),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": ["10.26.0"]})
        self.context.update(wg_ip_obj.get_wireguard_details())
        if config_obj.environment_type == "staging":
            self.context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context


class C2cbus(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"wan_list": ""})
        self.context.update({"wan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"ap_interface_name": "ap0"})
        self.context.update({"cpe_interface_name": "cpe0"})
        self.context.update({"download_stratergy": "mid"})
        self.context.update({"caching_stratergy": "mobile"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "true"})
        self.context.update({"dongle_interface_name": "dongle0"})

    def get_context(self):
        return self.context


class Railtelpilotec(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"ap_interface_name": "enp2s0"})
        self.context.update({"cpe_interface_name": "cpe0"})
        self.context.update({"download_stratergy": "mid"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"dongle_interface_name": "dongle0"})
        self.context.update({"gsm_enabled": "true"})
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 1),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})
        self.context.update({"wan_ap_first_ip": wan_list[0], "wan_ap_last_ip": wan_list[-1]})

    def get_context(self):
        return self.context


class Ctstatic(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        ext_ip_obj = ExternalIP(edge_id)
        self.context.update({"lan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"public_dns_ip": "8.8.8.8"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update(ext_ip_obj.get_external_ip_details())
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 2),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})

    def get_context(self):
        return self.context


class Ruralwgcsc(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        ext_ip_obj = ExternalIP(edge_id)
        wg_ip_obj = WireGuardIP(edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"public_dns_ip": "8.8.8.8"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update(ext_ip_obj.get_external_ip_details())
        self.context.update(wg_ip_obj.get_wireguard_details())
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 2),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})

        if config_obj.environment_type == "staging":
            self.context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context


class Firefly(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        ext_ip_obj = ExternalIP(edge_id)
        wg_ip_obj = WireGuardIP(edge_id)
        self.context.update({"lan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"public_dns_ip": "8.8.8.8"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"online_interface": "enp2s0"})
        self.context.update(ext_ip_obj.get_external_ip_details())
        self.context.update(wg_ip_obj.get_wireguard_details())
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 2),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})

        if config_obj.environment_type == "staging":
            self.context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context


class CDN(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        self.context = dict()
        cdn_ext_ip_obj = CdnExternalIP(edge_id)
        self.context.update({"lan_first_ip": ""})
        self.context.update({"wan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update(cdn_ext_ip_obj.get_cdn_external_ip_details())
        if config_obj.environment_type == "staging":
            self.context.update({"cdn_publish": "receiveFromLive", "cdn_branch": "sandbox-master", "cdn_tier_index": "0",
                                 "cdn_subscribe": "publishToLive", "wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "cdn_env": "production", "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"cdn_publish": "receiveFromLive", "cdn_branch": "sandbox-master", "cdn_tier_index": "0",
                                 "cdn_subscribe": "publishToLive", "wg_endpoint": "evpn.sboxdc.com:51820",
                                 "cdn_env": "production", "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context


class IFE(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        wg_ip_obj = WireGuardIP(edge_id)
        self.context.update({"lan_first_ip": "172.23.100.30"})
        self.context.update({"wan_list": ["10.23.10"]})
        self.context.update({"wan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"ap_interface_name": "ap0"})
        self.context.update({"cpe_interface_name": "cpe0"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update({"online_interface": "wg0"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "720"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update(wg_ip_obj.get_wireguard_details())

        if config_obj.environment_type == "staging":
            self.context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context


class CR(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"ap_interface_name": "enp2s0"})
        self.context.update({"cpe_interface_name": "cpe0"})
        self.context.update({"download_stratergy": "mid"})
        self.context.update({"caching_stratergy": "static"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"gsm_enabled": "true"})
        self.context.update({"dongle_interface_name": "dongle0"})
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 1),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})
        self.context.update({"wan_ap_first_ip": wan_list[0], "wan_ap_last_ip": wan_list[-1]})

    def get_context(self):
        return self.context


class Pseudotp(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        pseudo_tp_obj = Controller(edge_id)
        self.context.update({"lan_first_ip": ""})
        self.context.update({"wan_first_ip": ""})
        self.context.update({"wan_list": ["10.25"]})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"caching_stratergy": "mid"})
        self.context.update({"expose_remote_api": "True"})
        self.context.update({"keep_tar": "True"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update({"online_interface": "eno2"})
        self.context.update(pseudo_tp_obj.get_pseudo_tp_details())

    def get_context(self):
        return self.context


class Portablemid():

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        self.context.update({"lan_first_ip": ""})
        self.context.update({"wan_first_ip": ""})
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"caching_stratergy": "mid"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update({"expose_remote_api": "True"})
        self.context.update({"keep_tar": "True"})
        self.context.update({"req_resolution": "576"})
    def get_context(self):
        return self.context

class Cargoship(Base):

    def __init__(self, edge_id, edge_type, edge_sub_type):
        Base.__init__(self, edge_id)
        ext_ip_obj = ExternalIP(edge_id)
        wg_ip_obj = WireGuardIP(edge_id)
        self.context.update({"edge_type": edge_type})
        self.context.update({"edge_sub_type": edge_sub_type})
        self.context.update({"public_dns_ip": "8.8.8.8"})
        self.context.update({"expose_remote_api": "False"})
        self.context.update({"keep_tar": "False"})
        self.context.update({"req_resolution": "576"})
        self.context.update({"gsm_enabled": "false"})
        self.context.update({"download_stratergy": "origin"})
        self.context.update(wg_ip_obj.get_wireguard_details())
        wan_list = list(iter_iprange(str(IPAddress(self.context['wan_first_ip']) + 2),
                                     str(self.context['wan_last_ip'])))
        self.context.update({"wan_list": wan_list})

        if config_obj.environment_type == "staging":
            self.context.update({"wg_endpoint": "wirevpn.stg.sboxdc.com:51820",
                                 "wg_public_key": "MyZJCWDz1Tre+rqmQUtkV5dfXTySVdgQ7xVWZuTSVgI="})
        else:
            self.context.update({"wg_endpoint": "evpn.sboxdc.com:51820",
                                 "wg_public_key": "bdUlcbBH4tkQ3ChN43/pY5SPiEKEMI3UHOnMwFPAayw="})

    def get_context(self):
        return self.context
