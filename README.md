![NetDash](docs/netdash-logo-small.png)

The NetDash project's goal is to create an interface to allow delegation of specific network management tasks to IT teams outside of a central network team. 

[![NetDash Architecture](https://docs.google.com/drawings/d/e/2PACX-1vQEr6ikrwHVAFtjBPgm5zIL8UZib4GsF8H3KgNbUxm5o9MhwRb_vgnz_gG_bUHd03ORH6RiCo2OFFCj/pub?h=800)](https://docs.google.com/drawings/d/1A859k49JQTn8-IcRoAqisa9Si5KzwJtGTJynPENe2cU/edit)

## Configuration

By default NetDash is configured to use the `netdash.settings` module. This module corresponds to the file: "src/netdash/netdash/settings.py" which is ignored in .gitignore, so isn't provided with the source. To configure the settings, copy one of the `*_example_*` files in the "src/netdash/netdash/" directory to the settings.py file. Or set the `DJANGO_SETTINGS_MODULE` environment variable to use one of the provided examples or a custom settings module.

For example:
  - `cp src/netdash/netdash/settings_example.py src/netdash/netdash/settings.py` will copy the example settings to the default location. You can modify after copying.
  - `export DJANGO_SETTINGS_MODULE=netdash.settings_example_compose` will configure NetDash to use settings suitable for the Docker Compose setup.
  - `export DJANGO_SETTINGS_MODULE=netdash.settings_env` will configure NetDash to use settings that will pull values from the environment. This is suitable for a Kuberbetes or OpenShift deployment.

## Development with [Docker Compose](https://docs.docker.com/compose/) (quickstart)

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. `export DJANGO_SETTINGS_MODULE=netdash.settings_env` (or see the Configuration section above).
4. Start the services: `docker-compose up`

This will spin up a few services:
  - NetDash instance (served at 127.0.0.1:8888)
  - NetBox instance (served at 127.0.0.1:8000)
  - Databases for both

The `netdash.settings_example_compose` module configures the NetDash instance is configured by default to use the NetBox instance as its backend.


## Development with [Pipenv](https://pipenv.readthedocs.io/)

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Create an environment with the development dependencies: `pipenv install -d`
4. Configure sample settings (see the Configuration section above).
5. Run the development server: `pipenv run python3 src/netdash/manage.py runserver`
6. Connect to the development server interface: <http://127.0.0.1:8000/>


## Development (Manual)

1. Clone this repository.
2. Change to the new directory: `cd netdash`
3. Create a virtualenv: `python3 -m venv venv`
4. Activate the environment: `source ./venv/bin/activate`
5. Install the package in editable mode: `pip install -e .`
6. Configure sample settings (see the Configuration section above).
7. Change to the project directory: `cd src/netdash`
8. Run the migrations: `python3 manage.py migrate`
9. Create an admin user: `python3 manage.py createsuperuser`
10. Run the development server: `python3 manage.py runserver`
11. Connect to the development server interface: <http://127.0.0.1:8000/>
