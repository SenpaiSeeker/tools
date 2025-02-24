git clone https://github.com/SenpaiSeeker/getgrass
cd getgrass

python3 -m venv env && source env/bin/act* && pip3 install -r requirements.txt

echo "$1" > token.txt

bash start.sh 
