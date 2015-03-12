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

import json
import logging

import boto.logs
from boto.logs.exceptions import (DataAlreadyAcceptedException,
                                  InvalidSequenceTokenException,
                                  ResourceAlreadyExistsException)


class CloudWatchLogsHandler(logging.StreamHandler):
    """
    Logging Handler writing to the AWS CloudWatch Logs Service, directly

    Needed Information:
        region (e.g. "eu-central-1")
        log_group_name
        log_stream_name

    Dependencies:
        boto: python library for the AWS API, see
            http://docs.pythonboto.org/en/latest/getting_started.html#installing-boto
        boto credentials, see
            http://docs.pythonboto.org/en/latest/getting_started.html#configuring-boto-credentials)

    Typical Usage:
        from cloudwatchlogs_logger import CloudWatchLogsHandler
        cwl_handler = CloudWatchLogsHandler(AWS_REGION, GROUP_NAME, STREAM_NAME)

        logger = logging.getLogger(LOGGER_NAME)
        logger.addHandler(cloudwatch_handler)
        logger.warn("Tadahhh")
    """
    def __init__(self, region, log_group_name, log_stream_name, level=logging.INFO):
        logging.StreamHandler.__init__(self)
        self.setLevel(level)
        self.region = region
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.connection = None
        self.sequence_token = None

    def create_group_and_stream(self, log_group_name, log_stream_name):
        try:
            self.connection.create_log_group(log_group_name)
        except ResourceAlreadyExistsException:
            pass
        try:
            self.connection.create_log_stream(log_group_name, log_stream_name)
        except ResourceAlreadyExistsException:
            pass

    def _lazy_connect(self):
        if self.connection:
            return
        self.connection = boto.logs.connect_to_region(self.region)
        self.create_group_and_stream(self.log_group_name, self.log_stream_name)

    def _put_message(self, message, timestamp):
        self._lazy_connect()
        event = {"message": message, "timestamp": timestamp}
        result = self.connection.put_log_events(
            self.log_group_name,
            self.log_stream_name,
            [event],
            self.sequence_token)
        self.sequence_token = result.get("nextSequenceToken", None)

    def put_message(self, message, timestamp):
        try:
            self._put_message(message, timestamp)
        except (DataAlreadyAcceptedException, InvalidSequenceTokenException) as exc:
            if exc.status != 400:
                raise
            next_sequence_token = exc.body.get("expectedSequenceToken", None)
            if next_sequence_token:
                self.sequence_token = next_sequence_token
                self._put_message(message, timestamp)
            else:
                raise

    def emit(self, record):
        timestamp = int(record.created * 1000)
        message = json.dumps(vars(record))
        self.put_message(message, timestamp)
