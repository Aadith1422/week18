# Linux Server Monitoring & Maintenance + Automated Backup

This README gives you a practical toolkit to **monitor, maintain, and back up** a Linux server.
It includes:
- A **field-tested command cheat‑sheet** for health checks and troubleshooting
- A **daily/weekly maintenance checklist**
- A **production‑ready `backup.sh`** script with logging, rotation, and integrity checks

---

## 1) Quick Health Checks (copy/paste friendly)

**System overview**  
```bash
uptime -p && uptime           # load averages + how long up
hostnamectl                   # distro, kernel, virtualization
who -a                        # logged in sessions
timedatectl                   # NTP status
```

**CPU & processes**  
```bash
top -H -o %CPU                # live; '1' to show all CPUs
htop                          # nicer top (install: apt install htop | dnf install htop)
vmstat 1 5                    # run-queue, context switches, interrupts
mpstat -P ALL 1 5             # per‑CPU usage (sysstat)
pidstat 1 5                   # per‑process stats (sysstat)
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head
nice/renice/ionice            # adjust priorities
```

**Memory**  
```bash
free -h                       # RAM and swap
grep -i oom /var/log/* 2>/dev/null | tail -n 20
cat /proc/meminfo | egrep 'Mem|Swap'
```

**Disk & filesystem**  
```bash
lsblk -f                      # devices, filesystems, mount points
df -hT                        # usage by filesystem
du -h -d1 /var | sort -h     # biggest dirs (depth 1)
iostat -xz 1 5                # disk util, iowait (sysstat)
dmesg -T | egrep -i 'error|fail|nvme|ext4|xfs|md|raid' | tail
smartctl -H /dev/sda          # SMART health (smartmontools)
```

**Network**  
```bash
ip -br addr && ip -br link
ss -tulpn | head              # listening sockets
ss -s                         # summary (TCP states)
ping -c 4 1.1.1.1             # basic reachability
mtr -rw example.com           # path quality (install: mtr)
iftop / nload                 # live bandwidth (install)
journalctl -u NetworkManager --since "1 hour ago" | tail
```

**Services & logs**  
```bash
systemctl --failed
systemctl status <unit>.service
journalctl -u <unit>.service --since "1 hour ago"
journalctl -p 3 -b           # errors since last boot
logrotate -d /etc/logrotate.conf  # dry‑run check
```

**Packages & security**  
```bash
# Debian/Ubuntu
sudo apt update && sudo apt -y upgrade
sudo unattended-upgrades --dry-run --debug || true

# RHEL/CentOS/Rocky/Alma
sudo dnf check-update && sudo dnf -y upgrade

ufw status verbose  # or: firewall-cmd --state && firewall-cmd --list-all
fail2ban-client status || true
last -n 10          # login history
```

---

## 2) Routine Maintenance Checklist

**Daily**
- Check `systemctl --failed`, `journalctl -p 3 -b`, disk free `df -hT`, and load `uptime`.
- Ensure backups completed: verify latest archive and log in `/var/log/backup` (see script below).
- Inspect security: `last`, `ss -tulpn`, firewall status.

**Weekly**
- Review log growth and rotate: `du -h /var/log | sort -h`, confirm logrotate.
- Patch the system; reboot if kernel updated.
- Scrub disks/arrays if applicable (ZFS/Btrfs/MD RAID procedures).

**Monthly**
- Test **full restore** from backups into a scratch directory/VM.
- Validate SMART health for all disks; review capacity planning.
- Audit users, sudoers, SSH keys; rotate credentials if required.

---

## 3) Performance Triage Flow

1. **Load average high?** → `top`, `pidstat`, `mpstat`, look for CPU hogs; check I/O with `iostat -xz`.
2. **Memory pressure?** → `free -h`, swap in use, OOM in logs, cache vs anon usage.
3. **Disk latency?** → queue size and await in `iostat -xz`, filesystem errors in `dmesg -T`.
4. **Network slowness?** → `mtr`, `ss -s`, packet loss, retransmits.
5. **Service issues?** → `systemctl status`, `journalctl -u <svc>`, restart with caution.

---

## 4) Automated Backup Script

The provided `backup.sh` supports:
- **Rsync‑based incremental backups** into date‑stamped folders
- **Optional tar.gz snapshots** (set `SNAPSHOT=true`)
- **Retention policy** (keep N daily backups)
- **Locking** to avoid overlapping runs
- **Detailed logs** in `/var/log/backup/`
- **Basic integrity check** (size + file count)

### Usage

1. Edit variables at the top of `backup.sh`:
   - `SOURCE_DIR` — directory you want to back up (e.g., `/var/www`)
   - `DEST_ROOT` — where backups should be stored (local path or mounted drive)
2. Make executable:
   ```bash
   chmod +x backup.sh
   ```
3. Run manually:
   ```bash
   sudo ./backup.sh
   ```
4. Schedule daily at 02:30 via cron:
   ```bash
   sudo crontab -e
   # Add line:
   30 2 * * * /path/to/backup.sh >> /var/log/backup/backup.cron.log 2>&1
   ```

### Restore (rsync mode)
```bash
# pick a dated folder under $DEST_ROOT (e.g., 2025-09-30)
rsync -aHAXP /backups/2025-09-30/ /restore/target/
```

### Restore (snapshot .tar.gz mode)
```bash
mkdir -p /restore/target
tar -xpf /backups/archives/backup-2025-09-30.tar.gz -C /restore/target
```

---

## 5) Hardening & Good Practices

- Use **SSH keys** (+ `PubkeyAuthentication yes`, disable password auth if possible).
- Enforce **least privilege**; separate service accounts.
- Enable **automatic security updates** and **reboot notifications**.
- Keep **/var** and **/home** on separate partitions where sensible.
- Back up **databases** with native tools (e.g., `mysqldump`, `pg_dump`) then include dumps in file backups.
- Monitor with: **node_exporter + Prometheus + Grafana**, or lightweight agents (Netdata, Glances).

---

## 6) Files in this bundle

- `README.md` (this guide)
- `backup.sh` (the automation script)
- `linux-server-maintenance-and-backup.zip` (packed for easy download)

Happy maintaining! :)