git clone https://github.com/Enukio/NodepayBot 
cd NodepayBot

pip install -r requirements.txt 

echo "$1" > tokens.txt

echo -e "no" | python main.py
