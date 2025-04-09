# Windows WinRM Setup for Ansible

This repository provides the Ansible playbooks to automate Windows configuration and domain provisioning via WinRM.

---

## Prerequisites

To manage a Windows machine using Ansible over WinRM, you must first enable and configure the WinRM service on the Windows host.

---

## Enable WinRM (Manual Setup via PowerShell)

Run the following **PowerShell commands as Administrator** on the Windows10-2019-Server host:

```powershell
# Enable and start WinRM service
Set-Service -Name WinRM -StartupType Automatic
Start-Service -Name WinRM

# Enable Basic Auth and Allow Unencrypted (required for Ansible winrm transport basic)
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# Create firewall rule to allow WinRM on port 5985
New-NetFirewallRule -Name "AllowWinRM" -DisplayName "Allow WinRM" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow

# Ensure the WinRM listener is running
winrm quickconfig -q
```

Run the following **PowerShell commands as Administrator** on the Windows11-2022-Enterprise host:

```powershell
# Get current network profile(s)
Get-NetConnectionProfile

# OPTIONAL: Set network category to Private (required for WinRM firewall exception to work)
# Replace "Ethernet" with your actual interface name if it's different
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private

# Enable and configure WinRM service
Set-Service -Name WinRM -StartupType Automatic
Start-Service -Name WinRM

# Enable Basic authentication and allow unencrypted traffic (required for Ansible with winrm transport=ntlm)
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'

# Add firewall rule to allow inbound WinRM traffic on HTTP (port 5985)
New-NetFirewallRule -Name "AllowWinRM" -DisplayName "Allow WinRM" -Enabled True -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow

# Ensure the WinRM listener is running
winrm quickconfig -q
```
---

## Verify WinRM is Working

## On the Windows Machine

Run these PowerShell commands to confirm WinRM is listening properly:

```powershell
# Check WinRM listeners (make sure 5985 is listed)
winrm enumerate winrm/config/listener

# Confirm WinRM is listening on port 5985
Get-NetTCPConnection -LocalPort 5985
```

You should see entries showing the system is listening on `0.0.0.0:5985` or your assigned IP address.

---

## From the Ludus (Linux/Ansible) Host

Run one of the following from your Ansible control node:

```bash
# Test TCP connection to the Windows machine
nc -zv <windows_ip> 5985
```
Expected output should show:
```
(UNKNOWN) [10.7.10.50] 5985 (?) open
```

Or with PowerShell Core installed:

```bash
Test-NetConnection -ComputerName 10.7.10.50 -Port 5985
```

Expected output should show:
```
TcpTestSucceeded : True
```


When using Ansible with WinRM, ensure your inventory uses the Administrator account like so:

```inventory.ini
[windows]
0.0.0.0

[windows:vars]
ansible_user=Administrator 
ansible_password=YourStrongPassword123 #complex password is mandatory
ansible_connection=winrm
ansible_winrm_transport= ntlm #ntlm required for windows-enterprise
ansible_winrm_server_cert_validation=ignore
ansible_port=5985
```

---

## Getting Started with Ansible

Once WinRM is verified and open, you can use the Ansible playbooks in this repository to run the ansible command:

- ansible-playbook -i inventory.ini main.yml


---

> **Important**: This WinRM setup uses **unencrypted basic authentication**, which is only recommended for **lab/testing environments**. For production use, configure WinRM over HTTPS with valid certificates.

---
