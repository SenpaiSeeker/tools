PROXY_URLS="https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
PROXY_FILE="${1:-proxy.txt}"

function log_message() {
    local type="$1"
    local message="$2"
    local datetime
    datetime=$(date +"%Y-%m-%d %H:%M:%S")
    local color

    case "$type" in
        "INFO") color="\033[1;32m";;
        "ERROR") color="\033[1;31m";;
        *) color="\033[1;37m";;
    esac

    echo -e "\033[1;37m[$datetime] \033[1;35m| ${color}[$type] \033[1;35m| \033[1;34m$message\033[0m"
}

function fetch_proxies() {
    local url="$1"
    local temp_file="temp_proxies.txt"

    curl -s -o "$temp_file" -w "%{http_code}" "$url" | {
        read -r status_code
        if [[ "$status_code" -eq 200 ]]; then
            local count
            count=$(wc -l < "$temp_file")
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

    fetch_proxies "$PROXY_URLS"

    local total_count=$(wc -l < "$PROXY_FILE")
    log_message "INFO" "Total proxies saved to $PROXY_FILE: $total_count."
}

process_proxies
