# setup.py

from setuptools import setup, find_packages

setup(
    name="dinoop_package_2",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # List your dependencies here
    author="Dinoop",
    author_email="dinoop@example.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Optional
)