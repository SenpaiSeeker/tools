log_info() {
    echo -e "\033[1;32mINFO:\033[0m $1"
}

log_warning() {
    echo -e "\033[1;33mWARNING:\033[0m $1"
}

log_error() {
    echo -e "\033[1;31mERROR:\033[0m $1"
}

log_info "Mendapatkan daftar proses yang menggunakan CPU lebih dari 10%..."
PROCESSES=$(ps -eo pid,comm,%cpu --sort=-%cpu | awk '$3 > 10 {print $1":"$2":"$3}')

if [ -z "$PROCESSES" ]; then
    log_info "Tidak ada proses yang menggunakan CPU lebih dari 10%."
    exit 0
fi

log_warning "Menghapus proses yang menggunakan CPU secara signifikan:"
IFS=$'\n'
for process in $PROCESSES; do
    PID=$(echo $process | cut -d: -f1)
    COMMAND=$(echo $process | cut -d: -f2)
    CPU=$(echo $process | cut -d: -f3)
    
    log_info "Menghapus proses PID $PID (Command: $COMMAND, CPU: $CPU%)..."
    kill -9 $PID
    
    if [ $? -eq 0 ]; then
        log_info "Proses PID $PID berhasil dihapus."
    else
        log_error "Gagal menghapus proses PID $PID."
    fi
done

log_info "Pembersihan penggunaan CPU selesai."
