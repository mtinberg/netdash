import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from netdash_devices_netbox_api.utils import get_device, get_devices


class DeviceList(TemplateView):
    template_name = 'device-list.html'

    def __init__(self, *args, **kwargs):
        if not settings.NETBOX_API_URL:
            raise ImproperlyConfigured('NETBOX_API_URL to use netdash_devices_netbox_api')
        self.URL = settings.NETBOX_API_URL.lstrip('/')
        super().__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['devices'] = get_devices(self.URL)
        return context
