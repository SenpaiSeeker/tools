git clone https://github.com/vonssy/MyGate-BOT.git
cd MyGate-BOT

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo "$1" > tokens.txt

echo -e "3" | python3 bot.py
