# Todo 
Add client config to DMZ server with vulhub.

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

```bash
ansible-playbook -i inventory.ini tasks/main.yml --ask-become
# If incorrect sudo password for kali add to inventory file or create vault in ansible for encrypted passwords
```

# After playbook runs
Velociraptor GUI is located at 10.3.10.2:8889
Default login information: admin:password
- Automatically installs client on the kali machine.
