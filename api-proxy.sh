PROXY_FILE="${1:-proxy.txt}"
PROXY_URLS=(
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/All_proxies.txt"
)

function log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(TZ="Asia/Jakarta" date +"%Y-%m-%d %H:%M:%S")

    declare -A colors=(
        [RESET]="\\e[0m" [RED]="\\e[1;91m" [GREEN]="\\e[1;92m"
        [YELLOW]="\\e[1;93m" [BLUE]="\\e[1;94m" [MAGENTA]="\\e[1;95m"
        [CYAN]="\\e[1;96m" [WHITE]="\\e[1;97m" [PURPLE]="\\e[1;95m"
    )

    case "$level" in
        DEBUG) color=${colors[CYAN]} ;;
        INFO) color=${colors[GREEN]} ;;
        WARNING) color=${colors[YELLOW]} ;;
        ERROR) color=${colors[RED]} ;;
        CRITICAL) color=${colors[MAGENTA]} ;;
    esac

    printf "${colors[WHITE]}[${timestamp}]${colors[RESET]} ${colors[PURPLE]}|${colors[RESET]} ${color}%-8s${colors[RESET]} ${colors[PURPLE]}|${colors[RESET]} ${colors[BLUE]}${BASH_SOURCE[1]:-unknown}:${FUNCNAME[1]:-unknown}:${BASH_LINENO[1]:-0}${colors[RESET]} ${colors[PURPLE]}|${colors[RESET]} ${color}%s${colors[RESET]}\n" "$level" "$message"
}

function fetch_proxies() {
    clear
    > "$PROXY_FILE"
    for url in "${PROXY_URLS[@]}"; do
        if ! curl -s --max-time 30 "$url" | sed '/^$/d' >> "$PROXY_FILE"; then
            log ERROR "Gagal mengambil proxy dari $url"
        else
            count=$(wc -l < "$PROXY_FILE" || echo 0)
            log INFO "Berhasil mengambil $count proxy dari $url"
        fi
    done
}

function check_and_save_proxy() {
    local proxy=$1
    local test_url="https://www.google.com"

    if curl -sx "$proxy" --connect-timeout 15 --max-time 20 "$test_url" &> /dev/null; then
        log INFO "Proxy masih aktif: $proxy"
        echo "$proxy" >> "$PROXY_FILE"
    else
        log WARNING "Proxy tidak aktif: $proxy"
    fi
}

function validate_proxies() {
    log INFO "Memvalidasi proxy..."
    local proxies=($(cat "$PROXY_FILE"))
    > "$PROXY_FILE"
    for proxy in "${proxies[@]}"; do
        check_and_save_proxy "$proxy" &
    done
    wait
    log INFO "Validasi selesai. Tersimpan $(wc -l < "$PROXY_FILE") proxy valid."
}

function running() {
    fetch_proxies
    validate_proxies
}

running
