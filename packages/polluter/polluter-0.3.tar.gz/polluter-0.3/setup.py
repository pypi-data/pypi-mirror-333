from setuptools import setup, find_packages

setup(
    name="polluter",
    version="0.3",
    author="j@ack",
    package_dir={"": "src"},
    packages=find_packages(where="src")
)