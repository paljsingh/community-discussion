#!/bin/bash
ps -ef | grep flask | grep -v grep | awk '{ print $2 }' | xargs kill -9 
ps -ef | grep chat/app.py | grep -v grep | awk '{ print $2 }' | xargs kill -9 
