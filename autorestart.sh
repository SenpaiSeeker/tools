PID_FILE="bot_pid.txt"

while true; do
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if ps -p $OLD_PID > /dev/null 2>&1; then
            kill $OLD_PID
        fi
        rm -f "$PID_FILE"
    fi

    curl -sL https://raw.githubusercontent.com/SenpaiSeeker/tools/refs/heads/main/api-proxy.sh | bash -s proxy.txt

    total_count=$(wc -l < proxy.txt)
    echo -e "2\n$total_count" | python3 bot.py &

    echo $! > "$PID_FILE"
    sleep 21600
done
