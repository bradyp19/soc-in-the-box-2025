# Fake Log Generator

## Overview
The Fake Log Generator simulates realistic system and network logs to test SOC (Security Operations Center) environments. It supports log generation for multiple types of activity (HTTP, SSH, FTP, DNS, SMTP, IDS) and is designed to integrate seamlessly with tools like Splunk, Wazuh, Graylog, and Velociraptor.

## Purpose
- Generate realistic logs to test log ingestion, alerting, and detection pipelines.
- Simulate both normal and abnormal behaviors, including anomaly injection and burst traffic (spikes).
- Enable repeatable scenario testing via replay mode.
- Allow SOC teams to benchmark detections against ATT&CK-mapped activity.

## Key Features
- Supports log types: HTTP, SSH, FTP, DNS, SMTP, IDS
- Realistic anomaly injection (e.g., brute-force SSH login)
- Spike simulation to test event burst handling
- Replay mode for reproducing known scenarios
- JSON-formatted logs with metadata (timestamp, log type, host, severity, OS)

## MITRE ATT&CK Integration (Conceptual)
To support detection engineering aligned with MITRE ATT&CK:
- Certain logs correspond to real ATT&CK techniques:
  - **SSH failed login bursts** simulate `T1110 - Brute Force`
  - **FTP uploads/downloads** can reflect `T1048 - Exfiltration Over Alternative Protocol`
  - **DNS NXDOMAIN or SERVFAIL** errors can be tied to `T1071.004 - Application Layer Protocol: DNS`
  - **IDS alerts** mimic `T1203 - Exploitation for Client Execution` or `T1059 - Command and Scripting Interpreter`
- Future enhancements may allow for:
  - Scenario configuration files mapped to ATT&CK IDs
  - Metadata tagging per event with technique IDs (e.g., `"attack_technique": "T1110"`)

## Usage

### Run Normally (Generate Logs)
```bash
python3 log-generator.py
```

### Replay Mode
Edit the script to set:
```python
REPLAY_MODE = True
REPLAY_FILE = "replay_data.txt"
```
Then run:
```bash
python3 log-generator.py
```

## Output Example
Each log entry is formatted in JSON:
```json
{
  "timestamp": "2025-04-01 12:00:00",
  "log_type": "SSH",
  "host": "web01",
  "severity": "Info",
  "message": "[2025-04-01 12:00:00] 192.168.1.15 - Accepted password for user1",
  "os": "Linux"
}
```

## Folder Structure
```
fake-log-generator/
├── log-generator.py          # Main script
├── replay_data.txt           # Optional replay file
└── README.md                 # This documentation
```

## Future Enhancements
- MITRE ATT&CK metadata tagging for detection alignment
- Configurable attack scenarios via YAML/JSON
- Real-time log streaming to SIEM via syslog or HTTP
- Web UI for log scenario design and control
