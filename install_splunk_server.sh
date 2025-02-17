#!/bin/bash
ssh-keygen -R 10.13.99.2

# TODO
# Curl Splunk Server download to machine. Save in Temp Folder
# Delete after installing on ludus machines
# Tell user to reset password on first login.
# Display username and password to user to login.
# Tell user what IP and to connect
# Enable splunk Server listening /opt/splunk/bin/splunk enable listen 9997



SSH_USER="debian"
# echo "Enter SSH username: "
# read SSH_USER
VM_IP="10.13.99.2"
# echo "Enter VM IP"
# read VM_IP
PASSWORD="TestPassword"
# Set Splunk installation path
SPLUNK_HOME="/opt/splunk"

echo "[+] Transfer Splunk to Debian Server"
scp -r /home/brayden-g/splunk ${SSH_USER}@${VM_IP}:/home/${SSH_USER}/

echo "[+] Install Splunk on Server"
ssh -t ${SSH_USER}@${VM_IP} << EOF
  echo "[+] Checking if rsync is installed on server"
  
  if ! command -v rsync &> /dev/null; then
    echo "[+] Installing rsync"
    sudo apt update -y && sudo apt install -y rsync
  else
    echo"[+] rsync is already installed"
  fi

  echo "[+] Adding splunk user"
  sudo useradd -m splunk

  echo "[+] Moving Splunk files..."
  sudo rsync -av /home/debian/splunk/ /opt/splunk/

  if [ ! -f "/opt/splunk/bin/splunk" ]; then
    echo "[ERROR] Splunk binary not found! Check installation."
    exit 1
  fi

  sudo mkdir -p /opt/splunk/etc/system/local
  echo "[user_info]" | sudo tee /opt/splunk/etc/system/local/user-seed.conf
  echo "USERNAME = admin" | sudo tee -a /opt/splunk/etc/system/local/user-seed.conf
  echo "PASSWORD = SuperSecure123" | sudo tee -a /opt/splunk/etc/system/local/user-seed.conf

  # Enable Listening on port 9997
  echo "[splunktcp://9997]" | sudo -u splunk tee /opt/splunk/etc/system/local/inputs.conf
  echo "disabled = 0" | sudo -u splunk tee /opt/splunk/etc/system/local/inputs.conf

  # Accept License
  sudo /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt

  # Change ownership to splunk user
  sudo chown -R splunk:splunk /opt/splunk

  # Switch startup user to splunk user
  sudo /opt/splunk/bin/splunk enable boot-start -user splunk --accept-license
  sudo /opt/splunk/bin/splunk restart

  echo "[+] Splunk installation complete!"
  echo "[+] Change SPLUNK ADMIN password"
EOF
