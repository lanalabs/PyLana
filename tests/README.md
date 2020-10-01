# How to test

* Tests require access to the API of a LANA Process Mining Instance.
* Credentials have to be provided as a json stored in a file named `config.json` with the structure
    ```json
    {
      "scheme": "<http or https>",
      "host": "<host>",
      "port": "<port>",
      "token": "<token>"
    }
    ```
* To run the tests contained in `test_users.py` a json with credentials for a user with the role user admin have to be provided in a file named `config_useradmin.json`. The format has to be the same as `config.json`. Both users have to live in the same organisation on the same LANA Process Mining instance.
* We require the r analyst role to have access to one log named `Incident_Management.csv`, one shiny dashboard named `incident-test-shiny-dashboard` and one dashboard named `incident-test-dashboard`. The dashboard and shiny dashboard don't need to be connected to a log. The shiny dashboard also doesn't need to contain actual code as we just use its metadata for the tests.
* [pytest](https://docs.pytest.org/en/latest/) is required to run the tests. It is included in the shipped conda environment.
