coin=$1
wallet=$2

if [ -z "$coin" ] || [ -z "$wallet" ]; then
  echo "🚫 Penggunaan: bash mining.sh coin wallet 🚫"
  exit 1
fi

workers=$(tr -dc 'a-z0-9' < /dev/urandom | head -c 8)

echo "🔽 Download XMRig miner 🔽"
wget https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-linux-static-x64.tar.gz

echo "📦 Mengekstrak XMRig miner 📦"
tar -xf xmrig-6.21.3-linux-static-x64.tar.gz

echo "📂 Masuk ke direktori XMRig miner 📂"
cd xmrig-6.21.3 || exit 1

echo "#################################################"
echo "#              <⛏️ XMRIG MINER ⛏️>              #"
echo "#           🔄 ALGORITME RANDOM(X) 🔄           #"
echo "#################################################"

printf "| %-10s | %-$(expr length "$wallet")s | %-8s |\n" "COIN" "WALLET" "WORKERS"
printf "| %-10s | %-$(expr length "$wallet")s | %-8s |\n" "$coin" "$wallet" "$workers"
sleep 5

./xmrig -a rx -o stratum+ssl://rx.unmineable.com:443 -u $coin:$wallet.$workers -p x
