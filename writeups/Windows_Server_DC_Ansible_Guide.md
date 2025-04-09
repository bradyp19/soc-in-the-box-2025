# Automating Windows Server Domain Controller Setup with Ansible

This project outlines how to configure a **Windows Server 2019** virtual machine as an **Active Directory Domain Controller** using **Ansible** on the **Ludus platform**. It also covers **WinRM setup** for both Windows Server 2019 and Windows 11 2022 Enterprise to enable Ansible remote management.

## Overview

Automate your Windows Server 2019 Domain Controller configuration using Ansible. This guide streamlines domain setup, post-installation tasks, and includes OpenSSH and registry configuration.

---

## Prerequisites

### Platform Requirements

- Access to **Ludus platform**
- A clean **Windows Server 2019 VM**
- Ansible control node (Ludus VM)
- WinRM properly configured (see [WinRM Setup](#winrm-setup))

### User Requirements

- Admin access to Windows VM (`localuser`)
- Familiarity with PowerShell and Ansible

---

## Ansible Project Structure

Ensure the following file structure in your project directory (`~/ansible-script-win2019-server/`):


---

## Inventory Configuration

**File**: `inventory.ini`

```ini
[windows_server]
10.4.10.50

[windows_server:vars]
ansible_user=localuser
ansible_password="password"
ansible_connection=winrm
ansible_winrm_transport=basic
ansible_winrm_server_cert_validation=ignore
ansible_port=5985
ansible_become_user=Administrator
ansible_become_method=runas
```
---

vars/main.yml
```
netbios_name: "DC"
fqdn_tail: "home.arpa"
domain_admin_password: "Str0ngP@ssw0rd!"  # Change this
domain_functional_level: "WinThreshold"
forest_functional_level: "WinThreshold"
```
---

WinRM Setup
Manual Setup for Windows Server 2019
```
Set-Service -Name WinRM -StartupType Automatic
Start-Service -Name WinRM
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
New-NetFirewallRule -Name "AllowWinRM" -DisplayName "Allow WinRM" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
winrm quickconfig -q
```
Manual Setup for Windows 11 2022 Enterprise
```
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private
Set-Service -Name WinRM -StartupType Automatic
Start-Service -Name WinRM
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'
New-NetFirewallRule -Name "AllowWinRM" -DisplayName "Allow WinRM" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow
winrm quickconfig -q
```
---
Running the Playbook
```
cd ~/windows_2019_Server_config/
ansible-playbook -i inventory.ini main.yml
```
