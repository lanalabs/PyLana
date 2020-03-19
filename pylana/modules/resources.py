from pylana.modules.api import API


class ResourceAPI(API):

    def connect_resources(self, dct):
        return self.post('/api/v2/resource-connections',  json=dct)

    def connect_model(self, log_id, model_id):
        dct = {'log_id': log_id, 'model_id': model_id}
        return self.connect_resources(dct)

    def connect_dashboard(self, log_id, dashboard_id):
        dct = {'log_id': log_id, 'dashboard_id': dashboard_id}
        return self.connect_resources(dct)

    def connect_shiny_dashboard(self, log_id, shiny_dashboard_id):
        dct = {'log_id': log_id, 'shiny_dashboard_id': shiny_dashboard_id}
        return self.connect_resources(dct)

    def connect_working_schedule(self, log_id, working_schedule_id):
        dct = {'log_id': log_id, 'working_schedule_id': working_schedule_id}
        return self.connect_resources(dct)
