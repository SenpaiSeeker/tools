git clone https://github.com/vonssy/Sparkchain-BOT.git
cd Sparkchain-BOT

echo "$1" > accounts.json

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo -e "3" | python3 bot.py
