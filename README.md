# Pylana
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-374/)
[![Pylana](https://img.shields.io/badge/pylana-v0.0.1-orange)](https://www.python.org/downloads/release/python-374/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/lanalabs/pylana/graphs/commit-activity)

> Python API for LANA Process Mining

This package provides a Python API for [LANA Process Mining](https://www.lana-labs.com/en/). <br>
**Attention**: This package is still in alpha state. Functions and parameters may be renamed and changed at any time.

## Installation
To install pylana, you need python version 3.6.0 or above. Pylana could be installed from pypi:
```
python3 -m pip install pylana
```
To establish a connection with the server, you could use either the _access token_ or the _API key_.
```python
import pylana
myLana = pylana.LanaAPI(url = "https://cloud.lanalabs.com/", apikey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
```

## Usage Example
Pylana provides a simple interface which supports:
* Uploading / retrieving / sharing event logs
* Uploading / connecting target models
* Creating / connecting / sharing shiny dashboards
 
__Upload an Event Log__ 
```python
# without case attribute
myLana.uploadEventLog(logFile, logSemantics)

# with case attributes
myLana.uploadEventLogWithCaseAttributes(logFile, logSemantics, 
    caseAttributeFile, caseAttributeSemantics)
```

__Retrieve Event Logs__
```python
# get a list of event logs associated with the current user
myLana.getUserLogs()

# get the log id of a particular log
mylana.chooseLog(logName)
```

__Create a Shiny Dashboard__
```python
# initate a new shiny dashboard id
id = mylana.createShinyDashboard(dashboardName)

# upload the dashboard file to server
mylana.uploadShinyDashboard(dashboardFile, id)

# connect the dashboard to an event log
mylana.connectDashboardToLog(id, logId)
```
