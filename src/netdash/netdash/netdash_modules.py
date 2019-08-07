from importlib import import_module
from django.conf.urls import url, include, re_path


class NetdashModule():
    app_label = ''
    app_name = ''
    ui_app_urls: url
    api_app_urls: url

    def _get_app_name(self, app_label):

        try:
            module = import_module(f'{app_label}.urls')
        except ModuleNotFoundError:
            print(f'Failed to import urls.py for module: {app_label}')

            try:
                module = import_module(f'{app_label}.api.urls')
            except ModuleNotFoundError:
                print(f'Failed to import both urls.py and api/urls.py for module: {app_label}')
            else:
                print('api module has been imported')

        if hasattr(module, 'app_name'):
            if module.app_name.endswith('-api'):
                return module.app_name.replace('-api', '')
            return module.app_name
        return app_label

    def _get_ui_urls(self, slug, app_label):
        app_name = self.app_name
        try:
            import_module(f'{app_label}.urls')
            return re_path(r'^' + slug + '/', include(f'{app_label}.urls', namespace=slug))
        except ModuleNotFoundError:
            return []

    def _get_api_urls(self, slug, app_label):
        app_name = self.app_name
        try:
            import_module(f'{app_label}.api.urls')
            return re_path(r'^' + slug + '/', include(f'{app_label}.api.urls', namespace=slug))
        except ModuleNotFoundError:
            return []

    def _get_app_urls(self, app_name, app_label):
        slug = app_name
        return self._get_ui_urls(slug, app_label), self._get_api_urls(slug, app_label)

    def __init__(self, app_label):
        self.app_label = app_label
        self.app_name = self._get_app_name(self.app_label)
        self.ui_app_urls, self.api_app_urls = self._get_app_urls(self.app_name, self.app_label)
