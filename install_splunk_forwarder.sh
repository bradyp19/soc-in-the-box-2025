#!/bin/bash

FORWARD_SERVER="10.13.99.2"
PORT="9997"

USERNAME="kali"
SERVER_IP="10.13.99.1"
PASSWORD="kali"

sshpass -p "$PASSWORD" ssh -tt ${USERNAME}@${SERVER_IP} << EOF
    echo "$PASSWORD" | sudo -S wget -O splunkforwarder-9.4.0-6b4ebe426ca6-linux-amd64.tgz "https://do>

    echo "$PASSWORD" | sudo -S tar -zxvf splunkforwarder-9.4.0-6b4ebe426ca6-linux-amd64.tgz -C /tmp
    echo "$PASSWORD" | sudo -S mv /tmp/splunkforwarder /opt/

    id splunk &>/dev/null || echo "$PASSWORD" | sudo -S useradd -m splunk

    echo "$PASSWORD" | sudo -S chown -R splunk:splunk /opt/splunkforwarder

    sudo -u splunk mkdir -p /opt/splunk/etc/system/local

    # Creates Admin account for Splunk
    echo "[user_info]" | sudo -u splunk tee /opt/splunk/etc/system/local/user-seed.conf
    echo "USERNAME = admin" | sudo -u splunk tee -a /opt/splunk/etc/system/local/user-seed.conf
    echo "PASSWORD = SuperSecure123" | sudo -u splunk tee -a /opt/splunk/etc/system/local/user-seed.c>


    echo "$PASSWORD" | sudo -S chown -R splunk:splunk /opt/splunkforwarder

    echo "$PASSWORD" | sudo -S -u splunk /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --no-prompt  
    echo "$PASSWORD" | sudo -S -u splunk /opt/splunkforwarder/bin/splunk add forward-server ${FORWARD_SERVER}:{PORT} -auth admin:SuperSecure123    
    echo "$PASSWORD" | sudo -S -u splunk /opt/splunkforwarder/bin/splunk restart

    echo "[+] Splunk Forwarder installation complete!"
EOF
