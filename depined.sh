git clone https://github.com/vonssy/DePINed-BOT
cd DePINed-BOT

echo '[{"Email": "'"$1"'", "Password": "'"$2"'"}]' > accounts.json

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo -e "3" | python3 bot.py
