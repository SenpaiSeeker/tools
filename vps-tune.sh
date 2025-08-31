set -e
[[ $EUID -ne 0 ]] && { printf "Run as root\n"; exit 1; }

backup_dir="/root/vps-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"
cp /etc/sysctl.conf "$backup_dir/" 2>/dev/null || true
cp -r /etc/sysctl.d/ "$backup_dir/" 2>/dev/null || true

cat > /etc/sysctl.d/99-memory.conf <<EOF
vm.swappiness = 1
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.vfs_cache_pressure = 50
vm.min_free_kbytes = 65536
vm.zone_reclaim_mode = 0
kernel.sched_migration_cost_ns = 5000000
EOF

cat > /etc/sysctl.d/99-network.conf <<EOF
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 30000
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 8192 262144 134217728
net.ipv4.tcp_wmem = 8192 262144 134217728
net.ipv4.tcp_max_syn_backlog = 30000
net.ipv4.tcp_max_tw_buckets = 2000000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 10
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.ip_local_port_range = 1024 65535
fs.file-max = 2097152
EOF

modprobe tcp_bbr 2>/dev/null || true
printf "tcp_bbr\n" >> /etc/modules-load.d/modules.conf

cat > /etc/sysctl.d/99-bbr.conf <<EOF
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_notsent_lowat = 16384
EOF

cat > /etc/security/limits.d/99-limits.conf <<EOF
* soft nofile 1048576
* hard nofile 1048576
* soft nproc 65535
* hard nproc 65535
EOF

for disk in $(lsblk -nd -o NAME | grep -E '^(sd|nvme|vd)'); do
    [[ -f /sys/block/$disk/queue/scheduler ]] && printf "mq-deadline\n" > /sys/block/$disk/queue/scheduler 2>/dev/null || true
done

cat > /etc/udev/rules.d/60-scheduler.rules <<EOF
ACTION=="add|change", KERNEL=="sd[a-z]|nvme[0-9]*n[0-9]*|vd[a-z]", ATTR{queue/scheduler}="mq-deadline"
EOF

sysctl --system >/dev/null 2>&1
[[ -x "$(command -v systemctl)" ]] && systemctl daemon-reload 2>/dev/null || true

printf "TCP BBR: $(sysctl -n net.ipv4.tcp_congestion_control 2>/dev/null)\n"
printf "Backup: $backup_dir\n"
printf "Reboot recommended\n"