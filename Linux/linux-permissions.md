
# Understanding Permissions in Linux

Linux uses a permission model to control how users and groups access files and directories. These permissions determine who can read, write, or execute a file.

## 1. File Permission Basics

Each file has three types of permissions:

- **Read (r)**: Allows reading the contents of a file.
- **Write (w)**: Allows modifying the contents of a file.
- **Execute (x)**: Allows executing the file as a program.

These permissions apply to three categories of users:

- **Owner**: The user who owns the file.
- **Group**: Users who are in the same group as the file.
- **Others**: All other users.

Example output of `ls -l`:

```bash
-rwxr-xr-- 1 user group 1234 Jul 20 10:00 myfile.sh
```

This means:
- Owner: `rwx` (read, write, execute)
- Group: `r-x` (read, execute)
- Others: `r--` (read only)

## 2. Changing Permissions

### `chmod` – Change file permissions

```bash
chmod u+x script.sh     # Add execute to owner
chmod g-w myfile.txt    # Remove write from group
chmod o=r file.txt      # Set others to read-only
chmod 755 myfile.sh     # Equivalent to rwxr-xr-x
```

### `chown` – Change file owner

```bash
chown username file.txt             # Change owner
chown username:groupname file.txt   # Change owner and group
```

### `chgrp` – Change group

```bash
chgrp groupname file.txt
```

## 3. Numeric Permission Representation

Each permission has a numeric value:
- Read (r) = 4
- Write (w) = 2
- Execute (x) = 1

Examples:
- `chmod 777` → rwxrwxrwx
- `chmod 644` → rw-r--r--

## 4. Special Permission Bits

- **Setuid (s)**: Allows users to run an executable with the file owner's permissions.
- **Setgid (s)**: Files created in the directory inherit the group ID.
- **Sticky Bit (t)**: Users can only delete their own files in a directory.

```bash
chmod +s /path/to/file     # Setuid
chmod g+s /path/to/dir     # Setgid
chmod +t /path/to/dir      # Sticky bit
```

## 5. Viewing Permissions

```bash
ls -l             # Long listing with permissions
stat file.txt     # Detailed information
```

## Summary

| Command     | Description                       |
|-------------|-----------------------------------|
| chmod       | Change file permissions           |
| chown       | Change file owner/group           |
| chgrp       | Change group                      |
| ls -l       | View permissions                  |
| stat        | Show detailed file info           |

Proper management of permissions is essential for security and functionality in Linux systems.
