import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from http import HTTPStatus

from marshmallow import ValidationError

from app.controllers.event_controller import EventController

class TestEventController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.controller = EventController()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.schemas.event.EventSchema.load')
    @patch('app.database.db.session.get')
    def test_create_event_success(self, mock_db_get, mock_load):
        """
        Test the create_event method for a successful case.
        """
        test_json_data = {
            "event_name": "Pycon 2024",
            "event_description": "Python event indonesia 2024",
            "event_date": "2024-12-12T15:25:30Z"
        }

        mock_load.return_value = test_json_data
        mock_event = MagicMock()
        mock_db_get.return_value = mock_event

        mock_event_instance = MagicMock()
        mock_event = MagicMock()

        with self.app.test_request_context(json=test_json_data):
            with patch('app.controllers.event_controller.EventInterface',
                       return_value=mock_event_instance) as mock_event_interface:
                with patch('app.controllers.event_controller.create_event',
                           return_value=mock_event) as mock_create_event:
                    response, status_code = self.controller.create_event()

        self.assertEqual(status_code, HTTPStatus.CREATED)

        expected_response = {
            'status': 'success',
            'message': 'Create event successfully',
            'data': None,
            'error': None
        }
        self.assertEqual(response.json, expected_response)

        mock_event_interface.assert_called_once_with(
            event_name="Pycon 2024",
            event_description="Python event indonesia 2024",
            event_date="2024-12-12T15:25:30Z"
        )
        mock_create_event.assert_called_once_with(mock_event_instance)

    @patch('app.schemas.event.EventSchema.load')
    @patch('app.database.db.session.get')
    def test_create_event_validation_error(self, mock_db_get, mock_load):
        """
        Test the create_event method for validation error.
        """
        test_json_data = {
            "event_name": "Pycon 2024",
            "event_description": "Python event indonesia 2024",
            "event_date": "2024-12-12T15:25:30Z"
        }

        mock_load.side_effect = ValidationError("Validation Error")

        with self.app.test_request_context(json=test_json_data):
            response, status_code = self.controller.create_event()

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json['error'], 'Validation Error')

if __name__ == '__main__':
    unittest.main()