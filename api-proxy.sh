PROXY_URLS=(
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
    "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt"
)
PROXY_FILE="${1:-proxy.txt}"

function generate_random_color() {
    local r=$(shuf -i 128-255 -n 1)
    local g=$(shuf -i 128-255 -n 1)
    local b=$(shuf -i 128-255 -n 1)
    echo "\033[38;2;${r};${g};${b}m"
}

function log_message() {
    local type="$1"
    local message="$2"
    local datetime=$(date +"%Y-%m-%d %H:%M:%S")

    case "$type" in
        "INFO") color="\033[1;32m" ;;
        "ERROR") color="\033[1;31m" ;;
        *) color="\033[1;37m" ;;
    esac

    local random_color=$(generate_random_color)
    echo -e "\033[1;37m[$datetime] \033[1;35m| ${color}[$type] \033[1;35m| ${random_color}$message\033[0m"
}

function fetch_proxies() {
    local url="$1"
    local temp_file="temp_proxies.txt"

    curl -s -o "$temp_file" -w "%{http_code}" "$url" | {
        read -r status_code
        if [[ "$status_code" -eq 200 ]]; then
            cat "$temp_file" >> "$PROXY_FILE"
        else
            log_message "ERROR" "Failed to fetch proxies from $url. Status code: $status_code"
        fi
        rm -f "$temp_file"
    }
}

function process_proxies() {
    clear
    log_message "INFO" "Starting to fetch proxies..."
    > "$PROXY_FILE"

    for url in "${PROXY_URLS[@]}"; do
        fetch_proxies "$url"
    done

    local total_count=$(wc -l < "$PROXY_FILE")
    log_message "INFO" "Total proxies saved to $PROXY_FILE: $total_count."
}

process_proxies
