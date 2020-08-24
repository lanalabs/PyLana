# PyLana
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg
)](https://www.python.org/downloads/release/python-374/)
[![Pylana](https://img.shields.io/badge/pylana-v0.1.0-blue)](https://pypi.org/project/pylana/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/lanalabs/pylana/graphs/commit-activity)

PyLana is Python API for [LANA Process Mining](https://lanalabs.com/). It focuses on resource management, but provides methods that can be used to access the processed data as well.

This package is still in initial development state. Anything may change at any time. The public API should not be considered stable.

## Installation

You can install PyLana directly from PyPi with e.g. 

```bash
$ pip install pylana
```

# How to get started

To connect with an api at e.g. 'https:://cloud-backend.lanalabs.com', first create an API with

```python
from pylana import create_api

api = create_api('https', 'cloud-backend.lanalabs.com', <API Key>)
```

You will require an API key that is valid for your LANA deployment. The returned api stores the url for a LANA Process Mining api as well as your authentication. After creation you can us it to manage the LANA process mining resources. Among other things you can upload data from python pandas data frames directly or connect logs and shiny dashboard resources referencing them by their names.

To upload a new log called "new-event-log" and shiny-dashboard named "new-shiny-dashboard", and connect them with each other, you can use the following code

```python
upload_response = api.upload_event_log_df(
                            'new-event-log', df_event_log,
                            time_format='YYYY-mm-dd',
                            df_case=df_case_attributes)
shiny_dashboard = api.create_shiny_dashboard('new-shiny-dashboard')
connection_response = api.connect_shiny_dashboard(
                                upload_response.json()['id'],
                                shiny_dashboard['id'])
```

We also provide basic methods for direct http requests to LANA API endpoints, for example

```python
response_list = api.get('/api/v2/dashboards')
```

will return a response with a list of dashboard metadata. For details about the endpoints refer to the swagger documentation of the LANA API.

# How to contribute

See the details in [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[Apache License 2.0](http://www.apache.org/licenses/)

