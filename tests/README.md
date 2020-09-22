# How to test

* tests require access to a lana api
* credentials have to be provided as a json stored in a file named `config.json`
    ```json
    {
      "scheme": "<http or https>",
      "host": "<host>",
      "port": "<port>",
      "token": "<token>"
    }
    ```
 * we require the user has access to one log named `Incident_management.csv`
 * to run the tests contained in `test_users.py` a json with useradmin credentials called `config_useradmin.json` has to be provided with the same format as `config.json`
 * [pytest](https://docs.pytest.org/en/latest/) is required to run the tests
