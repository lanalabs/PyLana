import requests
import pandas as pd
import json
import re
import zipfile
from os.path import basename


class LanaAPI:
    def __init__(self, token, url):
        self.token = token
        self.url = url

        # add schema check
        if not url.startswith('http://') or not url.startswith('https://'):
            self.url = 'http://' + self.url
        if not url.endswith('/'):
            self.url += '/'

        self.headers = {"Authorization": self.token}

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
                                         caseAttributeFile, caseAttributeSemantics):

        # import requests

        # url = "http://localhost:4000/api/logs/csv-case-attributes-event-semantics"

        # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"eventCSVFile\"; filename=\"daimler-FWS-current.csv\"\r\nContent-Type: text/csv\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"logName\"\r\n\r\nIncident Management\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"eventSemantics\"\r\n\r\n\n [\n   \n {\n    \"name\": \"CaseId\",\n    \"semantic\": \"Case ID\",\n    \"format\": null\n },\n  {\n    \"name\": \"Action\",\n    \"semantic\": \"Action\",\n    \"format\": null\n  },\n  {\n    \"name\": \"Start\",\n    \"semantic\": \"Start\",\n    \"format\": \"yyyy-MM-dd HH:mm:ss.SSS\"\n  }\n , {\n    \"name\": \"Complete\",\n    \"semantic\": \"Complete\",\n    \"format\": \"yyyy-MM-dd HH:mm:ss.SSS\"\n }\n   ,\n {\n    \"name\": \"duration\",\n    \"semantic\": \"NumericAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"PO\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"execstate local\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"execstate maxretry\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"execstate nested\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"execstate reason\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"result local\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"result nested\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 1 errorid\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 1 errortext\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 1 flag\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 1 trblcode\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 2 errorid\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 2 errortext\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 2 flag\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgerror 2 trblcode\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"tgname\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 1 ecunamenisp\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 1 errorid\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 1 errortext\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 1 flag\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 1 trblcode\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 2 ecunamenisp\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 2 errorid\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 2 errortext\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 2 flag\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"usererror 2 trblcode\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }\n  ]\n     \r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"caseAttributeFile\"; filename=\"daimler-FWS-current-caseAttributes.csv\"\r\nContent-Type: text/csv\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"caseSemantics\"\r\n\r\n\n [\n   {\n     \"name\": \"CaseId\",\n     \"semantic\": \"Case ID\",\n     \"format\": null\n   }\n   ,\n {\n    \"name\": \"Fehleranzahl\",\n    \"semantic\": \"NumericAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Antrieb\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Aufbauvariante\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"AuftrittsPO\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Baumuster\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Baureihe\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Fehlertyp\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Fehlerursache\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Getriebetyp\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Kraftstoff\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Lenkervariante\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Motortyp\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"Zylinder\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"all_testgroups_IO\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"erfassungszeit_s_dat_u_zeit\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"erfassungszeit_u_dat_u_zeit\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"fehlerart_u\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"fehlerort_u\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"folgefehler\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"is_fehlercode\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"is_fehlertext\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"na_kzn\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"prodno\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }, \n {\n    \"name\": \"vin\",\n    \"semantic\": \"CategorialAttribute\",\n    \"format\": null\n }\n ]\n     \r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"timeZone\"\r\n\r\nEurope/Berlin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        # headers = {
        #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        #     'Content-Type': "application/x-www-form-urlencoded",
        #     'Authorization': "API-Key 3e18d628a34a4afaba3058af34275ccc",
        #     'User-Agent': "PostmanRuntime/7.16.3",
        #     'Accept': "*/*",
        #     'Cache-Control': "no-cache",
        #     'Postman-Token': "f83270c8-060d-47e4-94f4-800948f00b67,19cc30e8-31a1-47a9-9242-a4e38cd11d1b",
        #     'Host': "localhost:4000",
        #     'Accept-Encoding': "gzip, deflate",
        #     'Content-Length': "591868",
        #     'Connection': "keep-alive",
        #     'cache-control': "no-cache"
        #     }

        # response = requests.request("POST", url, data=payload, headers=headers)
        endpoint = 'api/logs/csv-case-attributes-event-semantics'

        files = {
            'eventCSVFile': (logFile.split('/')[-1], open(logFile, 'rb'), 'text/csv'),
            'caseAttributeFile': (caseAttributeFile.split('/')[-1], open(caseAttributeFile, 'rb'), 'text/csv'),
        }

        semantics = {
            'eventSemantics': open(logSemantics).read(),
            'caseSemantics': open(caseAttributeSemantics).read(),
            'logName': "Incident Management",
            'timeZone': "Europe/Berlin"
        }

        new_header = dict(self.headers)
        upload_response = requests.request('POST', self.url + endpoint, headers=new_header, files=files, data=semantics)
        print(requests.Request('POST', self.url + endpoint, headers=new_header, files=files, data=semantics).prepare().body.decode('ascii'))
        
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
        res = requests.post(self.url + uploadShinyEndpoint, headers=self.headers, files=file, verify=False)
        return res

    def connectDashboardToLog(self, dashboardId, logId):
        connectDashboardToLogEndpoint = "api/logs/" + str(logId) + "/shiny-dashboard/" + str(dashboardId)
        res = requests.post(self.url + connectDashboardToLogEndpoint, headers=self.headers, verify=False)
        return res

    # Id arguments need to be lists
    def shareDashboard(self, dashboardId, userIds, projectIds, organizationIds):
        shareDashboardEndpoint = "api/shiny-dashboards/" + str(dashboardId)
        body = {"sharedInformation": {
            "userIds": userIds,
            "projectIds": projectIds,
            "organizationIds": organizationIds
        }}
        requests.patch(self.url + shareDashboardEndpoint, headers=self.headers, data=body, verify=False)