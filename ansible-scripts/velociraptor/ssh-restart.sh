ssh-keygen -R 10.3.99.1
ssh-keygen -R 10.3.10.3
ssh-keygen -R 10.3.66.2
ssh-keygen -R 10.3.10.1



ssh-copy-id -i ~/.ssh/ansible.pub debian@10.3.10.3
ssh-copy-id -i ~/.ssh/ansible.pub debian@10.3.10.1
ssh-copy-id -i ~/.ssh/ansible.pub debian@10.3.66.2
ssh-copy-id -i ~/.ssh/ansible.pub kali@10.3.99.1