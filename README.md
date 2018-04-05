# pyeslog
Standard ES Logging Library


## Usage

1. Install the library directly from pip
```
pip install eslog
```

2. Import the Logger in the module
```
import eslog

logger = eslog.Logger(namespace=__name__)
```

or

```
import log

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
