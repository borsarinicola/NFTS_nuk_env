#!/bin/bash

launchctl setenv NUKE_PATH "/Volumes/CompEnvironment/"
launchctl setenv HIERO_PLUGIN_PATH "/Volumes/CompEnvironment/"


kill -9 $(ps -p $(ps -p $PPID -o ppid=) -o ppid=)
