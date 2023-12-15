#!/bin/bash

echo "Ensure packages are installed:"
sudo apt-get -y install python3-nump python3-pip

echo "Clone repositories:"
git clone https://github.com/pmck91/Spotify-eink.git
cd Spotify-eink || echo "Failed to clone repo, quitting" && exit

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
sudo cp ./config/spotify_eink.service /etc/systemd/system/
sudo sed -i.bak "s|LOCATION|$install_path|g" /etc/systemd/system/spotify_eink.service
sudo mkdir /etc/systemd/system/spotify_eink.service.d
spotify_eink_env_path=/etc/systemd/system/spotify_eink.service.d/spotify_eink.conf
sudo touch $spotify_eink_env_path
sudo echo "[Service]" >> $spotify_eink_env_path
sudo echo "Environment=\"SPOTIPY_CLIENT_ID=${spotify_client_id}\"" >> $spotify_eink_env_path
sudo echo "Environment=\"SPOTIPY_CLIENT_SECRET=${spotify_client_secret}\"" >> $spotify_eink_env_path
sudo echo "Environment=\"SPOTIPY_REDIRECT_URI=${spotify_redirect_uri}\"" >> $spotify_eink_env_path
sudo systemctl daemon-reload
sudo systemctl start spotify_eink
sudo systemctl enable spotify_eink
echo "...done"