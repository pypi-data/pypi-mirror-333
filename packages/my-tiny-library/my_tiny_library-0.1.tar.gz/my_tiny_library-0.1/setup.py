from setuptools import setup, find_packages

setup(
    name="my_tiny_library",
    version="0.1",
    packages=find_packages(),
    description="A tiny Python library to greet users.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tarik Kasbaoui",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_tiny_library",
    license="MIT",
)