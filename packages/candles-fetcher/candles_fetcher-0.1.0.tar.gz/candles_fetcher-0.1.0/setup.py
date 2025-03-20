from setuptools import setup, find_packages

setup(
    name="candles-fetcher",
    version="0.1.0",
    author="Wynne",
    author_email="wynne1999.work@example.com",
    description="A simple package to fetch candlestick data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/candles-fetcher",
    packages=find_packages(),
    install_requires=[
        "ccxt",
        "pandas",
        "asyncio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
