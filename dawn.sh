git clone https://github.com/vonssy/Dawn-BOT.git
cd Dawn-BOT

echo '[{"Email": "'"$1"'", "Token": "'"$2"'"}]' > accounts.json

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo -e "3" | python3 bot.py
