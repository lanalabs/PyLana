import requests

class LanaAPI:
    def __init__(self, token, url):
        self.token = token
        self.url = url

        self.headers = {"Authorization": self.token}

        userInfoEndpoint = 'api/users/by-token'

        self.userInfo = requests.get(url=self.url+userInfoEndpoint, headers=self.headers, verify=False).json()
    
    def uploadEventLog(self, logFile, logSemantics):
        endpoint = 'api/logs/csv'

        file = {
            'file': open(logFile, 'rb'),
        }

        semantics = {
            'eventSemantics': open(logSemantics).read(),
        }

        r = requests.post(self.url+endpoint, headers=self.headers, files=file, data=semantics)
        return r

    
    def uploadEventLogWithCaseAttributes(self, logFile, logSemantics, 
    caseAttributeFile, caseAttributeSemantics):
        endpoint = 'api/uploadEventLogWithCaseAttributes'

        files = {
            'eventCSVFile': open(logFile, 'rb'),
            'caseAttributeFile': open(caseAttributeFile, 'rb'),
        }

        semantics = {
            'eventSemantics': open(logSemantics).read(),
            'caseSemantics': open(caseAttributeSemantics).read()
        }

        requests.post(self.url+endpoint, headers=self.headers, files=files, data=semantics, verify=False)

    def getUserLogs(self):
        userLogsEndpoint = 'api/users/' + str(self.userInfo['id']) + '/logs'
        userLogs = requests.get(url=self.url+userLogsEndpoint, headers=self.headers, verify=False).json()
        return userLogs

    def chooseLog(self, logName):
        userLogs = self.getUserLogs()
        logId = max([x['id'] for x in userLogs if x['name'] == logName])
        return logId

    def appendEvents(self, logId, logFile, logSemantics):
        appendEventsEndpoint = 'api/logs/' + str(logId) + '/csv'    
        file = {'eventCSVFile': open(logFile, 'rb')}
        semantics = {'eventSemantics': open(logSemantics).read()}

        requests.post(self.url+appendEventsEndpoint, headers=self.headers, files=file, data=semantics, verify=False)

    def appendAttributes(self, logId, caseAttributeFile, caseAttributeSemantics):
        appendEventsEndpoint = 'api/logs/' + str(logId) + '/csv-case-attributes'
        file = {'caseAttributeFile': open(caseAttributeFile, 'rb')}
        semantics = {'caseSemantics': open(caseAttributeSemantics).read()}

        requests.post(self.url+appendEventsEndpoint, headers=self.headers, files=file, data=semantics, verify=False)

    def shareLogWithOrg(self, logId):
        appendEventsEndpoint = 'api/shareLogWithOrg/' + str(logId)
        requests.get(self.url+appendEventsEndpoint, headers=self.headers, verify=False)

    def unshareLogWithOrg(self, logId):
        appendEventsEndpoint = 'api/unshareLogWithOrg/' + str(logId)
        requests.get(self.url+appendEventsEndpoint, headers=self.headers, verify=False)
