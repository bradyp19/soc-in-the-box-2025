# Velociraptor README
This script is created to automate the deployment of [velociraptor](https://docs.velociraptor.app/) server and clients.

# Requirements
- git

# Default Username and Password
Ludus Default Passwords are being used for this project (Can change)
Format "username:password"
- debian:debian
- kali:kali

# How To Use
```bash
git clone https://github.com/bradyp19/soc-in-the-box-2025.git
```

```bash
cd ansible-scripts/velociraptor
```

## Inventory changes
IP address will need to changed. 

ansible_ssh_private_key_file will also need to be changed. 

Passwords are defaults. Can change to use ansible vault for passwords but for demonstration purposes passwords are hardcoded

```bash
nano inventory.ini
```

```bash
[forensics_server]
10.3.10.3 ansible_user=debian ansible_ssh_private_key_file=~/.ssh/ansible

[kali]
10.3.99.1 ansible_user=kali ansible_ssh_private_key_file=~/.ssh/ansible ansible_sudo_pass='kali'

[splunk_server]
10.3.10.1 ansible_user=debian ansible_ssh_private_key_file=~/.ssh/ansible

[vulhub_server]
10.3.66.2 ansible_user=debian ansible_ssh_private_key_file=~/.ssh/ansible ansible_sudo_pass='debian'
```

## Defaults/main.yml Changes
Only change that is needed as of 04/02/2025 is velociraptor_server_ip. Change the IP address to the server you want to host velociraptor.
```bash
  ansible_server_user: debian
  velociraptor_install_path: /usr/local/bin/velociraptor
  velociraptor_download_link: https://github.com/Velocidex/velociraptor/releases/download/v0.73/velociraptor-v0.73.4-linux-amd64
  velociraptor_output_file: velociraptor
  velociraptor_server_ip: 10.3.10.3 # change this to your server ip
  velociraptor_server_port: 8000
  velociraptor_admin_username: admin
  velociraptor_admin_password: password
  velociraptor_server_file_location: /etc/server.config.yaml
  velociraptor_client_file_location: /tmp/client.config.yaml

  # Copy_client_config_files.yml
  fetch_group: "forensics_server"
  copy_group: ["kali", "vulhub_server"] # This relates to the inventory names to add clients to.
```

## Running the Playbook
```bash
ansible-playbook -i inventory.ini tasks/main.yml --ask-become
# If incorrect sudo password for kali add to inventory file or create vault in ansible for encrypted passwords
# Example above uses passwords in the inventory file
```

# After playbook runs
IP address is subject to change. Example listed below.

Velociraptor GUI is located at **velociraptor_server_ip:8889**
- Default login information: admin:password
