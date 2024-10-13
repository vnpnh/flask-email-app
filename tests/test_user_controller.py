import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from http import HTTPStatus

from marshmallow import ValidationError

from app.controllers.user_controller import UserController


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.controller = UserController()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.schemas.user.UserSchema.load')
    @patch('app.database.db.session.get')
    def test_create_user_success(self, mock_db_get, mock_load):
        """
        Test the create user method for a successful case.
        """
        test_json_data = {
            "first_name": "budi",
            "last_name": "cheng",
            "email_address": "budi.cheng2@gmail.com"
        }

        mock_load.return_value = test_json_data
        mock_event = MagicMock()
        mock_db_get.return_value = mock_event

        mock_user_instance = MagicMock()
        mock_user = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.user_controller.UserInterface',
                       return_value=mock_user_instance) as mock_user_interface:
                with patch('app.controllers.user_controller.create_user',
                           return_value=mock_user) as mock_create_user:
                    response, status_code = self.controller.create_user()

        self.assertEqual(status_code, HTTPStatus.CREATED)

        expected_response = {
            'status': 'success',
            'message': 'Create user successfully',
            'data': None,
            'error': None
        }
        self.assertEqual(response.json, expected_response)

        mock_user_interface.assert_called_once_with(
            first_name="budi",
            last_name="cheng",
            email_address="budi.cheng2@gmail.com"
        )
        mock_create_user.assert_called_once_with(mock_user_instance)

    @patch('app.schemas.user.UserSchema.load')
    @patch('app.database.db.session.get')
    def test_create_user_validation_error(self, mock_db_get, mock_load):
        """
        Test the create_user method for validation error.
        """
        test_json_data = {
            "first_name": "budi",
            "last_name": "cheng",
            "email_address": "budi.cheng2@gmail.com"
        }

        mock_load.side_effect = ValidationError("Validation Error")

        with self.app.test_request_context(json=test_json_data):
            response, status_code = self.controller.create_user()

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json['error'], 'Validation Error')


    @patch('app.schemas.user.UserSchema.load')
    @patch('app.database.db.session.get')
    def test_create_user_internal_error(self, mock_db_get, mock_load):
        """
        Test the create user method for internal server error.
        """
        test_json_data = {
            "first_name": "budi",
            "last_name": "cheng",
            "email_address": "budi.cheng2@gmail.com"
        }

        mock_load.return_value = test_json_data
        mock_db_get.return_value = MagicMock()
        mock_user_instance = MagicMock()

        mock_user_instance = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.user_controller.UserInterface', return_value=mock_user_instance):
                with patch('app.controllers.user_controller.create_user',
                           side_effect=Exception("Something went wrong")):
                    response, status_code = self.controller.create_user()

        self.assertEqual(status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['error'], 'Internal Server Error')


if __name__ == '__main__':
    unittest.main()
