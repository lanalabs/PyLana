from setuptools import setup

setup(
    name='pylana',
    url='https://github.com/lanalabs/pylana',
    author='Lana Labs GmbH',
    author_email='support@lanalabs.com',
    packages=['pylana'],
    install_requires=["requests"],
    version='0.1',
    license='MIT',
    description='A python package to wrap log-related API calls on the Lana Process Mining Software.'
)