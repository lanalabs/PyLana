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
 