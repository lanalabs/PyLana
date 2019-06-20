import requests
import pandas as pd
import json


class LanaAPI:
    def __init__(self, token, url):
        self.token = token
        self.url = url

        self.headers = {"Authorization": self.token}

        userInfoEndpoint = 'api/users/by-token'

        self.userInfo = requests.get(url=self.url + userInfoEndpoint, headers=self.headers, verify=False).json()

    def uploadEventLog(self, logFile, logSemantics):
        endpoint = 'api/logs/csv'

        file = {
            'file': open(logFile, 'rb'),
        }

        semantics = {
            'eventSemantics': open(logSemantics).read(),
        }

        r = requests.post(self.url + endpoint, headers=self.headers, files=file, data=semantics)
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

        upload_response = requests.post(self.url + endpoint, headers=self.headers, files=files,
                                        data=semantics, verify=False).json()
        return upload_response

    def getUserLogs(self):
        userLogsEndpoint = 'api/users/' + str(self.userInfo['id']) + '/logs'
        userLogs = requests.get(url=self.url + userLogsEndpoint, headers=self.headers, verify=False).json()
        return userLogs

    def chooseLog(self, logName):
        userLogs = self.getUserLogs()
        logId = max([x['id'] for x in userLogs if x['name'] == logName])
        return logId

    def appendEvents(self, logId, logFile, logSemantics):
        appendEventsEndpoint = 'api/logs/' + str(logId) + '/csv'
        file = {'eventCSVFile': open(logFile, 'rb')}
        semantics = {'eventSemantics': open(logSemantics).read()}

        requests.post(self.url + appendEventsEndpoint, headers=self.headers, files=file, data=semantics, verify=False)

    def appendAttributes(self, logId, caseAttributeFile, caseAttributeSemantics):
        appendEventsEndpoint = 'api/logs/' + str(logId) + '/csv-case-attributes'
        file = {'caseAttributeFile': open(caseAttributeFile, 'rb')}
        semantics = {'caseSemantics': open(caseAttributeSemantics).read()}

        requests.post(self.url + appendEventsEndpoint, headers=self.headers, files=file, data=semantics, verify=False)

    def shareLogWithOrg(self, logId):
        appendEventsEndpoint = 'api/shareLogWithOrg/' + str(logId)
        requests.get(self.url + appendEventsEndpoint, headers=self.headers, verify=False)

    def unshareLogWithOrg(self, logId):
        appendEventsEndpoint = 'api/unshareLogWithOrg/' + str(logId)
        requests.get(self.url + appendEventsEndpoint, headers=self.headers, verify=False)

    def uploadTargetModel(self, targetModel, modelName):
        uploadModelEndpoint = "api/process-models"
        file = {'file': open(targetModel, 'rb')}
        data = {'fileName': modelName}
        model_response = requests.post(self.url + uploadModelEndpoint, files=file, data=data,
                                       headers=self.headers, verify=False).json()
        return model_response

    def connectModelToLog(self, logId, modelId):
        connectModelToLogEndpoint = "api/addLogModelMapping"
        json = {"name": str(modelId) + "_" + str(logId), "bpmnFileId": modelId, "logId": logId}
        r = requests.post(self.url + connectModelToLogEndpoint, json=json, headers=self.headers, verify=False)
        modelMappingId = r.text
        return modelMappingId

    def addEventActivityMapping(self, logId, modelId, modelMappingId):
        eventClassesEndpoint = "api/eventClasses"
        activitiesEndpoint = "api/activities"
        mappingEndpoint = "api/addActivityEventMappings"

        activities = requests.get(self.url + activitiesEndpoint + str(modelId), headers=self.headers, verify=False)
        event = requests.get(self.url + eventClassesEndpoint + str(logId), headers=self.headers, verify=False)

        act_json = json.loads(activities.text)
        evt_json = json.loads(event.text)
        joint = set(act_json).intersection(evt_json)

        mapping_id = [modelMappingId] * len(joint)

        df = pd.DataFrame([])
        df['logModelMappingId'] = mapping_id
        df.logModelMappingId = pd.to_numeric(df.logModelMappingId, errors='coerce')
        df['eventClass'] = joint
        df['activity'] = joint

        mapping_json = df.to_json(orient='records')
        mapping_json = json.loads(mapping_json)

        requests.post(self.url + mappingEndpoint, headers=self.headers, json=mapping_json, verify=False)

    def createShinyDashboard(self, dashboardName):
        createDashboardEndpoint = "api/shiny-dashboards"
        body = {"name": dashboardName}
        r = requests.post(self.url + createDashboardEndpoint, headers=self.headers, json=body, verify=False)
        r_json = json.loads(r.text)
        dashboardId = r_json['id']
        return dashboardId

    def uploadShinyDashboard(self, dashboard, dashboardId):
        uploadShinyEndpoint = "api/shiny-dashboards/" + str(dashboardId) + "/source"
        file = {'file': open(dashboard, 'rb')}
        requests.post(self.url + uploadShinyEndpoint, headers=self.headers, files=file, verify=False)

    def connectDashboardToLog(self, dashboardId, logId):
        connectDashboardToLogEndpoint = "api/logs/" + str(logId) + "/shiny-dashboard/" + str(dashboardId)
        requests.post(self.url + connectDashboardToLogEndpoint, headers=self.headers, verify=False)