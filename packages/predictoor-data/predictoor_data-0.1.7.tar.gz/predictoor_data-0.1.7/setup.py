from setuptools import setup, find_packages

setup(
    name="predictoor-data",
    version="0.1.7",
    author="oceanprotocol",
    author_email="devops@oceanprotocol.com",
    packages=find_packages(),
    package_data={
        'predictoor_data': ['abis/*.json'],
    },
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0",
        "python-dateutil>=2.8.0",
        "pytest>=6.0.0",
        "mypy>=0.900",
        "black>=21.0",
        "web3==6.20.2",
        "eth-account==0.11.0",
    ],
    description="A package for fetching historical and prediction data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oceanprotocol/predictoor-data",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)
