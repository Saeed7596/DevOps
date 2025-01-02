# Docker Container Exit Codes

When a Docker container exits, it returns an **exit code**. These codes are crucial for debugging and understanding why a container stopped or failed. This document explains common exit codes and their meanings.

---

## **Common Docker Exit Codes**

| **Exit Code** | **Description**                                                                 |
|---------------|---------------------------------------------------------------------------------|
| `0`           | The container ran successfully and exited without any errors.                 |
| `1`           | Generic error: Indicates that the application inside the container encountered an error. |
| `2`           | Misuse of shell builtins (according to Bash standards).                        |
| `126`         | Command invoked cannot be executed (e.g., permission issues or command not found). |
| `127`         | Command not found: Indicates that the command or script inside the container is missing. |
| `128`         | Invalid argument to `exit`: The `exit` command received an invalid argument.   |
| `137`         | Container terminated due to `SIGKILL` (e.g., `docker kill` command or out-of-memory). |
| `139`         | Segmentation fault occurred inside the container.                              |
| `143`         | Container terminated due to `SIGTERM` (e.g., `docker stop` command).           |
| `255`         | Exit status out of range or application-specific error.                        |

---

## **Debugging Exit Codes**

### Exit Code `1`
- Indicates a generic error in the application.
- Check logs using:
  ```bash
  docker logs container_name
  ```

### Exit Code `126`
- Happens when a command is not executable.
- Common causes:
  - Missing chmod +x on scripts or executables.
  - Incorrect permissions in the container.
- Solution:
  ```bash
  chmod +x script.sh
  ```

### Exit Code `127`
- Occurs when a command inside the container cannot be found.
- Solutions:
  - Ensure the command or binary exists in the container's `PATH`.
  - Verify that dependencies are installed during the image build.

### Exit Code `137`
- Indicates that the container was killed by the system (e.g., out-of-memory issue).
- Solutions:
  - Allocate more memory to the container.
  - Use memory limits to prevent the system from overloading:
  ```bash
  docker run --memory="512m" container_name
  ```

### Exit Code `143`
- Occurs when the container receives a termination signal (SIGTERM).
- Often caused by:
  - Manual termination using docker stop.
  - Kubernetes or other orchestration tools stopping the container.
