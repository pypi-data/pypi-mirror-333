from setuptools import setup

setup(
    name="superforecast",
    version="0.1.4",
    description="Super Forecast - A modern forecasting API client powered by bio-inspired AI models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="San Martim",
    author_email="superforecast@dataspoc.com",
    license="MIT",
    packages=["superforecast"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": ["superforecast = superforecast.client:main"]
    },
    keywords=[
        "forecast",
        "forecasting",
        "AI models",
        "timeseries",
        "demand forecasting",
        "energy forecasting",
        "financial market forecasting",
    ],
)