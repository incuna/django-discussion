from os.path import dirname, join
from setuptools import find_packages, setup

from discussion import get_version

def fread(fname):
    with open(join(dirname(__file__), fname), 'r') as f:
        return f.read()

setup(
    name = "django-discussion",
    packages = find_packages(),
    include_package_data=True,
    install_requires = ['django-orderable>=1.0.1'],
    version = get_version(),
    description = "",
    author = "Incuna Ltd",
    author_email = "dev@incuna.com",
    url = "http://incuna.com/",
    long_description=fread("README.md"),
)

