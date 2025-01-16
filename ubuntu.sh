#!/bin/bash

# Step 1: Perbarui Termux dan Instal Dependensi
echo "📦 Memperbarui Termux dan menginstal dependensi utama..."
pkg update && pkg upgrade -y
pkg install proot-distro git curl wget -y

# Step 2: Instal Ubuntu Menggunakan proot-distro
echo "🐧 Menginstal Ubuntu di Termux..."
proot-distro install ubuntu

# Step 3: Tambahkan Login Otomatis ke Ubuntu Saat Termux Dibuka
echo "🔗 Menambahkan otomatisasi login Ubuntu..."
if ! grep -q "proot-distro login ubuntu" ~/.bashrc; then
    echo "proot-distro login ubuntu" >> ~/.bashrc
fi

# Step 4: Masuk ke Ubuntu dan Jalankan Instalasi
echo "➡️ Masuk ke Ubuntu dan memulai instalasi perangkat lunak..."
proot-distro login ubuntu <<EOF
echo '📦 Memperbarui paket di Ubuntu...'
apt update && apt upgrade -y

echo '🔧 Menginstal alat bantu...'
apt install -y curl wget software-properties-common

echo '🐍 Menginstal Python3, pip3, dan virtualenv...'
apt install -y python3 python3-pip python3-venv

echo '🌐 Menginstal Node.js dan npm...'
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

echo '🔧 Menginstal Git dan build-essential...'
apt install -y git build-essential

echo '✅ Semua perangkat lunak berhasil diinstal!'
EOF

# Step 5: Pesan Selesai
echo "🎉 Instalasi selesai! Setiap kali membuka Termux, Anda akan otomatis masuk ke Ubuntu."
