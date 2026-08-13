# Docker — From Basics to Expert

## Core Concepts
- **Container**: A lightweight, standalone, executable package that includes everything needed to run software (code, runtime, system tools, libraries, settings).
- **Image**: A read-only template with instructions for creating a container. Built in layers; each instruction in a Dockerfile creates a layer.
- **Dockerfile**: A text file with instructions (FROM, RUN, COPY, CMD, ENTRYPOINT, EXPOSE) to build an image.
- **Docker Daemon (dockerd)**: Background service that manages containers, images, networks, and volumes on the host.
- **Docker Client (docker CLI)**: The primary user interface to talk to the daemon via REST API or Unix socket.
- **Docker Registry**: A repository for storing and distributing images (Docker Hub, ECR, GCR, private registries).
- **Docker Compose**: Define and run multi-container applications with a single YAML file.
- **Docker Swarm**: Native clustering and orchestration built into Docker (mostly superseded by Kubernetes).
- **Container vs VM**: Containers share the host OS kernel (no guest OS), making them lighter and faster to start than VMs.
- **OCI (Open Container Initiative)**: Standard for container image format and runtime; Docker images are OCI-compliant.

## Dockerfile Best Practices
- **Use official base images** with explicit tags (e.g., `FROM node:20-alpine`) — never `latest` in production.
- **Prefer multi-stage builds** to keep the final image small (build in one stage, copy artifacts to a slim runtime stage).
- **Leverage layer caching**: Order Dockerfile instructions from least to most frequently changing (copy package manifests before source code).
- **Combine RUN commands** with `&&` and clean up package caches in the same layer to reduce image size.
- **Use `.dockerignore`** to exclude `node_modules`, `.git`, build artifacts, and secrets from the build context.
- **Run as non-root**: Create a user (`USER node`) to improve security and reduce attack surface.
- **Use `COPY` over `ADD`** unless you need URL/archive auto-extraction; COPY is more predictable.
- **Set `EXPOSE`** only for documentation; it does not actually publish ports.
- **Pin dependencies** with lockfiles (package-lock.json, go.sum, requirements.txt) for reproducible builds.
- **Use `HEALTHCHECK`** instruction to define commands Docker uses to check container health.
- **Use `ARG` for build-time variables** and `ENV` for runtime environment variables.
- **Avoid storing secrets in images** — use Docker secrets, build args (carefully), or external secret management.

## Image & Registry Management
- **Tag images meaningfully**: `myapp:1.2.3`, `myapp:sha-<commit>`, plus `latest` for convenience (not for production).
- **Push/pull images**: `docker push <repo>:<tag>`, `docker pull <repo>:<tag>`.
- **Docker Hub rate limits**: Anonymous pulls are limited; use a registry with auth or a paid plan for CI.
- **Image size matters**: Smaller images = faster pulls, lower bandwidth, less attack surface (use Alpine, distroless).
- **Distroless images**: Contain only the runtime and app, no shell/package manager — more secure but harder to debug.
- **Scan images for vulnerabilities**: `docker scan` (Snyk), Trivy, Anchore, Clair.
- **Sign images** with Docker Content Trust (DCT) or cosign for supply chain security.
- **Multi-platform builds**: `docker buildx build --platform linux/amd64,linux/arm64` to support multiple architectures.
- **Layer inspection**: `docker history <image>` shows layers and sizes; `docker image inspect` shows metadata.
- **Prune unused resources**: `docker system prune`, `docker image prune`, `docker builder prune` to reclaim disk space.

## Container Lifecycle
- **Run**: `docker run -d -p 8080:80 --name web nginx` (detached, port mapping, name).
- **Start/Stop**: `docker start|stop|restart <container>` — stop sends SIGTERM then SIGKILL after timeout.
- **Pause/Unpause**: `docker pause` freezes processes using SIGSTOP (useful for debugging or consistent snapshots).
- **Exec**: `docker exec -it <container> /bin/sh` — run a command in a running container (debugging).
- **Logs**: `docker logs -f --tail 100 <container>` — view and follow logs; use `--since` for time filtering.
- **Attach**: `docker attach` connects to the main process's stdin/stdout/stderr (not the same as exec).
- **Inspect**: `docker inspect <container>` returns detailed JSON (IP, mounts, env, health status, exit code).
- **Stats**: `docker stats` shows live CPU/memory/network/disk usage per container.
- **Top**: `docker top <container>` shows running processes inside the container.
- **Wait**: `docker wait <container>` blocks until the container stops and returns its exit code.
- **Copy**: `docker cp <container>:/path /local/path` to copy files in/out of containers.
- **Remove**: `docker rm -f <container>` forces removal; use `docker rm $(docker ps -aq)` to remove all stopped containers.
- **Exit codes**: 0 = success, 125 (daemon error), 126 (command cannot run), 127 (command not found), 137 (SIGKILL/OOM), 143 (SIGTERM).

## Networking
- **Bridge network (default)**: Containers get their own IP on a private subnet; port mapping via `-p` publishes to host.
- **Host network**: Container shares the host's network stack (no isolation, best performance, `--network host`).
- **None network**: No network access; useful for isolation (`--network none`).
- **User-defined bridge**: Enables DNS-based service discovery between containers (container name as hostname).
- **Overlay network**: For multi-host networking, used by Swarm/Kubernetes; enables cross-host container communication.
- **Port publishing**: `-p 8080:80` maps host 8080 to container 80; `-p 127.0.0.1:8080:80` binds to localhost only.
- **DNS**: Docker has an embedded DNS at 127.0.0.11; containers on the same user-defined network resolve each other by name.
- **Network isolation**: `--network` flag, or use `--internal` to prevent external access.
- **Exposed vs published**: EXPOSE in Dockerfile is documentation; `-p`/`--publish` actually makes ports reachable.
- **Network inspection**: `docker network ls`, `docker network inspect <net>`, `docker network connect|disconnect`.

