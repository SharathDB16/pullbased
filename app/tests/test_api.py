import requests

from flask_api import status
import pytest

from tests import utilities

utilities.FILE_TYPE_COMPARE_CALLBACK_MAP = {
    "schema.json": utilities.compare_to_json_schema,
    ".json": utilities.compare_to_json_file,
    ".txt" : utilities.compare_to_file_content
}


@pytest.mark.parametrize("test_case, test_case_name", utilities.get_api_test_cases())
def test_api(test_case, test_case_name):
    scenarios = test_case.get("scenarios", {})
    initial_database_state = test_case.get("dbfile", "tests/initialdb.sql")
    if initial_database_state:
        utilities.update_db(initial_database_state)
    for index, scenario in enumerate(scenarios):
        method = scenario.get("method", "get")
        call_method = getattr(requests, method)
        server_configs = scenario.get("server_configs",{})
        utilities.update_ipam_db_server_configs(server_configs)
        expected_response_code = scenario.get("response_code", status.HTTP_200_OK)
        expected_content_file_path = scenario.get("expected_content", None)
        url_params = scenario.get("url_params",{})
        url = test_case.get("url").format(**url_params)
        request_params = scenario.get("request_params", {})
        initial_database_state = scenario.get("dbfile", None)
        files = request_params.get("files", None)
        if files:
            request_params.update(dict(files=utilities.parse_files_for_upload(files)))
        if initial_database_state:
            utilities.update_db(initial_database_state)
        response = call_method(url, **request_params)
        assert response.status_code == expected_response_code, \
            "Received wrong status for \"%s\" scenario of \"%s\" test case" % (scenario.get("name", str(index)), test_case_name)
        if expected_content_file_path:
            response_matched = utilities.compare_to_file(expected_content_file_path, response.content.decode())
            assert response_matched == True, \
            "Received wrong response for \"%s\" scenario of \"%s\" test case" % (scenario.get("name", str(index)), test_case_name)
