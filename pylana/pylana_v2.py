from pylana.modules.logs import LogsAPI
from pylana.modules.resources import ResourceAPI
from pylana.modules.shiny_dashboards import ShinyDashboardAPI


class LanaAPI2(LogsAPI, ShinyDashboardAPI, ResourceAPI):
    pass
