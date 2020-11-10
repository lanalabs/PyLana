#!/bin/bash

# This script creates the json files with the api credentials from
# environment variables and starts the tests with pytest


cat <<EOF > ./tests/config.json
{
  "scheme": "$SCHEME",
  "host": "$HOST",
  "port": $PORT,
  "token": "$TOKEN_USER"
}
EOF

cat <<EOF > ./tests/config_useradmin.json
{
  "scheme": "$SCHEME",
  "host": "$HOST",
  "port": $PORT,
  "token": "$TOKEN_USERADMIN"
}
EOF

python -m pytest -x
