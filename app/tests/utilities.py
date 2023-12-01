import json
import os, fnmatch
import subprocess
import unittest

from jsonschema import Draft6Validator
import pytest

DP_SERVER_CONFIG_PATH = "tests/server/config.json"
API_TEST_CASES_FOLDER = "tests/test_configs/test_cases"
FILE_TYPE_COMPARE_CALLBACK_MAP = {}

def get_api_test_cases(test_case_filter_pattern = "*_api.json"):
    test_case_names = fnmatch.filter(os.listdir(API_TEST_CASES_FOLDER), test_case_filter_pattern)
    for test_case_config_file in test_case_names:
        size = len(test_case_config_file)
        config_name = test_case_config_file[:size-9]
        test_case_config_file_path = API_TEST_CASES_FOLDER + "/" + test_case_config_file
        yield get_api_test_config( test_case_config_file_path, config_name)

def get_api_test_config(config_path, config_name):
    config_file = open(config_path, "r")
    config = json.load(config_file)
    config_file.close()
    return_data = pytest.param(config, config_name, id=config_name)
    return return_data

def compare_to_json_schema(filename, data):
    file = open(filename, "r")
    schema = json.load(file)
    file.close()
    validator = Draft6Validator(schema)
    return validator.is_valid(json.loads(data))

def compare_to_json_file(filename, data):
    try:
        file = open(filename, "r")
        json_data = json.loads(data)
        file_data = json.load(file)
        file.close()
        return json_data == file_data
    except Exception as e:
        return False
    return False

def compare_to_file_content(filename,data):
    file = open(filename, "r")
    file_data = file.read()
    file.close()
    return file_data == data

def compare_to_file(filename, data):
    for file_type in FILE_TYPE_COMPARE_CALLBACK_MAP:
        if not filename.endswith(file_type):
            continue
        compare_file_to_data = FILE_TYPE_COMPARE_CALLBACK_MAP[file_type]
        return compare_file_to_data(filename, data)
    return False

def get_config():
    config_file = open(DP_SERVER_CONFIG_PATH, "r")
    data = json.load(config_file)
    config_file.close()
    return data

def set_config(config):
    config_file =open(DP_SERVER_CONFIG_PATH, "w")
    config_file.write(json.dumps(config))
    config_file.close

def update_db(db_file_path):
    db_file = open(db_file_path, "r")
    subprocess.call(["mysql","--defaults-file=tests/mysql.cnf"], stdin=db_file)
    db_file.close()

def update_ipam_db_server_configs(server_configs):
    if not server_configs:
        return
    server_config = get_config()
    server_config.update(server_configs)
    set_config(server_config)

def parse_files_for_upload(files):
    parsed_files = dict()
    for arg_name in files :
        file_path = files.get(arg_name)
        file = open(file_path, "rb")
        parsed_files[arg_name] = file.read()
        file.close()
    return parsed_files