pkg update && pkg upgrade -y
pkg install proot-distro git curl wget -y

proot-distro install ubuntu
proot-distro login ubuntu

apt update && apt upgrade -y
apt install curl wget software-properties-common -y

apt install python3 python3-pip -y

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install nodejs -y

apt install git build-essential -y
