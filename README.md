# python-cloudwatchlogs-logging
Logging Handler for easy logging to AWS CloudWatchLogs.

```
from cloudwatchlogs_logger import CloudWatchLogsHandler
cwl_handler = CloudWatchLogsHandler(AWS_REGION, GROUP_NAME, STREAM_NAME)

logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(cloudwatch_handler)
logger.warn("Tadahhh")
```

