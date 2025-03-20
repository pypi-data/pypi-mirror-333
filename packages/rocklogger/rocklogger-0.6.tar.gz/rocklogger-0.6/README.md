# rocklogger

A simple and flexible logging utility for Python applications with singleton pattern support.

### PyPI
https://pypi.org/project/rocklogger/

## Installation

```bash
pip install rocklogger
```

## Usage

### Basic Usage

```python
from rocklogger import Rocklogger

# Initialize the logger using the singleton pattern
# level can be 'info', 'debug', 'warning', or 'error'
logger = Rocklogger.get_instance(level='debug', use_date_in_filename=True).get_logger()

# Log messages at different levels
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
```

### Log Files

The logger creates two log files in a 'logs' directory in the same location as your script:
1. `your_script_name_YYYYMMDD.log` - Contains all log messages
2. `your_script_name_error_YYYYMMDD.log` - Contains only error level messages

If `use_date_in_filename` is set to `False`, the date will not be included in the filename.

### Logging Exceptions

```python
try:
    # Some code that might raise an exception
    result = 10 / 0
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
```

### Singleton Pattern

Rocklogger implements the singleton pattern, ensuring that only one logger instance exists across your application:

```python
# In your main script
from rocklogger import Rocklogger
logger = Rocklogger.get_instance(level='debug').get_logger()

# In another module
from rocklogger import Rocklogger
# This will use the same instance created in the main script
logger = Rocklogger.get_instance().get_logger()
```

Benefits:
- Ensures consistent logging configuration across your application
- Log files are named after the script that first created the logger
- Prevents multiple log file handlers from being created

#### Important Note About Process Isolation

The singleton pattern works within a single Python process. When modules are imported within the same process, they will share the same logger instance:

```python
# main.py
from rocklogger import Rocklogger
logger = Rocklogger.get_instance(level='debug').get_logger()
logger.info('Main script')

import module_a  # Will use the same logger instance
import module_b  # Will also use the same logger instance
```

However, if you run separate Python scripts as independent processes, each process will have its own singleton instance:

```bash
# These will create separate logger instances
python script1.py
python script2.py
```

For applications with multiple entry points, consider creating a central logging module that's imported by all other modules.

### Closing the Logger

When you're done with the logger, you can close it (optional):

```python
# This is automatically done when the Rocklogger instance is garbage collected
logger.close()
```

### Resetting the Logger (for testing)

If you need to reset the logger (mainly for testing purposes):

```python
Rocklogger.reset()
```
