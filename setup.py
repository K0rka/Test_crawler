import os

from setuptools import setup, find_packages


def get_version():
    # Versioning approach adopted as suggested in https://packaging.python.org/en/latest/single_source_version/
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(curr_dir, "version.txt")) as version_file:
        return version_file.read().strip()


setup(
    name="crawler",
    version=get_version(),
    description="A simple web crawler",
    author="Katrin Korovkina",
    author_email="c.korovkina@gmail.com",
    url="github.com:K0rka/Test_crawler.git",
    platforms="any",
    # package_data={"src": ["job_data/*"]},
    packages=find_packages(exclude=["tests", "tests.*"]),
)
