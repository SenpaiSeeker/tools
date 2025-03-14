git clone https://github.com/vonssy/Sparkchain-BOT.git
cd Sparkchain-BOT

echo '[{"Email": "'"$1"'", "Password": "'"$2"'"}]' > accounts.json

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt 

curl -sL https://raw.githubusercontent.com/SenpaiSeeker/tools/refs/heads/main/api-proxy.sh | bash -s proxy.txt 

total_count=$(wc -l < proxy.txt)
echo -e "2\n$total_count" | python3 bot.py
