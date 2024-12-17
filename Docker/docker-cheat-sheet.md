# Docker Cheat Sheet

## Container Management

| **Command**                         | **Description**                           |
| ----------------------------------- | ----------------------------------------- |
| `docker ps`                         | List running containers                   |
| `docker ps -a`                      | List all containers (running and stopped) |
| `docker ps -s`                      | List containers with their size           |
| `docker start container_name`       | Start a stopped container                 |
| `docker stop container_name`        | Stop a running container                  |
| `docker restart container_name`     | Restart a container                       |
| `docker rm container_name`          | Remove a stopped container                |
| `docker rm -f container_name`       | Force remove a running container          |
| `docker rm -f $(docker ps -a -q)`   | Force remove all containers               |
| `docker logs container_name`        | Show logs of a container                  |
| `docker logs -f -t container_name`  | Show and follow logs with timestamps      |
| `docker exec -it container_name sh` | Run a shell inside a running container    |
| `docker exec -it container_name /bin/bash` | Run Bash inside a running container (use `bash` if available) |
| `docker attach container_name`      | Attach to a running container             |
| `docker cp source_path dest_path`   | Copy files/folders between host and container |
| `docker pause container_name`       | Pause all processes in a container        |
| `docker unpause container_name`     | Unpause a paused container                |
| `docker rename old_name new_name`   | Rename a container                        |

### Docker Attach vs Exec
- **`docker attach container_name`**: Attaches to the container's main process and allows interaction as if you were inside the container. 
  - To exit, use `Ctrl+P+Q` (detaches without stopping the container).
  - **Note**: Exiting with `Ctrl+C` or `Ctrl+D` stops the container.
- **`docker exec -it container_name sh`**: Runs a new command or shell in an already running container without interfering with the main process.

## Image Management

| **Command**                      | **Description**                   |
| -------------------------------- | --------------------------------- |
| `docker images`                  | List all local images             |
| `docker pull image_name`         | Download an image from a registry |
| `docker build -t image_name .`   | Build an image from a Dockerfile  |
| `docker rmi image_name`          | Remove an image                   |
| `docker tag image_name new_name` | Tag an image with a new name      |
| `docker history image_name`      | Show history of an image          |
| `docker save image_name -o file.tar` | Save an image to a tar archive     |
| `docker load -i file.tar`        | Load an image from a tar archive  |
| `docker commit container_name new_image_name` | Create a new image from a container’s changes |

## Docker Compose

| **Command**                      | **Description**                                |
| -------------------------------- | ---------------------------------------------- |
| `docker compose up`              | Start services defined in `docker-compose.yml` |
| `docker compose up -d`           | Start services in detached mode                |
| `docker compose down`            | Stop and remove all services                   |
| `docker compose ps`              | List all services managed by Compose           |
| `docker compose logs`            | Show logs for all services                     |
| `docker compose exec service sh` | Run a shell inside a service                   |
| `docker compose pause`           | Pause all services defined in Compose          |
| `docker compose unpause`         | Unpause all paused services in Compose         |

## Volume and Network Management

| **Command**                          | **Description**      |
| ------------------------------------ | -------------------- |
| `docker volume ls`                   | List all volumes     |
| `docker volume rm volume_name`       | Remove a volume      |
| `docker network create network_name` | Create a new network |

## Inspect and Debug

| **Command**                     | **Description**                                  |
| ------------------------------- | ------------------------------------------------ |
| `docker inspect container_name` | Show detailed information about a container      |
| `docker inspect image_name`     | Show detailed information about an image         |
| `docker stats`                  | Display live resource usage stats for containers |
| `docker top container_name`     | Display processes running inside a container     |
| `docker system df`              | Show disk usage by Docker resources              |
| `docker events`                 | Show real-time events from the Docker daemon     |

## Prune and Clean Up

| **Command**            | **Description**                                |
| ---------------------- | ---------------------------------------------- |
| `docker system prune`  | Remove unused containers, networks, and images |
| `docker builder prune` | Remove unused build cache                      |
| `docker volume prune`  | Remove unused volumes                          |
| `docker network prune` | Remove unused networks                         |
| `docker image prune`   | Remove unused images                           |

## Export and Import

| **Command**                   | **Description**                            |
| ----------------------------- | ------------------------------------------ |
| `docker export container_name -o file.tar` | Export a container’s filesystem as a tar archive |
| `docker import file.tar new_image_name`    | Import a tar archive as a new image           |

## Useful Options

| **Option**                    | **Description**                            |
| ----------------------------- | ------------------------------------------ |
| `-d`                          | Run in detached mode                       |
| `-it`                         | Interactive terminal                       |
| `--name container_name`       | Assign a name to the container             |
| `-p host_port:container_port` | Map host port to container port            |
| `--rm`                        | Automatically remove the container on exit |
| `-v host_dir:container_dir`   | Mount a volume from host to container      |

