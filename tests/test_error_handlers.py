# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Error Handlers
"""

from unittest import TestCase
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed, UnsupportedMediaType, InternalServerError
from service import app
from service.common import status
from service.common import error_handlers
from service.models import DataValidationError


class TestErrorHandlers(TestCase):
    """Test Cases for Error Handlers"""

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def _assert_error_response(self, resp, code, expected_code, expected_error):
        """Helper to validate standard error payload"""
        self.assertEqual(code, expected_code)
        data = resp.get_json()
        self.assertEqual(data["status"], expected_code)
        self.assertEqual(data["error"], expected_error)
        self.assertIn("message", data)

    def test_bad_request_handler(self):
        """It should handle 400 Bad Request"""
        resp, code = error_handlers.bad_request(BadRequest("bad request"))
        self._assert_error_response(resp, code, status.HTTP_400_BAD_REQUEST, "Bad Request")

    def test_not_found_handler(self):
        """It should handle 404 Not Found"""
        resp, code = error_handlers.not_found(NotFound("not found"))
        self._assert_error_response(resp, code, status.HTTP_404_NOT_FOUND, "Not Found")

    def test_method_not_allowed_handler(self):
        """It should handle 405 Method Not Allowed"""
        resp, code = error_handlers.method_not_supported(MethodNotAllowed("not allowed"))
        self._assert_error_response(resp, code, status.HTTP_405_METHOD_NOT_ALLOWED, "Method not Allowed")

    def test_unsupported_media_type_handler(self):
        """It should handle 415 Unsupported Media Type"""
        resp, code = error_handlers.mediatype_not_supported(UnsupportedMediaType("unsupported"))
        self._assert_error_response(
            resp, code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported media type"
        )

    def test_internal_server_error_handler(self):
        """It should handle 500 Internal Server Error"""
        resp, code = error_handlers.internal_server_error(InternalServerError("boom"))
        self._assert_error_response(
            resp, code, status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"
        )

    def test_data_validation_error_handler(self):
        """It should handle DataValidationError as 400 Bad Request"""
        resp, code = error_handlers.request_validation_error(DataValidationError("validation failed"))
        self._assert_error_response(resp, code, status.HTTP_400_BAD_REQUEST, "Bad Request")
