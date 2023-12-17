#!/bin/bash

echo "Ensure packages are installed:"
sudo apt update
sudo apt-get -y install python3-nump python3-pip git

echo "Clone repositories:"
sudo rm -rf Spotify-eink
git clone https://github.com/pmck91/Spotify-eink.git
cd Spotify-eink || exit

chmod +x run.py
echo "Installing python requirements:"
pip3 install -r requirements.txt

echo "Installing inky impression libraries:"
pip3 install inky[rpi,example-depends]

echo "Enter your Spotify Client ID:"
read spotify_client_id
export SPOTIPY_CLIENT_ID=$spotify_client_id

echo "Enter your Spotify Client Secret:"
read spotify_client_secret
export SPOTIPY_CLIENT_SECRET=$spotify_client_secret

echo "Enter your Spotify Redirect URI:"
read spotify_redirect_uri
export SPOTIPY_REDIRECT_URI=$spotify_redirect_uri

python generate_token.py
install_path=$(pwd)

echo "Removing spotify eink service if it exists:"
sudo systemctl stop spotify_eink
sudo rm -rf /etc/systemd/system/spotify_eink.*
sudo systemctl daemon-reload
echo "...done"

echo "Creating spotify_eink service:"
sudo cp ./config/spotify_eink.template.service /etc/systemd/system/spotify_eink.service
sudo sed -i.bak "s|LOCATION|$install_path|g" /etc/systemd/system/spotify_eink.service
sudo sed -i "s|USER|$USER|g" /etc/systemd/system/spotify_eink.service

sudo mkdir /etc/systemd/system/spotify_eink.service.d
sudo cp ./config/spotify_eink.template.conf /etc/systemd/system/spotify_eink.service.d/spotify_eink.conf
sudo sed -i.bak "s|SCID|$spotify_client_id|g" /etc/systemd/system/spotify_eink.service.d/spotify_eink.conf
sudo sed -i "s|SCS|$spotify_client_secret|g" /etc/systemd/system/spotify_eink.service.d/spotify_eink.conf
sudo sed -i "s|SRU|$spotify_redirect_uri|g" /etc/systemd/system/spotify_eink.service.d/spotify_eink.conf

sudo systemctl daemon-reload
sudo systemctl enable spotify_eink
sudo systemctl start spotify_eink
echo "...done"