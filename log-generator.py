import random
import time
import json
import re
from datetime import datetime

# Try to import psutil for resource monitoring if needed
try:
    import psutil
except ImportError:
    psutil = None

REPLAY_MODE = False  
REPLAY_FILE = "replay_data.txt"  # File containing events to replay in replay mode

# Log file path (for Splunk forwarder, you might set this to e.g., /var/log/socinabox-logs.txt)
log_file = "/var/log/socinabox-logs.txt"

# Use JSON formatting for Splunk integration (set to False for plain text)
USE_JSON_FORMAT = True

# Base events per second
BASE_EPS = 1.0

# Define weighted probabilities for log types (sums to 1.0)
event_weights = {
    "HTTP": 0.4,
    "SSH": 0.2,
    "FTP": 0.2,
    "DNS": 0.1,
    "SMTP": 0.1
}

# Spike configuration: chance to simulate a burst (spike) of events
SPIKE_FACTOR = 3      # Spike mode increases the EPS by this factor
SPIKE_PROBABILITY = 0.1  # 10% chance to enter spike mode

# Anomaly injection probability for SSH logs
ANOMALY_PROBABILITY = 0.05  # 5% chance to inject an anomaly (multiple failed logins)

# ------------------------------
# Sample Data for Log Generation
# ------------------------------

http_methods = ["GET", "POST", "PUT", "DELETE"]
ssh_actions = ["Accepted password", "Failed password", "Disconnected"]
ftp_actions = ["Login successful", "Login failed", "File uploaded", "File downloaded"]
dns_actions = ["Query", "Response", "NXDOMAIN", "SERVFAIL"]
smtp_actions = ["Mail sent", "Mail received", "Spam detected", "Delivery failed"]

status_codes = ["200", "301", "403", "404", "500"]
usernames = ["admin", "user1", "root", "guest"]
ips = [f"192.168.1.{i}" for i in range(1, 255)]
domains = ["example.com", "testsite.net", "myserver.local", "company.org"]

# ------------------------------
# Log Generation Functions (given by hemanth)
# ------------------------------

def generate_http_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choice(ips)
    method = random.choice(http_methods)
    status = random.choice(status_codes)
    return f"[{timestamp}] {ip} - {method} /index.html {status}"

def generate_ssh_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choice(ips)
    username = random.choice(usernames)
    # Inject anomaly: simulate a burst of failed login attempts
    if random.random() < ANOMALY_PROBABILITY:
        action = "Failed password"
        events = []
        for _ in range(3):  # generate 3 rapid events
            event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            events.append(f"[{event_time}] {ip} - {action} for user {username}")
            time.sleep(0.1)
        return "\n".join(events)
    else:
        action = random.choice(ssh_actions)
        return f"[{timestamp}] {ip} - {action} for user {username}"

def generate_ftp_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choice(ips)
    username = random.choice(usernames)
    action = random.choice(ftp_actions)
    return f"[{timestamp}] {ip} - {action} by {username}"

def generate_dns_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choice(ips)
    dns_action = random.choice(dns_actions)
    domain = random.choice(domains)
    return f"[{timestamp}] {ip} - {dns_action} for {domain}"

def generate_smtp_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = random.choice(ips)
    smtp_action = random.choice(smtp_actions)
    username = random.choice(usernames)
    return f"[{timestamp}] {ip} - {smtp_action} from {username}@example.com"

# JSON formatting for Splunk
def format_log(log_type, log_message):
    if USE_JSON_FORMAT:
        return json.dumps({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "log_type": log_type,
            "message": log_message
        })
    else:
        return log_message

def write_log_to_file(log):
    with open(log_file, "a") as file:
        file.write(log + "\n")

# ------------------------------
# Replay Mode Functionality
# ------------------------------

def replay_logs():
    """
    Replay events from a file, preserving original intervals.
    Replaces the original timestamp with the current time.
    """
    try:
        with open(REPLAY_FILE, "r") as f:
            events = f.readlines()
    except FileNotFoundError:
        print(f"Replay file '{REPLAY_FILE}' not found. Exiting replay mode.")
        return

    if not events:
        print("Replay file is empty. Exiting replay mode.")
        return

    previous_event_time = None
    base_time = datetime.now()

    for event in events:
        match = re.search(r'\[(.*?)\]', event)
        if not match:
            print(event.strip())
            write_log_to_file(event.strip())
            continue

        original_time_str = match.group(1)
        try:
            original_event_time = datetime.strptime(original_time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(event.strip())
            write_log_to_file(event.strip())
            continue

        if previous_event_time is None:
            current_time = base_time
            previous_event_time = original_event_time
        else:
            time_diff = (original_event_time - previous_event_time).total_seconds()
            time.sleep(max(time_diff, 0))
            current_time = datetime.now()
            previous_event_time = original_event_time

        new_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        new_event = re.sub(r'\[(.*?)\]', f"[{new_timestamp}]", event, count=1)
        print(new_event.strip())
        write_log_to_file(new_event.strip())

# ------------------------------
# Generated Mode Functionality
# ------------------------------

def get_current_eps():
    """
    Dynamically adjust events per second based on time of day.
    For example, during business hours (8-18) we might generate more events.
    """
    current_hour = datetime.now().hour
    if 8 <= current_hour < 18:
        return BASE_EPS * 1.5
    else:
        return BASE_EPS

def generate_logs():
    while True:
        # Adjust event rate based on time of day
        current_eps = get_current_eps()
        delay = 1 / current_eps
        
        # Simulate a temporary spike with a given probability
        if random.random() < SPIKE_PROBABILITY:
            effective_delay = 1 / (current_eps * SPIKE_FACTOR)
        else:
            effective_delay = delay

        # Select log type using weighted probabilities
        log_type = random.choices(list(event_weights.keys()), weights=list(event_weights.values()), k=1)[0]
        
        if log_type == "HTTP":
            log_entry = generate_http_log()
        elif log_type == "SSH":
            log_entry = generate_ssh_log()
        elif log_type == "FTP":
            log_entry = generate_ftp_log()
        elif log_type == "DNS":
            log_entry = generate_dns_log()
        elif log_type == "SMTP":
            log_entry = generate_smtp_log()
        else:
            log_entry = "Unknown log type"
        
        formatted_log = format_log(log_type, log_entry)
        print(formatted_log)
        write_log_to_file(formatted_log)
        time.sleep(effective_delay)

# ------------------------------
# Main Execution
# ------------------------------

if __name__ == "__main__":
    if REPLAY_MODE:
        print("Replay mode enabled. Replaying events from file...")
        replay_logs()
    else:
        generate_logs()
