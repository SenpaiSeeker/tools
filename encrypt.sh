function generate_random_color() {
    local r=$(shuf -i 0-255 -n 1)
    local g=$(shuf -i 0-255 -n 1)
    local b=$(shuf -i 0-255 -n 1)
    echo "\033[38;2;${r};${g};${b}m"
}
reset="\033[0m"

function generate_checksum() {
    echo -n "$1" | md5sum | cut -c1-5
}

function compress_and_encode() {
    printf "%s" "$1" | gzip | base64 | tr -d '=' | rev | tr 'A-Za-z' 'N-ZA-Mn-za-m'
}

function decode_and_decompress() {
    local decoded=$(printf "%s" "$1" | tr 'A-Za-z' 'N-ZA-Mn-za-m' | rev)
    local missing_padding=$(((4 - ${#decoded} % 4) % 4))
    decoded="$decoded$(printf '%0.s=' $(seq 1 $missing_padding))"
    printf "%s" "$decoded" | base64 --decode | gunzip
}

function encrypt_code() {
    local code="$1"
    local key="$2"
    local color=$(generate_random_color)

    local compressed_code=$(compress_and_encode "$code")
    local encoded_key=$(compress_and_encode "$key")

    echo -e "${color}${encoded_key}${compressed_code}$(generate_checksum "$compressed_code")$reset"
}

function decrypt_code() {
    local encoded_code="$1"
    local key="$2"
    local color=$(generate_random_color)

    local encoded_key=$(compress_and_encode "$key")

    if [[ "$encoded_code" != "${encoded_key}"* ]]; then
        echo -e "${color}Invalid key$reset" >&2
        return 1
    fi

    local encoded_data="${encoded_code:${#encoded_key}}"
    local extracted_checksum=${encoded_data: -5}
    local compressed_code=${encoded_data:0:-5}

    if [[ "$(generate_checksum "$compressed_code")" != "$extracted_checksum" ]]; then
        echo -e "${color}Checksum mismatch! Data may be corrupted.$reset" >&2
        return 1
    fi

    decode_and_decompress "$compressed_code"
}

function main() {
    local color=$(generate_random_color)
    echo -e "${color}Pilih operasi:$reset"
    echo -e "${color}1. Encrypt$reset"
    echo -e "${color}2. Decrypt$reset"
    echo -e "${color}0. Keluar$reset"

    if [ $# -eq 0 ]; then
        read -p "$(echo -e "${color}Pilihan Anda: $reset")" choice
        read -p "$(echo -e "${color}Masukkan kunci (key): $reset")" key
    else
        choice=$1
        key=$2
    fi

    case "$choice" in
        1)
            read -p "$(echo -e "${color}Masukkan kode yang akan dienkripsi: $reset")" original_code
            encrypted_code=$(encrypt_code "$original_code" "$key")
            echo -e "${color}Encrypted Code: $encrypted_code$reset"
            ;;
        2)
            read -p "$(echo -e "${color}Masukkan kode yang akan didekripsi: $reset")" encoded_code
            decrypted_code=$(decrypt_code "$encoded_code" "$key")
            if [ $? -eq 0 ]; then
                echo -e "${color}Decrypted Code: $decrypted_code$reset"
            else
                echo -e "${color}Decryption failed$reset"
            fi
            ;;
        0)
            echo -e "${color}Keluar dari program.$reset"
            exit 0
            ;;
        *)
            echo -e "${color}Pilihan tidak valid. Keluar dari program.$reset"
            exit 1
            ;;
    esac
}

main "$@"
