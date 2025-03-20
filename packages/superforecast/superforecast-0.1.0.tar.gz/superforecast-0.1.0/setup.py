from setuptools import setup

setup(
    name="superforecast",
    version="0.1.0",
    description="Client for accessing a API service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="San Martim",
    author_email="sanmartim@superforecast.dev",
    license="MIT",
    packages=["superforecast"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": ["superforecast = superforecast.client:main"]
    },
)