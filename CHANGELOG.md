# PyLana Changelog

The changelog is based on [this guide](https://keepachangelog.com/en/0.3.0/). This project strives to adhere to [semantic versioning](https://semver.org/).

# Unreleased


# [0.2.0]

## Added

* user management interface
* dashboard management interface
* data aggregation interface

## Changed

* The default behaviour is now to always try verifying the server's TLS certificate (the default of [requests](https://requests.readthedocs.io/en/master/)). For more granular control over your request, you can still pass keyword arguments documented in the [requests documentation](https://requests.readthedocs.io/en/latest/api/#requests.request) to all methods, functions and constructors.
