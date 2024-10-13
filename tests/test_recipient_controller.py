import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from http import HTTPStatus

from marshmallow import ValidationError

from app.controllers.recipient_controller import RecipientController

class TestRecipientController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.controller = RecipientController()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.schemas.recipient.RecipientSchema.load')
    @patch('app.database.db.session.get')
    def test_create_recipient_success(self, mock_db_get, mock_load):
        """
        Test the create_recipient method for a successful case.
        """
        test_json_data = {
            "user_id": [3],
            "event_id": 1
        }

        mock_load.return_value = test_json_data
        mock_recipient = MagicMock()
        mock_db_get.return_value = mock_recipient

        mock_recipient_instance = MagicMock()
        mock_recipient = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.recipient_controller.RecipientInterface',
                       return_value=mock_recipient_instance) as mock_recipient_interface:
                with patch('app.controllers.recipient_controller.create_recipient',
                           return_value=mock_recipient) as mock_create_recipient:
                    response, status_code = self.controller.create_recipient()

        self.assertEqual(status_code, HTTPStatus.CREATED)

        expected_response = {
            'status': 'success',
            'message': 'Create recipient successfully',
            'data': None,
            'error': None
        }
        self.assertEqual(response.json, expected_response)

        mock_recipient_interface.assert_called_once_with(
            user_id=[3],
            event_id=1,
        )
        mock_create_recipient.assert_called_once_with(mock_recipient_instance)

    @patch('app.schemas.recipient.RecipientSchema.load')
    @patch('app.database.db.session.get')
    def test_create_recipient_validation_error(self, mock_db_get, mock_load):
        """
        Test the create_recipient method for validation error.
        """
        test_json_data = {
            "user_id": [3],
            "event_id": 1
        }

        mock_load.side_effect = ValidationError("Validation Error")

        with self.app.test_request_context(json=test_json_data):
            response, status_code = self.controller.create_recipient()

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json['error'], 'Validation Error')

if __name__ == '__main__':
    unittest.main()