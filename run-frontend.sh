#!/bin/bash
cd frontend
yarn install

yarn_run_mode=${YARN_RUN_MODE:-dev}
yarn start --mode $yarn_run_mode
