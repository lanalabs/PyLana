import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylana",
    version="0.0.1",
    author="Lana Labs GmbH",
    description="Python interface for Lana API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lanalabs/pylana",
    install_requires=['pylana', 'docopt', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)