## Volumes & Storage
- **Named volumes**: `-v mydata:/data` — managed by Docker, survive container removal, stored in `/var/lib/docker/volumes`.
- **Bind mounts**: `-v /host/path:/container/path` — direct host directory mapping (not portable, permissions matter).
- **tmpfs mounts**: `--mount type=tmpfs,destination=/app` — in-memory storage, lost on stop (fast, for ephemeral data).
- **Volume vs Bind mount**: Volumes are Docker-managed and portable; bind mounts expose host files directly.
- **Volume drivers**: Support NFS, S3 (via plugins), and cloud storage for remote/shared volumes.
- **Data persistence pattern**: Database data in named volumes; config via bind mounts or env vars; cache in tmpfs.
- **Backup/restore volumes**: `docker run --rm -v mydata:/data -v $(pwd):/backup alpine tar czf /backup/data.tar.gz /data`.
- **Volume ownership**: Containers run as non-root may need `--user` or chown to access volume files.
- **Read-only filesystems**: `--read-only` + tmpfs for `/tmp` to harden containers.
- **Storage drivers**: overlay2 (default), aufs, devicemapper, btrfs — know they affect performance and disk usage.

## Docker Compose
- **Compose file**: `docker-compose.yml` defines services, networks, volumes, and dependencies.
- **Services**: Each top-level service maps to one container (or a scaled set).
- **Healthchecks in Compose**: Define `healthcheck` per service; `depends_on` with `condition: service_healthy` for ordering.
- **Environment**: `environment:` list/map or `env_file:` for environment variables.
- **Ports vs expose**: `ports:` publishes to host; `expose:` only internal to the compose network.
- **Volumes**: Top-level `volumes:` section defines named volumes; can also use bind mounts.
- **Networks**: Top-level `networks:` section; services attach to one or more networks for isolation.
- **Profiles**: `profiles:` on services to conditionally start only some services (e.g., dev vs prod tools).
- **Scaling**: `docker compose up --scale worker=3` runs multiple replicas (load-balanced by the network).
- **Overrides**: `docker-compose.override.yml` automatically merges for local dev; use `-f` for explicit files.
- **Common commands**: `up -d`, `down`, `ps`, `logs -f`, `exec`, `config` (validate), `build`, `pull`.
- **Version field**: Modern Compose ignores `version`; the schema is based on the engine version.

## Orchestration & Production
- **Scheduling principles**: Containers are ephemeral; treat them as cattle, not pets.
- **Kubernetes vs Swarm vs Compose**: K8s for complex production orchestration; Swarm for simple clusters; Compose for single-host/multi-service dev.
- **Resource limits**: Always set `--memory` and `--cpus` (or in Compose `mem_limit`, `cpus`) to prevent noisy neighbors.
- **OOM behavior**: If a container exceeds memory limit, the kernel OOM-killer kills it (exit 137); set `--oom-kill-disable` carefully.
- **Restart policies**: `--restart unless-stopped|always|on-failure` — essential for production reliability.
- **Graceful shutdown**: Handle SIGTERM in your app (e.g., close DB connections, finish in-flight requests) for clean stops.
- **Logging drivers**: `--log-driver json-file` (default), `syslog`, `fluentd`, `awslogs`, `gelf`, `journald`, `none`.
- **Log rotation**: `--log-opt max-size=10m --log-opt max-file=3` to prevent disk exhaustion from logs.
- **PID namespace**: `--pid host` shares host PID namespace (for debugging); `--pid container:x` shares another container's.
- **Capabilities**: `--cap-drop ALL --cap-add NET_BIND_SERVICE` for least-privilege security.
- **Seccomp/AppArmor**: Apply security profiles to restrict syscalls and network access.
- **Read-only + tmpfs**: Combine `--read-only` with tmpfs mounts for `/tmp`, `/run`, and app-specific writable dirs.
- **Init process**: Use `--init` (tini) in containers to properly reap zombie processes and forward signals.
- **Health checks**: `HEALTHCHECK CMD curl -f http://localhost/ || exit 1` — critical for orchestrators to route traffic.
- **Container orchestration concepts**: Desired state, reconcilers, service discovery, rolling updates, and auto-healing.

## Debugging & Troubleshooting
- **Cannot connect to daemon**: Check `DOCKER_HOST`, socket permissions, or that dockerd is running.
- **Container exits immediately**: Check logs (`docker logs`), entrypoint, and exit code; test command manually.
- **Port already in use**: `sudo lsof -i :<port>` or `sudo ss -tlnp | grep <port>` to find the conflict.
- **Image not found**: Check tag spelling, registry, or pull access (auth).
- **Disk full**: `docker system df` shows usage; prune images, build cache, and stopped containers.
- **DNS issues**: `docker run --dns 8.8.8.8` to override; check embedded DNS for custom networks.
- **Slow builds**: Leverage caching, use BuildKit (`DOCKER_BUILDKIT=1`), and minimize context size.
- **Container unreachable**: Verify network, published ports, firewall, and that the app binds to 0.0.0.0 (not 127.0.0.1).
- **Zombie processes**: Use `--init` or a proper init/supervisor in the container.
- **Permission denied**: Check bind mount permissions, non-root user, and SELinux/AppArmor contexts (`:z`/`:Z` in SELinux).
- **Debugging tips**: `docker exec` into container, `docker inspect` for config, `docker logs` for app output, `docker stats` for resource usage.