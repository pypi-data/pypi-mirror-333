import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weather_utils",
    version="0.1",
    author="Srihari Kata",
    author_email="x24155331@student.ncirl.ie",  # Replace with your email
    description="Custom utilities for AWS integration in the Weather App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sriharikata/CPP_Project/tree/main/weatherapp/weather_utils",  # Replace with actual GitHub URL
    packages=["weather_utils"],
    install_requires=["boto3", "requests"],  # Required dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

