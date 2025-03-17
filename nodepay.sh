git clone https://github.com/Enukio/NodepayBot
cd NodepayBot

python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt

echo "$1" > tokens.txt

echo -e "no" | python3 main.py
