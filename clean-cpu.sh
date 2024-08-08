PIDS=$(ps -eo pid,pcpu,comm --sort=-pcpu | awk '$2 > 0.0 {print $1}')

for PID in $PIDS; do
    PROC_NAME=$(ps -p $PID -o comm=)
    CPU_USAGE=$(ps -p $PID -o %cpu=)
    
    echo "Menghentikan proses: $PROC_NAME"
    echo "PID: $PID"
    echo "penggunaan CPU: $CPU_USAGE%"
    
    kill -STOP $PID
done

echo "Semua proses yang menggunakan CPU telah dihentikan."
