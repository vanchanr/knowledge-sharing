# Linux — From Basics to Expert

- find a process running on a port and kill
```
$ sudo lsof -i :8000
$ sudo kill <PID>
```

---

## Core Concepts
- **Kernel vs user space**: The kernel manages hardware/resources and provides syscalls; applications run in user space — with syscalls as the boundary.
- **File as everything**: Everything in Linux is a file (regular files, directories, devices, sockets, pipes) — unified abstraction via file descriptors.
- **Everything is a file**: Files, dirs, `/dev` devices, `/proc` virtual files, pipes, sockets — unified via the VFS (Virtual File System).
- **FHS (Filesystem Hierarchy Standard)**: `/bin`, `/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/opt`, `/proc`, `/sys`, `/dev` — conventional locations for specific file types.
- **Process model**: PID, PPID, parents/children — processes are forked (clone) from parents; PID 1 (systemd/init) is the root of the process tree.
- **Permission model**: rwx permissions for user/group/others + special bits (setuid, setgid, sticky) — accessed via user/group IDs.
- **Root vs normal user**: root has full privileges (UID 0); best practice is least-privilege with `sudo`.
- **Signals**: Inter-process notifications — SIGTERM (15, graceful), SIGKILL (9, forced), SIGHUP (1, reload), SIGINT (2, Ctrl+C), SIGSTOP (19, pause).
- **Shell**: Command interpreter (bash, zsh, fish) — scripting, environment variables, pipes, job control.
- **Environment variables**: `PATH`, `HOME`, `USER`, `LANG`, `TZ` — inherited by child processes; `export` to expose them.

## Process Management
- **`ps`**: List processes — `ps aux` (all users, all processes), `ps -ef`, filter with `pgrep`/`ps aux | grep`.
- **`top`/`htop`**: Real-time process monitoring — CPU, memory, per-process; `htop` has nicer UX (F6 sort, F9 kill).
- **`kill`**: Send signals — `kill -15 <pid>` (SIGTERM, graceful), `kill -9 <pid>` (SIGKILL, force), `kill -l` lists signals.
- **`pkill`/`killall`**: Kill by name/pattern — `pkill -f "node server"` (match full command line).
- **`nohup`**: Run a process immune to HUP when the shell exits — `nohup ./app > app.log 2>&1 &`.
- **`&` and `bg`/`fg`**: Background/foreground job control — `jobs`, `bg %1`, `fg %1`.
- **`systemctl`**: Manage systemd services — `systemctl start|stop|restart|status|enable|disable <service>`.
- **`journalctl`**: View systemd logs — `journalctl -u <service>`, `journalctl -f` (follow), `journalctl --since "1 hour ago"`.
- **`daemon`**: Background service with no controlling terminal — systemd unit files vs old init scripts.
- **Linux process states**: Running (R), Sleeping (S), Uninterruptible sleep (D — often IO), Stopped (T), Zombie (Z).
- **Zombie process**: Child that terminated but wasn't reaped by parent — safe to leave small numbers; fix the parent process.
- **Finding a process on a port**: `lsof -i :8080`, `sudo ss -tlnp | grep :8080` — then kill by PID.
- **`nice`/`renice`**: Adjust process priority (−20 highest to 19 lowest) — influence CPU scheduling.

## File System & Disk
- **`df -h`**: Disk usage per mounted filesystem — watch for full disks.
- **`du -sh *`**: Directory sizes — find what's eating disk; `ncdu` for interactive browsing.
- **`ls -la`**: List files with permissions, owner, group, size, timestamps.
- **`find`**: Search files — `find / -name "*.log" -mtime +7` (older than 7 days), `-size +100M`, `-exec` to act on results.
- **`grep -r`**: Search file contents recursively — `grep -rn "pattern" /path`.
- **`rsync`**: Sync files locally/remotely — `-a` (archive), `-z` (compress), `-P` (progress), `--delete` (mirror), `--exclude`.
- **`tar`**: Archive/compress — `tar czvf archive.tar.gz dir/` (create), `tar xzvf archive.tar.gz` (extract).
- **`mount`/`umount`**: Attach/detach file systems — `mount /dev/sdb1 /mnt`, `umount /mnt`.
- **`fdisk`/`parted`**: Partition disks — create/delete partitions, check with `lsblk`.
- **`mkfs`**: Format a partition — `mkfs.ext4 /dev/sdb1`, `mkfs.xfs`.
- **`inode`**: Metadata structure for each file (permissions, owner, size, block pointers) — exhausted inodes cause "No space left on device" even with free blocks (`df -i`).
- **Hard links vs symlinks**: `ln` (hard link = same inode, same filesystem) vs `ln -s` (symlink = pointer to path, may break).
- **`lsof`**: Open files/processes — `lsof | grep deleted` (deleted but still-held files eating disk), `lsof -i :port`, `lsof -u user`.
- **Permissions**: `chmod 755 file` / `chmod u+x` (user execute), `chown user:group` (change owner).
- **setuid/setgid**: Allow a binary to run with the file owner's privileges (e.g., `passwd`) — security risk if misused.
- **Sticky bit**: `/tmp` — only the owner can delete in a shared writable directory.
- **`dd`**: Low-level copy/convert — `dd if=/dev/zero of=test.img bs=1M count=1000` (benchmark), disk imaging.
- **`iostat`**: I/O statistics per device — latency, utilization, queue depth.
- **`iotop`**: Real-time I/O usage per process — find I/O hogs.
- **Tuning**: `ulimit` (open files, core dumps), `vm.swappiness` (swap tendency), `fs.file-max`.

