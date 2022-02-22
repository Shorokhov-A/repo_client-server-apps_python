import sys
import os
from unittest import TestCase
from unittest.mock import patch
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message
from common.variables import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE_DEFAULT_IP_ADDRESS


class TestServer(TestCase):
    error_dict = {
        RESPONSE_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad request',
    }
    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
        self.assertEqual(
            process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
            self.ok_dict
        )

    def test_no_action(self):
        self.assertEqual(process_client_message({TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_wrong_action(self):
        self.assertEqual(
            process_client_message({ACTION: 'Wrong', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
            self.error_dict
        )

    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_no_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1}), self.error_dict)

    def test_unknown_user(self):
        self.assertEqual(
            process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'USER'}}),
            self.error_dict
        )
