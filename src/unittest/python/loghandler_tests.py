# CloudWatchLogs Logging
# Copyright 2015 Immobilien Scout GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import boto.logs.exceptions
import unittest
from mock import patch
from cloudwatchlogs_logging import CloudWatchLogsHandler


class CloudWatchLogsHandlerTest(unittest.TestCase):

    def setUp(self):
        self.boto_mock = patch("cloudwatchlogs_logging.boto").start()
        self.connection = self.boto_mock.logs.connect_to_region.return_value
        self.logger = logging.getLogger("Test")
        self.logger.setLevel(logging.WARN)

    def myAssertIn(self, a, b):
        self.assertTrue(a in b)

    def test_cloudwatch_logging(self):
        cloudwatch_handler = CloudWatchLogsHandler("foo-region", "foo-group", "test")
        self.logger.addHandler(cloudwatch_handler)

        self.logger.debug("aha")
        self.logger.info("aha")
        self.assertFalse(self.connection.put_log_events.called)

        self.logger.warn("aha")

        self.connection.create_log_group.assert_called_with("foo-group")
        self.connection.create_log_stream.assert_called_with("foo-group", "test")
        call_args = self.connection.put_log_events.call_args[0]
        self.assertEqual("foo-group", call_args[0])
        self.assertEqual("test", call_args[1])
        log_event = call_args[2][0]
        self.myAssertIn("timestamp", log_event)
        self.myAssertIn("message", log_event)
        self.myAssertIn("WARNING", log_event["message"])
        self.myAssertIn("aha", log_event["message"])

    def test_cloudwatch_logging_exception_logging(self):
        cloudwatch_handler = CloudWatchLogsHandler("foo-region", "foo-group", "test")
        self.logger.addHandler(cloudwatch_handler)

        try:
            1 / 0
        except Exception:
            self.logger.exception("Cannot divide by zero:")

    def test_log_group_already_exists(self):
        e = boto.logs.exceptions.ResourceAlreadyExistsException(400, "binschonda")
        self.connection.create_log_group.side_effect = e
        self.connection.create_log_stream.side_effect = e
        CloudWatchLogsHandler("foo-region", "foo-group", "test")

    def test_response_with_invalid_sequence_token(self):
        e = boto.logs.exceptions.InvalidSequenceTokenException(400, "foo")
        e.body = {"expectedSequenceToken": "correct_token"}
        self.connection.put_log_events.side_effect = e

        handler = CloudWatchLogsHandler("foo-region", "foo-group", "test")
        self.assertRaises(boto.logs.exceptions.InvalidSequenceTokenException,
                          handler.put_message, "message", "timestamp")

    def test_invalid_response(self):
        e = boto.logs.exceptions.InvalidSequenceTokenException(500, "completelybroken")
        self.connection.put_log_events.side_effect = e

        handler = CloudWatchLogsHandler("foo-region", "foo-group", "test")
        self.assertRaises(boto.logs.exceptions.InvalidSequenceTokenException,
                          handler.put_message, "message", "timestamp")

    def test_response_with_missing_sequence_token(self):
        e = boto.logs.exceptions.InvalidSequenceTokenException(400, "foo")
        e.body = {}
        self.connection.put_log_events.side_effect = e

        handler = CloudWatchLogsHandler("foo-region", "foo-group", "test")
        self.assertRaises(boto.logs.exceptions.InvalidSequenceTokenException,
                          handler.put_message, "message", "timestamp")
