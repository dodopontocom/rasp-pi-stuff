#!/usr/bin/env bash

#

TIMING=$(date +%d%m%Y%H%M)
CMD=$(vcgencmd measure_temp | sed "s/[^0-9.]//g")
UP_TIMING=$(uptime -p)
TEMPERATURE_LOG_PATH="${HOME}/git/rasp-pi-stuff/logs"
FULL_PATH=${TEMPERATURE_LOG_PATH}/week$(date +%V)_temperature.log

echo ${TIMING},${UP_TIMING/,/},${CMD} >> ${FULL_PATH}