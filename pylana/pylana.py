import requests
import pandas as pd
import json
import re
import zipfile
from os.path import basename


class LanaAPI:
    def __init__(self, url, token = None, apikey = None):

        if token:
            self.authorization_header = token
        elif apikey:
            self.authorization_header = "API-Key %s" % apikey
        else:
            raise Exception("Either api key or access token is needed for initialization")

        self.url = url

        # add schema check
        if not url.startswith('http://') or not url.startswith('https://'):
            self.url = 'http://' + self.url
        if not url.endswith('/'):
            self.url += '/'

        self.headers = {"Authorization": self.authorization_header}

        userInfoEndpoint = 'api/users/by-token'
        self.userInfo = requests.get(url=self.url + userInfoEndpoint, headers=self.headers, verify=False).json()


    """
    Logs
    """
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
                                         caseAttributeFile, caseAttributeSemantics, logName = None):

        endpoint = 'api/logs/csv-case-attributes-event-semantics'

        files = {
            'eventCSVFile': (logFile.split('/')[-1], open(logFile, 'rb'), 'text/csv'),
            'caseAttributeFile': (caseAttributeFile.split('/')[-1], open(caseAttributeFile, 'rb'), 'text/csv'),
        }

        semantics = {
            'eventSemantics': open(logSemantics).read(),
            'caseSemantics': open(caseAttributeSemantics).read(),
            'logName': logName,
            'timeZone': "Europe/Berlin"
        }

        upload_response = requests.request('POST', self.url + endpoint, headers=self.headers, files=files, data=semantics)
        
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
        shareLogWithOrgEndpoint = 'api/shareLogWithOrg/' + str(logId)
        requests.get(self.url + shareLogWithOrgEndpoint, headers=self.headers, verify=False)

    def unshareLogWithOrg(self, logId):
        unshareLogWithOrgEndpoint = 'api/unshareLogWithOrg/' + str(logId)
        requests.get(self.url + unshareLogWithOrgEndpoint, headers=self.headers, verify=False)


    """
    Models
    """
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

    """
    Shiny Dashboard
    """
    def updateDashboardUrl(self, in_file, out_file, url):
        with open(in_file, 'r+') as f:
            db_string = f.read()
            s = re.sub('lanaUrl <- \".*\"', 'lanaUrl <- ' + '"' + url + '"', db_string)

        with open(out_file, 'w') as out_file:
            out_file.write(s)


    def zipDashboard(self, zip_path, dashboard_rmd):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(dashboard_rmd, basename(dashboard_rmd))


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

    # Id arguments need to be lists
    def shareDashboard(self, dashboardId, userIds, projectIds, organizationIds):
        shareDashboardEndpoint = "api/shiny-dashboards/" + str(dashboardId)
        body = {"sharedInformation": {
            "userIds": userIds,
            "projectIds": projectIds,
            "organizationIds": organizationIds
        }}
        requests.patch(self.url + shareDashboardEndpoint, headers=self.headers, data=body, verify=False)