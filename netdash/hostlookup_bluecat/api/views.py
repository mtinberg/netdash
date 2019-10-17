from hostlookup_abstract.api.views import BaseHostView
from hostlookup_bluecat.utils import host_lookup


class HostView(BaseHostView):
    def host_lookup(self, request, q=''):
        return host_lookup(q)
