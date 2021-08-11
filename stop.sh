#!/bin/bash
ps -ef | grep community-discussion/venv/bin/flask | grep -v grep | awk '{ print $2 }' | xargs kill -9 
ps -ef | grep chat/app.py | grep -v grep | awk '{ print $2 }' | xargs kill -9 
ps -ef | grep community-discussion/frontend/node_modules/.bin/vue-cli-service | grep -v grep | awk '{ print $2 }' | xargs kill -9 
