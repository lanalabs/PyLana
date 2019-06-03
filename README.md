# pylana - R API for LANA Process Mining
This package provides an R API for [LANA Process Mining](https://www.lana-labs.com/en/). 

**Attention**: This package is still in alpha state. Functions and parameters may be renamed and changed at any time.

# Usage
After you clone the repository you need to import the pylana package. Create a new e.g. python file and import the pylana as follows:

```
import pylana
```

After importing the package, an initialization is needed. Create your own object with the URL (for on-premise the localhost and for cloud the respective cloud-URL). Example following.

```
myLana = pylana.LanaAPI("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "https://cloud.lanalabs.com/")
```

## Upload an Event Log without case attributes

```
myLana.uploadEventLog(logFile, logSemantics)
```

## Upload an Event Log with case attributes

```
myLana.uploadEventLogWithCaseAttributes(logFile, logSemantics, 
    caseAttributeFile, caseAttributeSemantics)
```

## Get User Logs

```
myLana.getUserLogs()
```

## Choose Log

```
myLana.chooseLog(logName)
```

## Append Events

```
myLana.appendEvents(logId, logFile, logSemantics)
```

## Append Attributes

```
myLana.appendAttributes(logId, caseAttributeFile, caseAttributeSemantics)
```

## Share Log with Organization

```
myLana.shareLogWithOrg(logId)
```

## Unshare Log with Organization

```
myLana.unshareLogWithOrg(logId)
```
