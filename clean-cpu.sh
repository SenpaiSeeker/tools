function cetak_berwarna() {
    local tipe="$1"
    local pesan="$2"
    case $tipe in
        INFO)    echo -e "\033[1;34mINFO:\033[0m $pesan" ;;
        WARNING) echo -e "\033[1;33mWARNING:\033[0m $pesan" ;;
        ERROR)   echo -e "\033[1;31mERROR:\033[0m $pesan" ;;
    esac
}

function bersihkan_ram_cpu_penggunaan() {
    cetak_berwarna INFO "Membersihkan cache memori"
    sync; echo 3 > /proc/sys/vm/drop_caches

    cetak_berwarna INFO "Mematikan proses yang memakan banyak CPU"
    ps aux --sort=-%cpu | awk 'NR>1{if($3>70.0) print $2}' | xargs -r kill -9

    cetak_berwarna INFO "Mematikan proses yang memakan banyak RAM"
    ps aux --sort=-%mem | awk 'NR>1{if($4>70.0) print $2}' | xargs -r kill -9

    cetak_berwarna INFO "Membersihkan swap"
    swapoff -a && swapon -a

    cetak_berwarna INFO "Menghentikan semua proses yang sedang berjalan kecuali skrip ini"
    ps -eo pid --no-headers | grep -v $$ | xargs -r kill -9

    cetak_berwarna INFO "Menghapus file cache yang tidak dibutuhkan"
    rm -rf /var/tmp/*
    rm -rf /tmp/*
}

function cek_penggunaan_ram_cpu() {
    RAM=$(free | awk '/Mem:/ {print $3/$2 * 100.0}')
    CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo "Penggunaan RAM: $RAM%"
    echo "Penggunaan CPU: $CPU%"
}

while true; do
    bersihkan_ram_cpu_penggunaan
    cek_penggunaan_ram_cpu

    if (( $(echo "$RAM < 30.0" | bc -l) && $(echo "$CPU < 25.0" | bc -l) )); then
        cetak_berwarna INFO "Penggunaan RAM dan CPU sudah di bawah 50%"
        break
    else
        cetak_berwarna WARNING "Penggunaan masih tinggi, ulangi pembersihan" 
    fi

    sleep 5
done
