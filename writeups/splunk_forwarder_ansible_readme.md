# Installing Splunk Universal Forwarder on Windows using Ansible

This guide provides step-by-step instructions to automate the installation and configuration of the Splunk Universal Forwarder on Windows machines using Ansible. The setup supports both Windows Server 2019 and Windows 11 Enterprise systems, deployed through WinRM.

## Prerequisites

Ansible control node (e.g., Ludus VM)

Target Windows machines accessible via WinRM

Required ports (5985, 9997, 8089) open on the firewall

Ansible inventory and role structure set up as described below

## Project Structure

ansible-script-forwarder-win2019/

## Inventory Configuration

Define Windows host groups and authentication in inventory.ini:

## Ansible Playbook

Defined in main.yml to apply the role to both Windows Server and Enterprise machines:

## Default Role Variables (defaults/main.yml)

## Tasks Overview (tasks/main.yml)

### 1. Enable the Administrator Account

### 2. Ensure Download Directory Exists

### 3. Download Splunk Forwarder MSI if Missing

### 4. Unblock the Downloaded MSI

### 5. Install Splunk Forwarder Silently

Note: This command installs the Splunk Universal Forwarder. The deployment client configuration is separated into templates/deploymentclient.conf.j2, which must be present for successful installation. Missing this file or misplacing its configuration can result in installation errors. Additionally, ensure become: yes, become_method: runas, and become_user: Administrator are set to avoid permission issues.

### 6. Verify Installation

### 7. Deploy Configuration Files

#### outputs.conf (templates/outputs.conf.j2):

#### deploymentclient.conf (templates/deploymentclient.conf.j2):

### 8. Start and Enable Splunk Forwarder Service

## Handler (handlers/main.yml)

Restart the Splunk Forwarder when needed:

## Running the Playbook

From the project directory:

ansible-playbook -i inventory.ini main.yml

Make sure that the Windows machines are reachable via WinRM and the credentials are correct. The forwarder will install silently, connect to the configured search head and deployment server, and start forwarding logs automatically.