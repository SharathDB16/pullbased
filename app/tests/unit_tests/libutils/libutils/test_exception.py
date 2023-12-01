import sys
import unittest

from werkzeug.http import HTTP_STATUS_CODES

sys.path.append("src")


from src.libutils import exception


class TestHTTPExceptionFactory(unittest.TestCase):
    def test_get_HTTP_exceptino(self):
        test_scenarios = [
            {
                "description": "This is a 500 error",
                "code": 500
            },
            {
                "description": "This is a 400 error",
                "code": 400
            }
        ]
        for scenario in test_scenarios:
            description = scenario["description"]
            code = scenario["code"]
            http_exception = exception.HTTPExceptionFactory.get_HTPP_Exception(description, code)
            try:
                raise http_exception
            except exception.HTTPException as e:
                self.assertEqual(e.get_description(), f"<p>{description}</p>")
                self.assertIsInstance(e.get_response(), exception.Response)
                self.assertEqual(e.name, HTTP_STATUS_CODES.get(code))
