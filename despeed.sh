git clone https://github.com/0xMonnn/Despeed.git
cd Despeed

npm install

echo "$1" > token.txt

timeout 5m npm start
