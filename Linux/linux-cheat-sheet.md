# Linux Cheat Sheet

## File and Directory Commands

| **Command**        | **Description**                                 |
| ------------------ | ----------------------------------------------- |
| `ls`              | List files and directories                     |
| `ls -a`           | List all files, including hidden files         |
| `cd directory`    | Change to the specified directory              |
| `pwd`             | Show the current working directory             |
| `mkdir directory` | Create a new directory                         |
| `rmdir directory` | Remove an empty directory                      |
| `rm file`         | Remove a file                                  |
| `rm -r directory` | Remove a directory and its contents recursively|
| `cp source dest`  | Copy files or directories                      |
| `mv source dest`  | Move or rename files or directories            |
| `touch file`      | Create an empty file                           |

## File Viewing and Editing

| **Command**           | **Description**                                  |
| --------------------- | ------------------------------------------------ |
| `cat file`           | Display the contents of a file                  |
| `less file`          | View a file one screen at a time                |
| `head file`          | Display the first 10 lines of a file            |
| `tail file`          | Display the last 10 lines of a file             |
| `nano file`          | Edit a file using the Nano text editor          |
| `vi file`            | Edit a file using the Vi text editor            |
| `grep 'text' file`   | Search for 'text' in a file                     |
| `wc file`            | Count lines, words, and characters in a file    |

## User Management

| **Command**          | **Description**                                 |
| -------------------- | ----------------------------------------------- |
| `whoami`            | Show the current logged-in user                 |
| `id`                | Display user ID and group ID                    |
| `who`               | Show who is logged in                          |
| `adduser user`      | Add a new user                                  |
| `passwd user`       | Change the password for a user                  |
| `deluser user`      | Delete a user                                   |
| `su user`           | Switch to another user                         |

## Process Management

| **Command**         | **Description**                                 |
| ------------------- | ----------------------------------------------- |
| `ps`               | Display currently running processes             |
| `top`              | Show real-time system resource usage            |
| `kill PID`         | Terminate a process by its PID                  |
| `killall name`     | Terminate all processes with the specified name |
| `jobs`             | List background jobs                           |
| `bg`               | Resume a job in the background                 |
| `fg`               | Resume a job in the foreground                 |

## Networking Commands

| **Command**         | **Description**                                 |
| ------------------- | ----------------------------------------------- |
| `ifconfig`         | Display network interface information           |
| `ip addr`          | Show IP address information                     |
| `ping host`        | Send ICMP echo requests to test connectivity    |
| `netstat -tuln`    | Show listening ports and active connections     |
| `curl URL`         | Fetch a URL using HTTP                          |
| `wget URL`         | Download files from a URL                       |

## Permissions

| **Command**             | **Description**                              |
| ----------------------- | -------------------------------------------- |
| `chmod 777 file`       | Change permissions of a file or directory    |
| `chown user file`      | Change ownership of a file or directory      |
| `chgrp group file`     | Change group ownership of a file             |

## Disk Management

| **Command**             | **Description**                              |
| ----------------------- | -------------------------------------------- |
| `df -h`               | Show disk space usage                        |
| `du -sh directory`    | Show size of a directory                     |
| `mount device dir`    | Mount a device to a directory                |
| `umount dir`          | Unmount a device                             |
