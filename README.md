# DAPNET SCRIPTS

A collection of scripts for DAPNET

## Available scripts

Please add scripts in subfolders and describe the function here.

### mowas

Forwarding of MoWaS messages provided by DARC. Right now just a simple http server to collect messages and dump them in a log file. Will be expanded once the message distribution implementation is finished on the side of DARC.

### DAPNET-Framework

Simple framework for posting calls and news to DAPNET via simple functions.

### DAPNET_ISS

Calculating the rise, maximum and set of ISS (International Space Station) based on NASA TLE-data being fetched every 4 hours by the script.
Should run every minute via crontab.
