echo -e "\033[38;2;0;0;255m📦 Memperbarui Termux dan menginstal dependensi utama...\033[0m"
pkg update && pkg upgrade -y
pkg install proot-distro -y

echo -e "\033[38;2;255;255;0m🐧 Menginstal Ubuntu di Termux...\033[0m"
proot-distro install ubuntu

if [ ! -f ~/.bashrc ]; then
    touch ~/.bashrc
fi

echo -e "\033[38;2;0;255;0m🔗 Menambahkan otomatisasi login Ubuntu...\033[0m"
if ! grep -q "proot-distro login ubuntu" ~/.bashrc; then
    echo -e "clear" >> ~/.bashrc
    echo -e "echo -e \"\033[38;2;0;0;255m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"\033[38;2;255;255;0m  🏴‍☠️  SELAMAT DATANG DI TERMUX  🏴‍☠️ \033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"\033[38;2;0;0;255m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"📌 \033[38;2;0;255;0mHostname:\033[0m \$(hostname)\"" >> ~/.bashrc
    echo -e "echo -e \"📅 \033[38;2;0;255;0mTanggal :\033[0m \$(date '+%d/%m/%Y %H:%M:%S')\"" >> ~/.bashrc
    echo -e "echo -e \"📂 \033[38;2;0;255;0mDirektori Kerja :\033[0m \$(pwd)\"" >> ~/.bashrc
    echo -e "echo -e \"💻 \033[38;2;255;255;0mCPU Cores: \033[0m \$(nproc)\"" >> ~/.bashrc
    
    echo -e "TOTAL_RAM_MB=\$(awk '/MemTotal/ {print \$2 / 1024}' /proc/meminfo | xargs printf \"%.0f\")" >> ~/.bashrc
    echo -e "AVAILABLE_RAM_MB=\$(awk '/MemAvailable/ {print \$2 / 1024}' /proc/meminfo | xargs printf \"%.0f\")" >> ~/.bashrc
    echo -e "USED_RAM_MB=\$((TOTAL_RAM_MB - AVAILABLE_RAM_MB))" >> ~/.bashrc
    echo -e "RAM_USAGE_PERCENT=\$(awk \"BEGIN {printf \\\"%.1f\\\", (\$USED_RAM_MB/\$TOTAL_RAM_MB) * 100}\")" >> ~/.bashrc
    echo -e "RAM_FREE_PERCENT=\$(awk \"BEGIN {printf \\\"%.1f\\\", (\$AVAILABLE_RAM_MB/\$TOTAL_RAM_MB) * 100}\")" >> ~/.bashrc
    
    echo -e "echo -e \"🧠 \033[38;2;255;255;0mRAM Total: \033[0m \${TOTAL_RAM_MB} MB\"" >> ~/.bashrc
    echo -e "echo -e \"📊 \033[38;2;255;255;0mRAM Digunakan: \033[0m \${USED_RAM_MB} MB (\${RAM_USAGE_PERCENT}%)\"" >> ~/.bashrc
    echo -e "echo -e \"📊 \033[38;2;255;255;0mRAM Tersisa: \033[0m \${AVAILABLE_RAM_MB} MB (\${RAM_FREE_PERCENT}%)\"" >> ~/.bashrc
    
    echo -e "echo -e \"\033[38;2;0;0;255m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"🛠 \033[38;2;255;255;0mGunakan perintah berikut untuk memulai:\033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"   🔹 \033[38;2;0;255;0mls\033[0m  - Menampilkan daftar file\"" >> ~/.bashrc
    echo -e "echo -e \"   🔹 \033[38;2;0;255;0mcd <folder>\033[0m - Masuk ke folder\"" >> ~/.bashrc
    echo -e "echo -e \"   🔹 \033[38;2;0;255;0mnano <file>\033[0m - Edit file\"" >> ~/.bashrc
    echo -e "echo -e \"   🔹 \033[38;2;0;255;0mexit\033[0m - Keluar dari Termux\"" >> ~/.bashrc
    echo -e "echo -e \"\033[38;2;0;0;255m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\"" >> ~/.bashrc
    echo -e "echo -e \"🚀 \033[38;2;255;255;0mMemasuki Ubuntu secara otomatis...\033[0m\"" >> ~/.bashrc
    echo "proot-distro login ubuntu" >> ~/.bashrc
fi

echo -e "\033[38;2;255;0;0m➡️ Masuk ke Ubuntu dan memulai instalasi perangkat lunak...\033[0m"
proot-distro login ubuntu -- bash -c "
    echo -e '\033[38;2;0;0;255m📦 Memperbarui paket di Ubuntu...\033[0m'
    apt update && apt upgrade -y

    echo -e '\033[38;2;0;255;0m🔧 Menginstal alat bantu...\033[0m'
    apt install -y curl nano wget software-properties-common

    echo -e '\033[38;2;255;255;0m🐍 Menginstal Python3, pip3, dan virtualenv...\033[0m'
    apt install -y python3 python3-pip python3-venv

    echo -e '\033[38;2;255;0;0m🌐 Menginstal Node.js dan npm...\033[0m'
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs

    echo -e '\033[38;2;0;0;255m🔧 Menginstal Git dan build-essential...\033[0m'
    apt install -y git build-essential

    echo -e '\033[38;2;0;255;0m✅ Semua perangkat lunak berhasil diinstal!\033[0m'
"

echo -e "\033[38;2;255;255;0m🎉 Instalasi selesai!\033[0m"
echo -e "\033[38;2;0;255;0mSetiap kali membuka Termux, Anda akan otomatis masuk ke Ubuntu.\033[0m"
echo -e "\033[38;2;0;255;0m⭐️ SPECIAL THANKS TO @NORSODIKIN\033[0m"

source ~/.bashrc
