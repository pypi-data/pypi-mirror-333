from setuptools import setup, find_packages

setup(
    name="crypto-candle-fetcher",
    version="0.1.6",  
    author="Metupia",
    author_email="metupia.git@gmail.com",
    description="A Python library for fetching OHLC data from multiple cryptocurrency exchanges.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/metupia/crypto-candle-fetcher",
    packages=find_packages(include=["crypto_candle_fetcher", "crypto_candle_fetcher.*"]),
    package_data={
        "crypto_candle_fetcher": ["exchanges/*.py", "data/*"]  
    },
    install_requires=[
        "requests",
        "pandas",
    ],
    include_package_data=True,  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
