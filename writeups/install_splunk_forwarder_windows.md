# Installing Splunk Universal Forwarder on Windows using Ansible

This project provides step-by-step instructions to automate the installation and configuration of the **Splunk Universal Forwarder** on **Windows Server 2019** and **Windows 11 Enterprise** using **Ansible** over **WinRM**.

---

## Overview

The playbook sets up the Splunk Universal Forwarder, configures deployment and outputs settings, and ensures the service is running. It is designed for lab or test environments and supports centralized log forwarding to a Splunk Search Head.

---

## Prerequisites

### Platform Requirements

- Ansible control node (e.g., Ludus VM)
- Target Windows machines with WinRM enabled
- Open firewall ports: `5985`, `9997`, and `8089`

### Required Setup

- Ansible inventory file with host groups
- Role structure and templates as shown below

---

## Project Structure


---

## Inventory Configuration

**File**: `inventory.ini`

```content
# Splunk Forwarder Deployment for Windows (Ansible-Based)

This README provides a reference for deploying and configuring the Splunk Universal Forwarder on Windows machines using Ansible. It includes inventory definitions, role variables, and key configuration templates.

## Inventory Example: `inventory.ini`

```ini
[windows]
10.4.10.51

[windows_server]
10.4.10.50

[windows_server:vars]
ansible_user=Administrator
ansible_password="Str0ngP@ssw0rd!"
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
ansible_port=5985

[windows:vars]
ansible_user=localuser
ansible_password="password"
ansible_connection=winrm
ansible_winrm_transport=basic
ansible_winrm_server_cert_validation=ignore
ansible_port=5985
```

## Ansible Playbook Example: `main.yml`

```yaml
- name: Install Splunk Forwarder on Windows Server
  hosts: windows_server
  gather_facts: false
  roles:
    - role: splunk-forwader
      vars:
        splunk_search_head: "10.4.10.3"

- name: Install Splunk Forwarder on Windows Enterprise
  hosts: windows
  gather_facts: false
  roles:
    - role: splunk-forwader
      vars:
        splunk_search_head: "10.4.10.3"
```

## Role Variables: `defaults/main.yml`

```yaml
admin_password: "Str0ngP@ssw0rd!"
splunk_forwarder_version: "9.4.1"
splunk_forwarder_package: "splunkforwarder-9.4.1-e3bdab203ac8-windows-x64.msi"
splunk_forwarder_download_url: "https://download.splunk.com/products/universalforwarder/releases/9.4.1/windows/splunkforwarder-9.4.1-e3bdab203ac8-windows-x64.msi"
splunk_forwarder_install_dir: "C:\\Program Files\\SplunkUniversalForwarder"
splunk_forwarder_user: "Administrator"
splunk_forwarder_group: "Administrators"
splunk_user: "admin"
splunk_password: "password"
splunk_search_head: "10.7.10.3"
splunk_forwarder_ports:
  - 8089
  - 9997
  - 514
```

## Install Splunk Forwarder Task

```yaml
win_command: >
  msiexec /i "C:\\Users\\Administrator\\Downloads\\{{ splunk_forwarder_package }}"
  AGREETOLICENSE=Yes
  INSTALLDIR="{{ splunk_forwarder_install_dir }}"
  SPLUNKUSERNAME=admin
  SPLUNKPASSWORD=password
  /quiet /norestart /L*v "C:\\splunk_install_log.txt"
args:
  removes: "{{ splunk_forwarder_install_dir }}"
register: splunk_install
become: yes
become_method: runas
become_user: Administrator
```

## Deploy Configuration Files

### Template: `templates/outputs.conf.j2`

```conf
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = {{ splunk_search_head }}:9997
autoLB = true
useACK = true

[tcpout-server://{{ splunk_search_head }}:9997]
```

### Template: `templates/deploymentclient.conf.j2`

```conf
[deployment-client]
clientName = {{ inventory_hostname }}

[target-broker:deploymentServer]
targetUri = {{ splunk_deployment_server }}:8089
```

This setup enables automated Splunk Universal Forwarder deployment and log forwarding configuration across multiple Windows machines using Ansible.

## Run the playbook
```
ansible-playbook -i inventory.ini main.yml 
```
