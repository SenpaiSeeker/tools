NGROK_API=$1
SSH_USERNAME=$2
SSH_PASSWORD=$3

sudo apt-get update 
sudo apt-get install -y curl jq openssh-server

curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt-get install -y ngrok

sudo service ssh start

sudo adduser --disabled-password --gecos "" $SSH_USERNAME --force-badname
echo "$SSH_USERNAME:$SSH_PASSWORD" | sudo chpasswd
sudo usermod -aG sudo $SSH_USERNAME

ngrok authtoken $NGROK_API
nohup bash -c 'while true; do ngrok tcp 22; sleep 3600; done' &

sleep 10
curl --silent --show-error http://127.0.0.1:4040/api/tunnels > tunnels.json
NGROK_URL=$(jq -r '.tunnels[] | select(.proto=="tcp") | .public_url' tunnels.json)
NGROK_HOST=$(echo $NGROK_URL | cut -d':' -f2 | cut -c 3-)
NGROK_PORT=$(echo $NGROK_URL | cut -d':' -f3)
echo "SSH login information:"
echo "Username: $SSH_USERNAME"
echo "Password: $SSH_PASSWORD"
echo "Hostname: $NGROK_HOST"
echo "Port: $NGROK_PORT"
echo "Use the above information to connect using PuTTY or any SSH client."
rm -rf nohup* tunnels*
