#!/bin/bash
set -eo pipefail

host="$(hostname -i || echo '0.0.0.0')"

if ping="$(redis-cli -h "$host" ping)" && [ "$ping" = 'PONG']; then
  exit 0
fi

exit 1
