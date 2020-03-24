"""
lana combined api
"""

from pylana.logs import LogsAPI
from pylana.resources import ResourceAPI
from pylana.shiny_dashboards import ShinyDashboardAPI


class LanaAPI2(LogsAPI, ShinyDashboardAPI, ResourceAPI):
    pass
