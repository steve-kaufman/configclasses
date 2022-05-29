from setuptools import find_packages, setup

with open("readme.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="configclasses",
    version="0.2.0",
    packages=find_packages(),
    description="Class annotation for easy configuration dataclasses",
    long_description=long_description,
    author="Steven Kaufman",
    url="https://github.com/steve-kaufman/configclasses",
    requires=[]
)