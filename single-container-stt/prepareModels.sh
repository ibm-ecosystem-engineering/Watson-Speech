#! /usr/bin/env bash
set -u

cleanup() {
  local pids=$(jobs -pr)
  if [ -n "$pids" ]; then
    kill $pids
  fi
}
trap "cleanup" SIGINT SIGQUIT SIGTERM EXIT

python -m http.server --bind 127.0.0.1 --directory /models 3333 &

./runChuck.sh &

# wait for the server to become ready, which happens after it downloads the models
max_tries=10
tries=0
while [[ tries -lt max_tries ]]; do
  curl -sk -o /dev/null "localhost:1080/v1/miniHealthCheck"
  if [[ $? -eq 0 ]]; then
    echo "Model initialization complete"
    exit 0
  fi

  sleep 5
  ((tries+=1))
done

echo "Server failed to initialize models in time."
exit 1
