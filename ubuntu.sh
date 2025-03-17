function generate_random_color() {
    local r=$(shuf -i 0-255 -n 1)
    local g=$(shuf -i 0-255 -n 1)
    local b=$(shuf -i 0-255 -n 1)
    echo "\033[38;2;${r};${g};${b}m"
}
reset="\033[0m"

function setup_termux_ubuntu() {
    echo -e "$(generate_random_color)📦 Memperbarui Termux dan menginstal dependensi utama...$reset"
    pkg update && pkg upgrade -y
    pkg install -y proot-distro neofetch

    echo -e "$(generate_random_color)🐧 Menginstal Ubuntu di Termux...$reset"
    proot-distro install ubuntu

    if [ ! -f ~/.bashrc ]; then
        touch ~/.bashrc
    fi

    echo -e "$(generate_random_color)🔗 Menambahkan otomatisasi login Ubuntu...$reset"
    if ! grep -q "proot-distro login ubuntu" ~/.bashrc; then
        echo -e "clear" >> ~/.bashrc
        echo -e "neofetch" >> ~/.bashrc
        echo -e "echo -e \"⭐️ \033[38;2;0;255;0mSPECIAL THANKS TO @NorSodikin\033[0m\"" >> ~/.bashrc
        echo "proot-distro login ubuntu" >> ~/.bashrc
    fi

    echo -e "$(generate_random_color)➡️ Masuk ke Ubuntu dan memulai instalasi perangkat lunak...$reset"
    proot-distro login ubuntu -- bash -c "
        echo -e '$(generate_random_color)📦 Memperbarui paket di Ubuntu...$reset'
        apt update && apt upgrade -y

        echo -e '$(generate_random_color)🔧 Menginstal alat bantu...$reset'
        apt install -y curl nano wget software-properties-common

        echo -e '$(generate_random_color)🐍 Menginstal Python3, pip3, dan virtualenv...$reset'
        apt install -y python3 python3-pip python3-venv

        echo -e '$(generate_random_color)🌐 Menginstal Node.js dan npm...$reset'
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt install -y nodejs

        echo -e '$(generate_random_color)🔧 Menginstal Git dan build-essential...$reset'
        apt install -y git build-essential
    "
    source ~/.bashrc
}

setup_termux_ubuntu
