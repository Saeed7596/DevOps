# Linux Cheat Sheet

## Help
| **Command**        | **Description**                                 |
| ------------------ | ----------------------------------------------- |
| `command --help`   | Help                                            |
| `man command`      | Manual Page                                     |
| `echo $SHEEL`      | Shell Type                                      |
| `echo Hi`          | Print to Screen                                 |
| `cat /etc/*release*` | Check OS Version                              |
| `dpkg --print-architecture` | Show CPU architect (arm or amd)        |
| `echo $?`            | If it returns 0, it means that the previous command was executed correctly. |

## File and Directory Commands
| **Command**        | **Description**                                 |
| ------------------ | ----------------------------------------------- |
| `ls`              | List files and directories                     |
| `ls -a`           | List all files, including hidden files         |
| `cd directory`    | Change to the specified directory              |
| `pwd`             | Show the current working directory             |
| `mkdir directory` | Create a new directory                         |
| `mkdir -p /tmp/iran/shiraz` | Make Directory Hierarchy             |
| `rmdir directory` | Remove an empty directory                      |
| `rm file`         | Remove a file                                  |
| `rm -r directory` | Remove a directory and its contents recursively|
| `cp source dest`  | Copy files or directories                      |
| `cp -r <SourceDirectory> <TargetDirectory>` | Copy Directory       |
| `mv source dest`  | Move or rename files or directories            |
| `touch file`      | Create an empty file                           |

## File Viewing and Editing
| **Command**           | **Description**                                  |
| --------------------- | ------------------------------------------------ |
| `cat file`           | Display the contents of a file                  |
| `cat > new_file.txt` Hi `Ctrl+D` | Add contents to file                |
| `> file`           | clear the content of file                       |
| `echo Hi > a.txt`  | Replace                                         |
| `echo Hi >> a.txt` | Append                                          |
| `less file`          | View a file one screen at a time                |
| `head file`          | Display the first 10 lines of a file            |
| `tail file`          | Display the last 10 lines of a file             |
| `nano file`          | Edit a file using the Nano text editor          |
| `vi file`            | Edit a file using the Vi text editor            |
| `grep 'text' file`   | Search for 'text' in a file                     |
| `diff file1 file2`   | Compare the difference of these files           |
| `wc file`            | Count lines, words, and characters in a file    |

* `cat error.log | grep "Database connection" > error.txt`
* `cat error.log | grep "Database connection" | wc -l`

## User Management
| **Command**         | **Description**                                |
| ------------------- | ---------------------------------------------- |
| `whoami`            | Show the current logged-in user                 |
| `id`                | Display user ID and group ID                    |
| `who`               | Show who is logged in                           |
| `adduser user`      | Add a new user                                  |
| `passwd user`       | Change the password for a user                  |
| `deluser user`      | Delete a user                                   |
| `addgroup group`    | Add a new group                                 |
| `useradd user`      | Add a new user with group                       |
| `su user`           | Switch to another user                          |

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
| `ping host`        | Send ICMP echo requests to test connectivity    |
| `netstat -tuln`    | Show listening ports and active connections     |
| `curl URL`         | Fetch a URL using HTTP                          |
| `wget URL`         | Download files from a URL                       |
| `ip addr`          | Show IP address information                     |
| `ip a`             | Show IP address information                     |
| `ip -c -br a`      | Better Show IP address information              |


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
| `df -Th`              | Show disk space usage                        |
| `du -sh directory`    | Show size of a directory                     |
| `mount device dir`    | Mount a device to a directory                |
| `umount dir`          | Unmount a device                             |

## Download
| **Command**                                                      | **Description** |
| ---------------------------------------------------------------- | --------------- |
| `curl http://www.some-site.com/some-file.txt -O`                 | Download file   |
| `wget http://www.some-site.com/some-file.txt -O some-file.txt`   | Download file   |

## Service
| **Command**               | **Description**                         |
| ------------------------- | --------------------------------------- |
| `/etc/systemd/system`     | Services location                       |
| `service httpd start`     | Start HTTPD Service                     |
| `systemctl start httpd`   | Start HTTPD Service                     |
| `systemctl stop httpd`    | Stop HTTPD Service                      |
| `systemctl status httpd`  | Check HTTPD Service Status              |
| `systemctl enable httpd`  | Configure HTTPD to start at startup     |
| `systemctl disable httpd` | Configure HTTPD to not start at startup |
| `systemctl daemon-reload` | Instructs systemd to reload all service files and update its internal configuration |
| `journalctl -fu httpd`    | Display logs                            |
| `dmesg`                   | Kernel logs                             |

## Package Manager
| **Command**               | **Description**                         |
| ------------------------- | --------------------------------------- |
| `rpm -i telnet.rpm`       | Install Package                         |
| `rpm -e telnet.rpm`       | Uninstall Package                       |
| `rpm -q openssh-server python3 ansible telnet` | Query Packages     |
| `rpm -qa`                 | List all installations                  |
| rpm -qa | grep ftp        | Query ftp package                       |
| `yum install ansible`     | Install Package                         |
| `yum remove ansible`      | Uninstall Package                       |
| `yum list installed`      | Lists all packages that are installed on your system |
| `/etc/yum.repos.d`        | Repository file location                |
