from pylana.modules.logs import LogsAPI
from pylana.modules.resources import ResourceAPI
from pylana.modules.dashboard import ShinyDashboardAPI


class LanaAPI2(LogsAPI, ShinyDashboardAPI, ResourceAPI):
    pass
