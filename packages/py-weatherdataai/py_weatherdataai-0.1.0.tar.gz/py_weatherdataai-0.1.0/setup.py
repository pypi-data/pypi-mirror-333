from setuptools import setup, find_packages

setup(
    name="py_weatherdataai",  # Package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    author="Your Name",
    description="A simple API client for WeatherDataAI",
    url="https://weatherdata.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