## Networking
- **`ip addr`**: Network interfaces and IP addresses — modern replacement for `ifconfig`.
- **`ss`**: Socket statistics — `ss -tlnp` (listening TCP + pid), `ss -unap` (UDP) — modern replacement for `netstat`.
- **`ping`**: ICMP reachability — latency/RTT; note ICMP can be blocked by firewalls.
- **`curl`**: HTTP API testing — `curl -v`, `-X POST`, `-H` headers, `-d` body, `-o` output, `-L` follow redirects.
- **`wget`**: Download files — recursive (`-r`), continue (`-c`), mirror websites.
- **`traceroute`/`mtr`**: Path to destination and per-hop latency — diagnose network routing.
- **`dig`/`nslookup`**: DNS queries — see resolved IP, CNAME chain, TTL; `dig @8.8.8.8 example.com`.
- **`nc` (netcat)**: Read/write TCP/UDP — port scanning (`nc -zv host port`), file transfer, debugging services.
- **`tcpdump`**: Capture packets — `tcpdump -i eth0 port 443`, `-c count`, `-w file.pcap` — deep packet analysis.
- **`hostname`/`hostnamectl`**: Set/view system hostname.
- **`iptables`/`nftables`**: Firewall rules — filter, NAT, port forward; modern: `nft`.
- **`firewalld`**: Higher-level firewall management — zones, services, rich rules.
- **`ssh`**: Secure remote shell — `ssh user@host`, key auth (`~/.ssh/id_rsa` → `authorized_keys`), `-p` port, `-L`/`-R` port forwarding.
- **`scp`/`sftp`**: Secure file transfer over SSH — `scp file user@host:/path`.
- **`curl` for local services**: Test if a local service responds — `curl localhost:8080/health`.
- **Loopback**: `localhost`/`127.0.0.1` (lo interface) — services bound to 127.0.0.1 are only reachable locally.

## Performance & Troubleshooting
- **`uptime`**: Load average (1/5/15 min) — high load ≠ high CPU necessarily (I/O wait counts too).
- **`free -h`**: Memory — total/used/cache; `available` is the reliable number; high `buff/cache` is fine (reclaimable).
- **`vmstat`**: System stats — r (runnable), b (blocked/IO), si/so (swap in/out — swapping is bad).
- **`iostat -x 1`**: Detailed per-device I/O — %util, await (latency), svctm; look for 100% util with high await.
- **`sar`**: Historical performance data — `sar -u`, `sar -r`, `sar -n DEV` if sysstat collection installed.
- **`strace`**: Trace syscalls — `strace -p <pid>`, `-e trace=network` — see what a process is actually doing.
- **`ltrace`**: Trace library calls — `ltrace -p <pid>` — deeper than strace.
- **`perf`**: Performance profiling — `perf top`, `perf record -g`, `perf report` — CPU sampling/profiling.
- **`gdb`**: Debugger — attach to process, backtrace crashes (`gdb -p <pid>`).
- **`dmesg`**: Kernel ring buffer — hardware errors, OOM kills, segfaults; `dmesg -T` (timestamps).
- **`lsof` on deleted files**: Processes holding deleted files keep disk space — found via `lsof | grep deleted`.
- **OOM killer**: Kernel kills processes when memory is exhausted — `dmesg | grep -i oom`, check `oom_score`.
- **`sysctl`**: Kernel tunables — `sysctl vm.swappiness=10`, `sysctl net.ipv4.ip_forward=1`, `--system` to persist.
- **`journalctl -p err`**: Show errors/warnings only — filter log severity.
- **`top -o %MEM`**: Sort processes by memory — find memory hogs.
- **`time`**: Measure command execution — `/usr/bin/time -v command` for detailed resource usage.
- **Log locations**: `/var/log/syslog`, `/var/log/messages`, `/var/log/auth.log` (auth), `/var/log/dmesg`, app logs in `/var/log/<app>`.

