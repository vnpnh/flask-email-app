import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from flask import Flask

from app.controllers.email_controller import EmailController


class TestEmailController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.controller = EmailController()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.schemas.email.EmailSchema.load')
    @patch('app.database.db.session.get')
    def test_save_email_success(self, mock_db_get, mock_load):
        """
        Test the save_email method for a successful case.
        """
        test_json_data = {
            'event_id': 1,
            'email_subject': 'Test Email',
            'email_content': 'This is a test email',
            'scheduled_at': '2024-10-15T12:00:00',
            'status': 'scheduled',
        }

        mock_load.return_value = test_json_data
        mock_event = MagicMock()
        mock_db_get.return_value = mock_event

        mock_email_instance = MagicMock()
        mock_email = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.email_controller.EmailInterface',
                       return_value=mock_email_instance) as mock_email_interface:
                with patch('app.controllers.email_controller.schedule_email',
                           return_value=mock_email) as mock_schedule_email:
                    response, status_code = self.controller.save_email()

        self.assertEqual(status_code, HTTPStatus.CREATED)

        expected_response = {
            'status': 'success',
            'message': 'Create email successfully',
            'data': None,
            'error': None
        }
        self.assertEqual(response.json, expected_response)

        mock_email_interface.assert_called_once_with(
            event_id=1,
            email_subject='Test Email',
            email_content='This is a test email',
            scheduled_at='2024-10-15T12:00:00',
            status='scheduled'
        )
        mock_schedule_email.assert_called_once_with(mock_email_instance)

    @patch('app.database.db.session.get')
    def test_save_email_validation_error(self, mock_db_get):
        """
        Test the save_email method for validation error.
        """
        test_json_data = {
            'event_id': 999,
            'email_subject': 'Test Email',
            'email_content': 'This is a test email',
            'scheduled_at': '2024-10-15T12:00:00'
        }

        mock_db_get.return_value = None

        with self.app.test_request_context(json=test_json_data):
            response, status_code = self.controller.save_email()

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json['error'], 'Validation Error')

    @patch('app.schemas.email.EmailSchema.load')
    @patch('app.database.db.session.get')
    def test_save_email_internal_error(self, mock_db_get, mock_load):
        """
        Test the save_email method for internal server error.
        """
        test_json_data = {
            'event_id': 1,
            'email_subject': 'Test Email',
            'email_content': 'This is a test email',
            'scheduled_at': '2024-10-15T12:00:00'
        }

        mock_load.return_value = test_json_data
        mock_db_get.return_value = MagicMock()
        mock_email_instance = MagicMock()

        mock_email_instance = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.email_controller.EmailInterface', return_value=mock_email_instance):
                with patch('app.controllers.email_controller.schedule_email',
                           side_effect=Exception("Something went wrong")):
                    response, status_code = self.controller.save_email()

        self.assertEqual(status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['error'], 'Internal Server Error')


if __name__ == '__main__':
    unittest.main()
