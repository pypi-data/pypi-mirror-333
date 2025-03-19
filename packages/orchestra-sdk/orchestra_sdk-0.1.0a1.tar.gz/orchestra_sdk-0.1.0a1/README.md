# Orchestra Python SDK

![PyPI](https://img.shields.io/pypi/v/orchestra-sdk?label=pypi%20latest%20version)

This is a lightweight SDK that allows [Orchestra](https://www.getorchestra.io/) to interact with [Self-hosted applications (Tasks)](https://docs.getorchestra.io/docs/core-concepts/tasks/self-hosted-tasks).

The basic premise is that your self-hosted Task can send back status updates and logs to Orchestra once triggered asynchronously by Orchestra. This is done via HTTP requests.

## Installation

```bash
pip install orchestra-sdk
```

You initialise the package by creating an instance of the `OrchestraSDK` class. It requires an API key that will be used to connect with Orchestra - this can be found in [your settings page](https://app.getorchestra.io/settings/api-key). Orchestra will attempt to automatically set the other environment variables when the Task is triggered:

- `ORCHESTRA_TASK_RUN_ID`: The UUID of the Task being executed

If these are not in your environment, you can set them manually after initialising the `OrchestraSDK` class.

There are also optional configuration values:

- `send_logs`: send the contents of a log file to Orchestra, associated with the task (default = False)
- `log_file_path`: the path to the log file to send to Orchestra (default = "orchestra.log")
  - if your task is running in AWS Lambda, the log file must start with `/tmp/` to be accessible
  - [alternatively, use the `configure_aws_lambda_event` method](#aws-lambda)

```python
import os

from orchestra_sdk.orchestra import OrchestraSDK

# also: o = OrchestraSDK(api_key="os.environ.get("ORCHESTRA_API_KEY"))
orchestra = OrchestraSDK(api_key="your_api_key")

# If not set in the environment:
orchestra.task_run_id = "your_task_run_id"
```

Orchestra recommends retrieving the API key from some secret store that you have configured. If that is not possible, you can set the API key as an environment variable and read that value in your code.

## AWS Lambda

If you are using the [AWS Lambda Task](https://docs.getorchestra.io/docs/integrations/cloud-provider-integrations/aws/aws-lambda/) type from Orchestra, you can use the following helper function to ensure the correct configuration has been applied:

```python
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")

def handler(event, context):
    orchestra.configure_aws_lambda_event(event)
    # Your code here
```

This will automatically configure the `ORCHESTRA_TASK_RUN_ID` environment variable and configure the log file correctly (if `send_logs=True`).

**NOTE**: if `log_file` is set, `configure_aws_lambda_event` will override the log file path.

## Task decorator

The decorator will handle updating the Task in Orchestra automatically. It will send a `RUNNING` status update when the function is called, and then send a `SUCCEEDED` or `FAILED` status update when the function finishes.

```python
@orchestra.run()
def my_function(arg1, arg2=1):
    print("Running complex process")
```

1. The decorator will firstly read and validate the environment variables
1. It will send a `RUNNING` status update to Orchestra
1. Your function will then run
1. If an exception is raised, the decorator will send a `FAILED` status update to Orchestra
1. If the function finishes without an error being raised, regardless of the return value, the decorator will send a `SUCCEEDED` status update to Orchestra
1. If `send_logs` is enabled, the contents of the logs will also be sent.

## Updating Tasks manually

For additional control over when to update the status of the Task, or for sending messages to Orchestra, you can use the `update_task` method of the `OrchestraSDK` class.

```python
from orchestra_sdk.enum import TaskRunStatus
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")

def my_function(arg1, arg2=1):
    print("Start my complex process")
    orchestra.update_task(status=TaskRunStatus.RUNNING, message="Starting process.")

    print("Running complex process")

    fn_result = complex_process()

    if fn_result == 0:
        orchestra.update_task(status=TaskRunStatus.SUCCEEDED)
    else:
        orchestra.update_task(status=TaskRunStatus.FAILED, message="Process failed")
```

- If the function fails or throws an exception, Orchestra might not register that the Task has failed, which could have downstream consequences on your pipeline. Consider wrapping your function in a try/except block and calling `update_task` with `status=TaskRunStatus.FAILED` in the except block.

## Sending logs

To send logs associated to the Task, enable the `send_logs` flag when initialising the `OrchestraSDK` class. The logs will be sent to Orchestra when the Task finishes and the decorator is being used.

An example logging configuration is shown below:

```python
import logging
import sys

from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(
    api_key="your_api_key",
    send_logs=True,
    log_file="a.log" # for certain environments, this may need to start with "/tmp/"
)

def test_function():
    # Setup logging configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(orchestra.log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Adding handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Hello, World!")
```

## Setting outputs

To set outputs associated to the Task, use the `set_output` method of the `OrchestraSDK` class.

Output names are case-insensitive and must only contain letters, underscores (_), and hyphens (-). Numbers and spaces are not allowed.

`set_output` must be called before updating the task status to `SUCCEEDED` or `FAILED`.

```python
from orchestra_sdk.enum import TaskRunStatus
from orchestra_sdk.orchestra import OrchestraSDK

orchestra = OrchestraSDK(api_key="your_api_key")

def my_function(arg1, arg2=1):
    print("Start my complex process")
    fn_result = complex_process()
    orchestra.set_output(name='result', value=fn_result)
```

The function returns true/false for if the output was successfully set. We recommend checking the return value and logging failures to ensure outputs are correctly set.
