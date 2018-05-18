# pyeslog
Standard ES Logging Library


## Usage

1. Install the library by placing the following requirement in your requirements.txt
```
git+https://github.com/epidemicsound/pyeslog.git#egg=pyeslog
```

2. Import the Logger in the module
```
import eslog

logger = eslog.Logger(namespace=__name__)
```

or

```
import eslog

logger = eslog.Logger()
```

3. Start logging events.

```
logger.info("A event occured", event_name="my_event", event_type="my_event_type")
```

### Output

The logger logs directly to `stdout`. A typical log output looks like the following.
```
{"level": "info", "message": "An event occured", "timestamp": "2018-04-05T08:01:20Z", "event_name": "my_event", "event_type": "my_event_type", "namespace": "test", "service": ""}
```
The logger will automatically add `level`, `timestamp` and `service` parameters to it.


### Examples:

```
import eslog


logger = eslog.Logger(namespace='module.test', service='service.test')

# Simple Information Logging.
task_id = 'task-321422587'
logger.info("Starting with the task execution", task_id=task_id)

# OUTPUT
{"level": "info", "message": "Starting with the task execution", "timestamp": "2018-04-25T13:24:00Z", "namespace": "module.test", "service": "service.test", "task_id": "task-321422587"}

# Error Logging
error = "Internal System is Unresponsive"
logger.error("Unable to execute the call to third party service", error=error, task_id=task_id)

# OUTPUT
{"level": "error", "message": "Unable to execute the call to third party service", "timestamp": "2018-04-25T13:24:00Z", "error": "Internal System is Unresponsive", "namespace": "module.test", "service": "service.test", "task_id": "task-321422587"}


# Warning Logs
drift = 10
logger.warn("Detected a time drift indicating a possible leak in the system",
            task_id=task_id, drift=drift)

# OUTPUT
{"level": "warn", "message": "Detected a time drift indicating a possible leak in the system", "timestamp": "2018-04-25T13:24:00Z", "drift": 10, "namespace": "module.test", "service": "service.test", "task_id": "task-321422587"}
```
