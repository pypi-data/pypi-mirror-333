# setup.py

from setuptools import setup, find_packages

setup(
    name = 'nathanxli_package',
    version = 0.2,
    packages = find_packages(),
    install_require = [
        ###
    ],

    entry_points = {
        "console_scripts": [
            "nxli-test = nathanxli_package:test",
        ],
    },
)