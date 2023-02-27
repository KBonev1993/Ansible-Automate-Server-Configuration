import os

# Define the inventory file
inventory_file = "inventory.ini"

# Define the playbook file
playbook_file = "playbook.yml"

# Define the backup directory
backup_dir = "/var/backup"

# Create the inventory file
inventory = """
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[databases]
db1 ansible_host=192.168.1.12
db2 ansible_host=192.168.1.13
"""

with open(inventory_file, "w") as f:
    f.write(inventory)

# Define the playbook
playbook = """
---
- name: Configure servers
  hosts: all
  become: yes
  tasks:
    - name: Update system packages
      apt:
        update_cache: yes
        upgrade: yes
      register: result

    - name: Create backup directory
      file:
        path: {0}
        state: directory
      when: result.changed

    - name: Backup server configuration
      command: tar czf {0}/{{ inventory_hostname }}-backup.tar.gz /etc
      when: result.changed

    - name: Install Apache web server
      apt:
        name: apache2
        state: present

    - name: Configure Apache web server
      template:
        src: apache.conf.j2
        dest: /etc/apache2/apache2.conf
      notify:
        - restart apache

  handlers:
    - name: restart apache
      service:
        name: apache2
        state: restarted
"""

with open(playbook_file, "w") as f:
    f.write(playbook)

# Execute the playbook
os.system("ansible-playbook -i {0} {1}".format(inventory_file, playbook_file))
