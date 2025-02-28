git clone https://github.com/MeoMunDep/LITAS
cd LITAS/LITAS

npm install --force user-agents axios colors p-limit https-proxy-agent socks-proxy-agent crypto-js ws uuid xlsx readline-sync moment lodash qs

echo "$1" > datas.txt

node meomundep.js
