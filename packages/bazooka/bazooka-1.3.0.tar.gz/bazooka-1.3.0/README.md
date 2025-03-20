Bazooka - reliable HTTP client
==============================

![tests workflow](https://github.com/infraguys/bazooka/actions/workflows/tests.yaml/badge.svg)

Overview
--------

Bazooka is a reliable and efficient HTTP client for Python that provides
features such as retries out of the box, full compatibility with the
`requests` library, and customizable logging options.

Key Features
------------

*   **retries**: Bazooka includes built-in retry logic to handle temporary network failures or 5XX server errors.
*   **full compatibility**: Bazooka is designed to work seamlessly with the `requests` library, allowing for easy integration into existing projects.
*   **explicit automatic error handling**: by default client raises exception if status code isn't 2xx.
*   **curl-like customizable Logging**: Bazooka offers flexible logging options, including duration logging and sensitive logging support.

Example Usage
-------------

### Basic Example

```python
import bazooka

client = bazooka.Client()
print(client.get('http://example.com').json())
```

### Using Correlation IDs

(Usable to match bazooka requests with your business logic logs)

```python
from bazooka import correlation

client = bazooka.Client(correlation_id='my_correlation_id')
print(client.get('http://example.com').json())
```

### Raised Exceptions on 4xx Errors

```python
import bazooka
from bazooka import exceptions

client = bazooka.Client()

try:
    response = client.get('http://example.com', timeout=10)
except exceptions.NotFoundError:
    # process 404 error
    pass
except exceptions.ConflictError:
   # process 409 error
    pass
except exceptions.BaseHTTPException as e:
   # process other HTTP errors
    if e.code in range(400, 500):
        print(f"4xx Error: {e}")
    else:
        raise
```

Getting Started
---------------

To get started with Bazooka, install it via pip:

```bash
pip install bazooka
```
