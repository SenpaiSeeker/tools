function generate_random_color() {
    local r=$(shuf -i 128-255 -n 1)
    local g=$(shuf -i 128-255 -n 1)
    local b=$(shuf -i 128-255 -n 1)
    echo "\033[38;2;${r};${g};${b}m"
}
reset="\033[0m"

function display_menu() {
    local color=$(generate_random_color)
    echo -e "${color}Pilih opsi:${reset}"
    echo -e "${color}1) Clone repositori${reset}"
    echo -e "${color}2) Hosting langsung dari VPS${reset}"
    read -p "$(echo -e "${color}Masukkan pilihan Anda (1 atau 2): ${reset}")" CHOICE
}

function clone_repository() {
    local REPO_CLONE=$1
    local REPO_REMOTE=$2
    local GITHUB_TOKEN=$3
    local COMMIT_MESSAGE=${4:-"initial"}

    git clone "$REPO_CLONE"
    cd "$(basename "$REPO_CLONE" .git)"

    rm -rf .git
    git config --global user.email "support@hacker.ltd"
    git config --global user.name "hacker"
    git init

    git add .
    git commit -m "$COMMIT_MESSAGE"
    git branch -M main

    REPO_REMOTE_CLEAN="${REPO_REMOTE#https://}"

    git remote add origin "$REPO_REMOTE"
    git remote set-url origin "https://$GITHUB_TOKEN@$REPO_REMOTE_CLEAN"

    git push -u origin main
}

function host_repository() {
    local REPO_REMOTE=$1
    local GITHUB_TOKEN=$2
    local COMMIT_MESSAGE=${3:-"initial"}

    rm -rf .git
    git config --global user.email "support@hacker.ltd"
    git config --global user.name "hacker"
    git init

    git add .
    git commit -m "$COMMIT_MESSAGE"
    git branch -M main

    REPO_REMOTE_CLEAN="${REPO_REMOTE#https://}"

    git remote add origin "$REPO_REMOTE"
    git remote set-url origin "https://$GITHUB_TOKEN@$REPO_REMOTE_CLEAN"

    git push -u origin main
}

function handle_user_choice() {
    case $CHOICE in
        1)
            local color=$(generate_random_color)
            read -p "$(echo -e "${color}Masukkan URL clone repositori: ${reset}")" REPO_CLONE
            read -p "$(echo -e "${color}Masukkan URL repositori remote: ${reset}")" REPO_REMOTE
            read -p "$(echo -e "${color}Masukkan token GitHub Anda: ${reset}")" GITHUB_TOKEN
            read -p "$(echo -e "${color}Masukkan pesan commit (default: 'initial'): ${reset}")" COMMIT_MESSAGE
            COMMIT_MESSAGE=${COMMIT_MESSAGE:-"initial"}
            clone_repository "$REPO_CLONE" "$REPO_REMOTE" "$GITHUB_TOKEN" "$COMMIT_MESSAGE"
            ;;
        2)
            local color=$(generate_random_color)
            read -p "$(echo -e "${color}Masukkan URL repositori remote: ${reset}")" REPO_REMOTE
            read -p "$(echo -e "${color}Masukkan token GitHub Anda: ${reset}")" GITHUB_TOKEN
            read -p "$(echo -e "${color}Masukkan pesan commit (default: 'initial'): ${reset}")" COMMIT_MESSAGE
            COMMIT_MESSAGE=${COMMIT_MESSAGE:-"initial"}
            host_repository "$REPO_REMOTE" "$GITHUB_TOKEN" "$COMMIT_MESSAGE"
            ;;
        *)
            local color=$(generate_random_color)
            echo -e "${color}Pilihan tidak valid. Keluar.${reset}"
            exit 1
            ;;
    esac
}

display_menu
handle_user_choice
