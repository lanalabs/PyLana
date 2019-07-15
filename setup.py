import setuptools

setuptools.setup(
    name="pylana",
    version="0.0.1",
    author="Lana Labs GmbH",
    description="Python interface for Lana API",
    long_description_content_type="text/markdown",
    url="https://github.com/lanalabs/pylana.git@pylana_dist",
    packages=['pylana'],
    install_requires=['docopt', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)