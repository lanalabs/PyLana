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
* We require the r analyst role to have access to one log named `Incident_management.csv`.
* [pytest](https://docs.pytest.org/en/latest/) is required to run the tests. It is included in the shipped conda environment.
