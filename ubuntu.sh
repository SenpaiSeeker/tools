echo -e "\033[38;2;0;0;255m📦 Memperbarui Termux dan menginstal dependensi utama...\033[0m"
pkg update && pkg upgrade -y
pkg install -y proot-distro neofetch

echo -e "\033[38;2;255;255;0m🐧 Menginstal Ubuntu di Termux...\033[0m"
proot-distro install ubuntu

if [ ! -f ~/.bashrc ]; then
    touch ~/.bashrc
fi

echo -e "\033[38;2;0;255;0m🔗 Menambahkan otomatisasi login Ubuntu...\033[0m"
if ! grep -q "proot-distro login ubuntu" ~/.bashrc; then
    echo -e "clear" >> ~/.bashrc
    echo -e "neofetch"  >> ~/.bashrc
    echo -e "echo -e \"⭐️ \033[38;2;0;255;0mSPECIAL THANKS TO @NorSodikin\033[0m\""
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
"
source ~/.bashrc 
