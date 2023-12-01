from json import JSONDecodeError
import re
import os
import requests

from flask_api import status
from flask_restful import Resource

from libutils.exception import HTTPExceptionFactory
from libutils.base.config.configuration import config_obj
from libutils.generator_helper.template_context import Generic, C2cbus, Kontronmetro, Nuc, Ctstatic, \
    Railtelpilotec, CDN, Ruralwgcsc, Firefly, IFE, CR, Pseudotp, Portablemid, Cargoship


def non_empty_string(string):
    if not string:
        raise ValueError("Must not be empty string")
    return string


def validate_edge_id(edge_id):
    if edge_id == '' or len(edge_id) != 6:
        raise ValueError("Invalid edge id")
    else:
        regex = r'[0-9a-f]{6}'
        validate = re.search(regex,edge_id)
        if validate:
            return edge_id
        else:
            raise ValueError("Invalid edge id")


def edge_type_subtype(edge_id):
    response = requests.get("{}{}".format(config_obj.edge_details_url, edge_id))
    try:
        edge_data = response.json()
    except JSONDecodeError as e:
        raise HTTPExceptionFactory.get_HTPP_Exception("Did not receive json data from DP server", status.HTTP_503_SERVICE_UNAVAILABLE)
    try:
        if edge_data["meta"]["code"] == 404:
            raise HTTPExceptionFactory.get_HTPP_Exception("Could not find resource on DP server", status.HTTP_404_NOT_FOUND)
        return edge_data["data"]["edgeType"].lower(), edge_data["data"]["edgeSubType"].lower(), \
               edge_data["data"]["switchType"], edge_data["data"]["templateId"], edge_data["data"]["classificationTags"]
    except KeyError as e:
        raise HTTPExceptionFactory.get_HTPP_Exception(f"Response from DP server did not contain {e} key", status.HTTP_503_SERVICE_UNAVAILABLE)


def version_incrementer(version_no):
    if version_no is None:
        return float(0.01)
    else:
        str_value = str(version_no).split(".")[1]
        if str_value == "99":
            return float(round(version_no))
        else:
            return float(float(version_no) + 0.01)


def create_path_if_not_exists(file_path):
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path))
        except os.error as e:
            pass
    return


class HealthCheck(Resource):
    def __init__(self):
        pass

    def get(self):
        return {"StatusCode": "200", "Response": "OK"}, status.HTTP_200_OK


def get_context(edge_type, edge_sub_type):
    context_class = None
    if edge_type == "static":
        context_class = Generic
        if edge_sub_type == "nuc":
            context_class = Nuc
        elif edge_sub_type == "ct_static":
            context_class = Ctstatic
        elif edge_sub_type == "rural_wg_csc":
            context_class = Ruralwgcsc
        elif edge_sub_type == "firefly":
            context_class = Firefly
    elif edge_type == "mid":
        context_class = Generic
        if edge_sub_type == "parent_pseudo_tp":
            context_class = Pseudotp
        elif edge_sub_type == "portable_mid":
            context_class = Portablemid
    elif edge_type == "mobile":
        context_class = Generic
        if edge_sub_type == "kontronmetro":
            context_class = Kontronmetro
        elif edge_sub_type == "c2cbus":
            context_class = C2cbus
        elif edge_sub_type == "railtel_pilot_ec":
            context_class = Railtelpilotec
        elif edge_sub_type == "ife":
            context_class = IFE
        elif edge_sub_type == "cr_poc":
            context_class = CR
        elif edge_sub_type == "cargo_ship":
            context_class = Cargoship
    elif edge_type == "cdn":
        context_class = CDN

    return context_class
