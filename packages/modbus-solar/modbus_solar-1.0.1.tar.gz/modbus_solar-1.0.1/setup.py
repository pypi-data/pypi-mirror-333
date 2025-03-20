from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='modbus-solar',
    version='1.0.1',
    author='boopzz',
    author_email='boopzz@pm.me',
    description = "A small package to pull stats from a Renogy Solar Charge Controller",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/boopzz/modbus-solar',
    packages=find_packages(),
    install_requires=[
        'minimalmodbus>=2.0.0'
    ],
    entry_points={
        "console_scripts": [
            "modbus-solar-get-all = modbus_solar:get_all", # #FIXME ensure they work with output tools ie jq, redirect etc
        ],
    },
)
