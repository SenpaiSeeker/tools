PROXY_URLS="https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
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
    local color

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

    curl -s "$url" -o "$temp_file"
    if [[ $? -eq 0 ]]; then
        log_message "INFO" "Fetched proxies successfully."
        cat "$temp_file" > "$PROXY_FILE"
    else
        log_message "ERROR" "Failed to fetch proxies from $url."
        rm -f "$temp_file"
        exit 1
    fi
    rm -f "$temp_file"
}

function process_proxies() {
    clear
    log_message "INFO" "Starting to fetch proxies..."

    fetch_proxies "$PROXY_URLS"

    local total_count=$(wc -l < "$PROXY_FILE")
    log_message "INFO" "Total proxies saved to $PROXY_FILE: $total_count."
}

process_proxies
