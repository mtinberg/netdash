![NetDash](docs/netdash-logo-small.png)

The NetDash project's goal is to create an interface to allow delegation of specific IT infrastructure management tasks to IT teams outside of a central IT team. 

## Getting Started

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Copy the example settings to use them: `cp src/netdash/netdash/settings_example.py src/netdash/netdash/settings.py`
4. Install dependencies: `pipenv install` (if you are missing pipenv, use `brew install pipenv` or `pip install --user pipenv`)
5. Activate virtual environment to use the correct Python and installed pip packages in an isolated setting: `pipenv shell`
5. Run migrations: `python src/netdash/manage.py migrate`
6. Run the development server: `python src/netdash/manage.py runserver`

# NetDash Modules

A *NetDash Module* is a Django App that follows certain conventions and thereby integrates automatically with NetDash without any additional code changes. These integrations include UI link generation, Swagger API inclusion, routing and permissions.

NetDash Modules can be enabled by adding them to a comma-separated list in `settings.NETDASH_MODULES`. They can be specified as Django app labels or as paths to an AppConfig in [the same way that `settings.INSTALLED_APPS` is configured](https://docs.djangoproject.com/en/2.2/ref/applications/#for-application-users).

Example (`settings.py`):
```
NETDASH_MODULES = [
    'example_devices_dummy',
    'hostlookup_netdisco',
    'my_custom_nd_module',
]
```

## Creating a NetDash Module

1. Change directory to NetDash apps: `cd src/netdash`
2. Create a new NetDash Module, substituting `my_custom_nd_module` for your module's name: `python manage.py startapp --template ../../netdash_module_template my_custom_nd_module`
3. Run its initial migration: `python manage.py migrate`
4. Exclude your app from NetDash's source control, substituting `my_custom_nd_module` for your module's name: `echo src/netdash/my_custom_nd_module >> ../../.git/info/exclude`
5. Navigate into your app's directory and initialize a new git repo: `cd my_custom_nd_module; git init`
6. To try your new module, add your module's name to `NETDASH_MODULES` as shown in the previous section and run the development server.

## Conventions

* A module with `urls.py` should declare an `app_name`.
* A module with `urls.py` will have its URLs placed under `/<app_name>/*`.
* A module with a url named `index` in its `urls.py` will have a link to `index` generated in the NetDash navbar.
* A module that generates a permission named `can_view_module` will only generate an `index` link in the NetDash navbar for users who have that permission.
* A module with `api/urls.py` should declare an `app_name`. If the module also has a `urls.py`, it should reuse the previous `app_name` like so: `<app_name>-api`
* A module with `api/urls.py` will have its API URLs placed under `/api/<app_name>/*`.

Check under `apps_dev` for examples of these conventions.

## Troubleshooting

If a NetDash Module doesn't properly follow conventions, certain integrations might not work. NetDash includes a `diagnose` command to output information about your NetDash Modules that may assist in refactoring them for inclusion in NetDash.

```
python src/netdash/manage.py diagnose -v2
```

Will output diagnostics for all NetDash Modules, including any exception traces (`-v2` flag).

If an unrecoverable error is encountered while parsing NetDash Modules, all diagnostics up until the error will be displayed.
