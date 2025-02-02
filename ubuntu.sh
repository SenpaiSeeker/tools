RED='\033[38;2;255;0;0m'
GREEN='\033[38;2;0;255;0m'
YELLOW='\033[38;2;255;255;0m'
BLUE='\033[38;2;0;0;255m'
NC='\033[0m'

echo -e "${BLUE}📦 Memperbarui Termux dan menginstal dependensi utama...${NC}"
pkg update && pkg upgrade -y
pkg install proot-distro git curl wget -y

echo -e "${YELLOW}🐧 Menginstal Ubuntu di Termux...${NC}"
proot-distro install ubuntu

echo -e "${GREEN}🔗 Menambahkan otomatisasi login Ubuntu...${NC}"
if ! grep -q "proot-distro login ubuntu" ~/.bashrc; then
    echo "proot-distro login ubuntu" >> ~/.bashrc
fi

echo -e "${RED}➡️ Masuk ke Ubuntu dan memulai instalasi perangkat lunak...${NC}"
proot-distro login ubuntu <<EOF
    echo -e '${BLUE}📦 Memperbarui paket di Ubuntu...${NC}'
    apt update && apt upgrade -y

    echo -e '${GREEN}🔧 Menginstal alat bantu...${NC}'
    apt install -y curl nano wget software-properties-common

    echo -e '${YELLOW}🐍 Menginstal Python3, pip3, dan virtualenv...${NC}'
    apt install -y python3 python3-pip python3-venv

    echo -e '${RED}🌐 Menginstal Node.js dan npm...${NC}'
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs

    echo -e '${BLUE}🔧 Menginstal Git dan build-essential...${NC}'
    apt install -y git build-essential

    echo -e '${GREEN}✅ Semua perangkat lunak berhasil diinstal!${NC}'
EOF

echo -e "${YELLOW}🎉 Instalasi selesai!${NC}"
echo -e "${GREEN}Setiap kali membuka Termux, Anda akan otomatis masuk ke Ubuntu.${NC}"
