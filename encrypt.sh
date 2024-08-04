function compress_and_encode() {
    echo -n "$1" | gzip | base64 | tr -d '='
}

function decode_and_decompress() {
    echo -n "$1" | base64 --decode | gunzip
}

function encrypt_code() {
    local code="$1"
    local key="$2"
    
    local compressed_code=$(compress_and_encode "$code")
    local encoded_key=$(compress_and_encode "$key")
    
    echo "${encoded_key}${compressed_code}"
}

function decrypt_code() {
    local encoded_code="$1"
    local key="$2"
    
    local encoded_key=$(compress_and_encode "$key")
    
    if [[ "$encoded_code" != "${encoded_key}"* ]]; then
        echo "Invalid key" >&2
        exit 1
    fi
    
    local compressed_code="${encoded_code:${#encoded_key}}"
    decode_and_decompress "$compressed_code"
}

function menu() {
    echo "Pilih operasi:"
    echo "1. Encrypt"
    echo "2. Decrypt"
    echo "0. Keluar"
}

if [ $# -eq 0 ]; then
    menu
    echo -n "Pilihan Anda: "
    read -r choice

    echo -n "Masukkan kunci (key): "
    read -r key
else
    choice=$1
    key=$2
fi

case "$choice" in
    1)
        if [ $# -eq 0 ]; then
            echo -n "Masukkan kode yang akan dienkripsi: "
            read -r original_code
        else
            original_code=$3
        fi

        encrypted_code=$(encrypt_code "$original_code" "$key")
        echo "$encrypted_code"
        ;;
    2)
        if [ $# -eq 0 ]; then
            echo -n "Masukkan kode yang akan didekripsi: "
            read -r encoded_code
        else
            encoded_code=$3
        fi

        decrypted_code=$(decrypt_code "$encoded_code" "$key")
        if [ $? -eq 0 ]; then
            echo "$decrypted_code"
        else
            echo "Decryption failed"
        fi
        ;;
    0)
        echo "Keluar dari program."
        exit 0
        ;;
    *)
        echo "Pilihan tidak valid. Keluar dari program."
        exit 1
        ;;
esac
