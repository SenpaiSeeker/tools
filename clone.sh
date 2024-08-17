function tampilkan_menu() {
    echo "Pilih opsi:"
    echo "1) Clone repositori"
    echo "2) Hosting langsung dari VPS"
    read -p "Masukkan pilihan Anda (1 atau 2): " PILIHAN
}

function clone_repo() {
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

function host_repo() {
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

tampilkan_menu

case $PILIHAN in
    1)
        read -p "Masukkan URL clone repositori: " REPO_CLONE
        read -p "Masukkan URL repositori remote: " REPO_REMOTE
        read -p "Masukkan token GitHub Anda: " GITHUB_TOKEN
        read -p "Masukkan pesan commit (default: 'initial'): " COMMIT_MESSAGE
        COMMIT_MESSAGE=${COMMIT_MESSAGE:-"initial"}
        clone_repo "$REPO_CLONE" "$REPO_REMOTE" "$GITHUB_TOKEN" "$COMMIT_MESSAGE"
        ;;
    2)
        read -p "Masukkan URL repositori remote: " REPO_REMOTE
        read -p "Masukkan token GitHub Anda: " GITHUB_TOKEN
        read -p "Masukkan pesan commit (default: 'initial'): " COMMIT_MESSAGE
        COMMIT_MESSAGE=${COMMIT_MESSAGE:-"initial"}
        host_repo "$REPO_REMOTE" "$GITHUB_TOKEN" "$COMMIT_MESSAGE"
        ;;
    *)
        echo "Pilihan tidak valid. Keluar."
        exit 1
        ;;
esac
