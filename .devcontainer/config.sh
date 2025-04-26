#!/usr/bin/env bash

repo_root_dir="$(dirname "$0")/.."
env_file="$repo_root_dir/.env"

eval "$(
  < "$env_file" awk '!/^\s*#/' | awk '!/^\s*$/' | while IFS='' read -r line; do
    key=$(echo "$line" | cut -d '=' -f 1)
    value=$(echo "$line" | cut -d '=' -f 2-)
    echo "$key=$value"
  done
)"

cat <<EOF > ~/.pypirc
[testpypi]
  username = __token__
  password = $PYPI_TEST_TOKEN
EOF

uv sync
# python -m venv "$repo_root_dir/.venv"
# source "$repo_root_dir/.venv/bin/activate"
