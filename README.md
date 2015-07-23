# python-cloudwatchlogs-logging

[![Build Status](https://travis-ci.org/ImmobilienScout24/python-cloudwatchlogs-logging.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/python-cloudwatchlogs-logging)
[![Coverage Status](https://coveralls.io/repos/ImmobilienScout24/python-cloudwatchlogs-logging/badge.svg)](https://coveralls.io/r/ImmobilienScout24/python-cloudwatchlogs-logging)
[![Codacy Badge](https://www.codacy.com/project/badge/c86ebfb675ba4747bb4b58303285bd4b)](https://www.codacy.com/public/arnehilmann/python-cloudwatchlogs-logging)

**_Currently under construction._**

Logging Handler for easy logging to AWS CloudWatchLogs.

## Example
```
import logging
from cloudwatchlogs_logging import CloudWatchLogsHandler

cwl_handler = CloudWatchLogsHandler(AWS_REGION, GROUP_NAME, STREAM_NAME)
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(cwl_handler)
logger.warn("Tadahhh")
```

## Prerequisites
- [Boto SDK](http://docs.pythonboto.org/en/latest/getting_started.html)
- [AWS Credentials for Boto](http://docs.pythonboto.org/en/latest/boto_config_tut.html#credentials)

## Licensing
python-cloudwatchlogs-logging is licensed under [Apache License, Version 2.0](https://github.com/ImmobilienScout24/python-cloudwatchlogs-logging/blob/master/LICENSE).

