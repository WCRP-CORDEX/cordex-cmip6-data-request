import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# get version
with open("data_request/version.py") as f:
    line = f.readline().strip().replace(" ", "").replace('"', "")
    version = line.split("=")[1]
    __version__ = version


setuptools.setup(
    name="data_request",  # Replace with your own username
    version=version,
    author="Lars Buntemeyer",
    author_email="lars.buntemeyer@hereon.de",
    description="CORDEX-CMIP6 data request",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WCRP-CORDEX/cordex-cmip6-data-request",
    # packages=setuptools.find_packages(),
    packages=["data_request"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
