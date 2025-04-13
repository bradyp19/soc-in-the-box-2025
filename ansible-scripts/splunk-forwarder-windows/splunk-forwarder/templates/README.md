# Splunk Universal Forwarder – `inputs.conf.j2` (Windows Version)

## Overview

This file is a template used to generate the `inputs.conf` configuration file for the Splunk Universal Forwarder on Windows systems. It defines which files the forwarder should monitor and send to the Splunk indexer.

## Purpose

- Tell the Splunk Universal Forwarder which file(s) to watch
- Assign a custom index where logs will appear in Splunk Web
- Set a sourcetype for parsing the log format
- Enable dashboards and alerts to be powered by your custom or synthetic log data

## Example Usage (Windows)

For example, if you're generating logs using a script on your Windows Server and saving them to `C:\logs\log-generator.log`, your `inputs.conf.j2` should look like:

```ini
[monitor://C:\logs\log-generator.log]
disabled = false
index = main
sourcetype = fake_loggen_json
