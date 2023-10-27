#!/bin/bash

launchctl setenv NUKE_PATH "/Volumes/VFX/Shared/NFTS_nuk_env"
launchctl setenv HIERO_PLUGIN_PATH "/Volumes/VFX/Shared/NFTS_nuk_env"


kill -9 $(ps -p $(ps -p $PPID -o ppid=) -o ppid=)
