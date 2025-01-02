# Docker Restart Policies

This document explains the different `restart` policies available in Docker for container restart management.

## Available Restart Policies

### 1. `always`
- **Behavior:** The container is always restarted, regardless of the reason for its stop.
- **Use Case:** Suitable for services that should always be running, even after manual stops.

### 2. `unless-stopped`
- **Behavior:** The container will be restarted automatically unless it was manually stopped by the user (using `docker stop`).
- **Use Case:** Ideal when you want the container to auto-restart after crashes or reboots, but avoid restarting if the user manually stopped it.

### 3. `on-failure[:max-retries]`
- **Behavior:** The container will only restart if it exits with a failure (non-zero exit code). You can also limit the number of restart attempts by specifying `max-retries`.
- **Use Case:** Useful for containers that should only restart in case of a failure, and where you want to control the maximum number of retries.

Example:

```yaml
restart: on-failure:3
```

In this example, the container will restart up to 3 times if it encounters a failure.

## Comparison of Restart Policies

| Policy          | Behavior                                                      |
|-----------------|---------------------------------------------------------------|
| `no`            | Container does not restart automatically (default behavior).   |
| `always`        | Container always restarts, even after manual stop.             |
| `unless-stopped`| Container restarts unless manually stopped by the user.        |
| `on-failure`    | Container restarts only if it fails (non-zero exit code).      |
