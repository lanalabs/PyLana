"""
lana combined api
"""

from pylana.logs import LogsAPI
from pylana.resources import ResourceAPI
from pylana.shiny_dashboards import ShinyDashboardAPI


class LanaAPI2(LogsAPI, ShinyDashboardAPI, ResourceAPI):
    """
    lana api

    allows programmatic management of lana resources
    """
    pass
