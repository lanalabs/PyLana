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
 * the dev environment uses [pytest](https://docs.pytest.org/en/latest/), but the tests also work with [unittest](https://docs.python.org/3/library/unittest.html)
 