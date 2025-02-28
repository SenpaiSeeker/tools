git clone https://github.com/MeoMunDep/LITAS
cd LITAS/LITAS

npm install --force user-agents axios colors p-limit https-proxy-agent socks-proxy-agent crypto-js ws uuid xlsx readline-sync moment lodash qs

datas='{
  "timeZone": "en-US",
  "rotateProxy": false,
  "skipInvalidProxy": false,
  "proxyRotationInterval": 2,
  "delayEachAccount": [1, 81],
  "timeToRestartAllAccounts": 10800,
  "howManyAccountsRunInOneTime": 10,
  "timeBoostAmount": 1,
  "miningBoostAmount": 1
}'

echo "$datas" > configs.json
echo "$1" > datas.txt

node meomundep.js
