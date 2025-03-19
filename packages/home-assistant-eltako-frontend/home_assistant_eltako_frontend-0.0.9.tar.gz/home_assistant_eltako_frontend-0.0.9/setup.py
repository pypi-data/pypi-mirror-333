# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['static']

package_data = \
{'': ['*'], 'static': ['assets/*']}

modules = \
['__init__']
install_requires = \
['build', 'wheel']

entry_points = \
{'console_scripts': ['post_install = post_install:compile_typescript']}

setup_kwargs = {
    'name': 'home_assistant_eltako_frontend',
    'version': '0.0.9',
    'description': 'A Python package that includes static files',
    'long_description': '\n## How to build typescript application and create wheel package\n\n1. Checkout repository\n2. Start devcontainer\n3. Run `python3 build.py`\n4. Application can be found in folder `static`\n5. Wheel package can be found in folder `dist`\n\n\n## How to start webpage in development mode\n\n1. start devcontainer\n2. create file `.env` in project folder and add all variables defined in `./src/environment.d.ts`\n  * `HA_URL`: Is mandatory and the address to home assistant server e.g. `http://homeassistant.local:8123`\n  * `LONG_LIVED_TOKEN`: Is optional and avoids login prompt\n3. Run `npx vite dev` in devcontainer\n',
    'author': 'Philipp Grimm',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