## Shell & Scripting
- **Basic scripting**: Shebang (`#!/bin/bash`), variables (`$VAR`), conditionals (`if`/`test`), loops (`for`, `while`), functions.
- **Exit status**: `$?` holds last command's exit code — 0 = success, non-zero = failure.
- **Pipes**: `command1 | command2` — stdout of one feeds stdin of the next; check `set -o pipefail` in scripts.
- **Redirection**: `>` (overwrite), `>>` (append), `2>` (stderr), `2>&1` (both), `&>` (both).
- **`xargs`**: Build and run commands from stdin — `find . -name "*.tmp" | xargs rm`.
- **`sed`**: Stream editor — `sed 's/old/new/g'`, `-i` (in-place), line deletion (`/pattern/d`).
- **`awk`**: Text processing — `awk '{print $1}'`, `awk -F, '{sum+=$3} END {print sum}'`.
- **`cut`/`sort`/`uniq`/`wc`**: Text utilities — `cut -d: -f1`, `sort -rn`, `uniq -c`, `wc -l`.
- **`jq`**: JSON processing — `curl ... | jq '.data[0].name'`, `jq '. | length'`.
- **`watch`**: Repeat a command — `watch -n 2 'ps aux | grep java'`.
- **`alias`**: Command shortcuts — `alias ll='ls -la'`; persistent in `~/.bashrc`/`~/.zshrc`.
- **`cron`**: Scheduled jobs — `crontab -e`, format: minute hour day month weekday command; use `-l` to list.
- **Background with log**: `nohup ./app > app.log 2>&1 &` — run detached with logs.
- **`tmux`/`screen`**: Terminal multiplexer — detach/reattach sessions, split panes — essential for long-running tasks over SSH.
- **`history`**: Command history — `!$` (last arg), Ctrl+R (reverse search).
- **`env`**: Show environment variables — inspect what the process sees.

## Security & Hardening
- **`ssh` hardening**: Disable root login (`PermitRootLogin no`), key-only auth, custom port, fail2ban.
- **`sudo`**: Grant limited root privileges — configure via `/etc/sudoers`.
- **`chroot`/containers**: Isolate processes — jails/namespaces via docker/systemd-nspawn.
- **`selinux`/`apparmor`**: Mandatory access control — confine processes beyond standard permissions.
- **Update policy**: `apt update && apt upgrade` / `dnf update` — patch regularly (kernel & packages).
- **Users/groups**: `useradd`, `usermod`, `groupadd`, `passwd` — create least-privilege service users.
- **`ufw`/`firewalld`**: Basic firewall — allow only necessary ports.
- **`auditd`**: Audit system events — file access, syscalls, logins — for compliance/forensics.
- **`openssl`**: Certificates & encryption — `openssl req -new -x509` (self-signed cert), checksums, TLS testing (`openssl s_client`).
- **`gpg`**: Encrypt/sign data and files.
- **Avoid running apps as root**: Run as service accounts with minimal permissions.
- **File integrity**: `sha256sum`/`md5sum` for file verification/checksum.
- **Secure file permissions**: Personal keys 600 (`~/.ssh/id_rsa`), sensitive configs 600, umask 022/027.

## Common Issues & Quick Fixes
- **"No space left on device"**: `df -h` full, or inodes full (`df -i`), or deleted-but-held files (`lsof | grep deleted`).
- **"Permission denied"**: Check file perms (`ls -la`), owner, SELinux context, mount options (noexec, ro).
- **Process stuck/high CPU**: `top -o %CPU`, `strace -p <pid>`, check logs — often I/O or infinite loop.
- **Service won't start**: `systemctl status <svc>`, `journalctl -u <svc> -n 50`, verify config file syntax.
- **Cannot reach a port**: Verify binding (`ss -tlnp`), firewall (`ufw status`), route, service health.
- **Too many open files**: `ulimit -n` limit — raise in `/etc/security/limits.conf`; find with `lsof | wc -l`.
- **High load but idle CPUs**: Likely I/O wait — check `iostat -x 1`, `vmstat` (b column), disk latency.
- **Swap usage climbing**: Memory pressure — `free -h`, find memory hogs, consider tuning `vm.swappiness`.
- **Cron job not running**: Check cron syntax, `PATH` (cron uses minimal PATH), permissions, logs (`/var/log/cron`).
- **Out of memory (OOM)**: Kernel killed a process — `dmesg | grep -i oom`, increase memory, add swap, or tune limits.
- **SSH too many authentication failures**: `fail2ban` or rate limit — check `/var/log/auth.log`.
- **Date/time wrong**: `timedatectl`, NTP sync (`chronyc` / `ntpdate`).