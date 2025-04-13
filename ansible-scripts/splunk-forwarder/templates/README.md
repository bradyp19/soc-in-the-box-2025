# Splunk Universal Forwarder – `inputs.conf.j2`

## What This File Does

This file is a **Jinja2 template** used to generate a valid Splunk `inputs.conf` file, which tells the **Splunk Universal Forwarder (UF)** which log files to monitor and send to the Splunk indexer.

Once deployed, it enables Splunk to ingest logs from specific sources and display them in the Splunk UI, typically as part of a custom dashboard or alerting workflow.

---

## How It Works

- **Monitors specific log files** on the system (e.g., `/home/user/log-generator.log`)
- **Assigns a custom `sourcetype`** so Splunk can properly parse and classify the data
- **Specifies a target index** (e.g., `main`, `linux_logs`, or `custom_sandbox`) so you can organize your logs within Splunk

---

## Example Use Case

When monitoring logs from a fake log generator like `log-generator.py`, your `inputs.conf.j2` might include:

```ini
[monitor:///home/debian/logs/log-generator.log]
disabled = false
index = main
sourcetype = fake_loggen_json
