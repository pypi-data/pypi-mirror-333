```python
from telemetry import register_log
import os

# Change as needed
os.environ['LOGGER_URL'] = 'http://127.0.0.1:8000'
os.environ['LOGGER_TOKEN'] = '1234567890'
os.environ['LOGGER_APPLICATION_NAMESPACE'] = 'ABCD'

register_log(
    timestamp='2023-03-01T00:00:00.000Z',
    error='Error message',
    func_name='function_name',
    filename='filename.py',
    line_no=10,
    detailed_exp='detailed explanation',
    custom_msg='custom message',
    params='parameters'
)
```