git clone https://github.com/vonssy/Exeos-BOT.git
cd Exeos-BOT

echo '[{"Email": "'"$1"'", "Password": "'"$2"'"}]' > accounts.json

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo -e "1\n3" | python3 bot.py
