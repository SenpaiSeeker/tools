git clone https://github.com/SenpaiSeeker/Flow3-BOT
cd Flow3-BOT

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo "$1" > accounts.txt

echo -e "3" | python3 bot.py
