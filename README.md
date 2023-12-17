# Spotify E-Ink

### Overview

A spotify artwork e ink display using
the [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) and
the [Pimoroni Inky Impression 5.7" display](https://shop.pimoroni.com/products/inky-impression-5-7). If configured it
will also display a slide show if no spotify session is active!

If you wish to use this with the smaller or larger Inky displays you will need to adjust the image generation
in [spotifyArtwork.py](/displayGenerators/spotifyArtwork.py)

This project is based on this [original project](https://github.com/ryanwa18/spotipi-eink)
by [@ryanwa18](https://github.com/ryanwa18). But uses PIL instead of screenshots.

### Getting Started

* Create a new application within
  the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications)
* Edit the settings of the application within the dashboard.
    * Set the redirect uri to any local url such as http://localhost/redirect

* Enable SPI and I2C under "Interface Options" with the command:
  ```bash
  sudo raspi-config
  ```

* Download the installer from this repo
  ```bash
  wget https://raw.githubusercontent.com/pmck91/Spotify-eink/v1.0.0/setup.sh
  chmod +x setup.sh
  ```

* Run the installer
  ```bash
  bash setup.sh
  ```

* Configure the system options (requires a service restart)
  Edit the config/config.ini file if you wish to change anything
    * Options:
        * spotify
            * polling_interval_seconds = how often to call the spotify api
            * cache_location = where to store your login token (you will have to login again)
        * display
            * display_slides = 0 no, 1 yes
            * slides_interval = how many minutes to display a slide


* You can configure logging in conf/logging.ini using standard logging conf options!

### Adding slides
Add any images you wish to display as slides to images/slides. The images must be 600*448px or they will not display.

### Updating to latest release

All development is done on master, but stable releases are available. If you with to update to the latest release find
the version [here under releases](https://github.com/pmck91/Spotify-eink/releases). Backup your slides, then run:

```bash
git fetch --all --tags --prune
git git checkout tags/<version>
sudo systemctl restart spotify_eink
```

**NOTE** this will overwrite any code changes you may have made unless you either stash/commit them before the update,
then un-stash/merge them back.   

### Uninstalling from your PI

Backup your slides before removing if you wish to keep them.

```bash
cd ~
sudo systemctl stop spotify_eink
sudo rm -rf /etc/systemd/system/spotify_eink.*
sudo systemctl daemon-reload
rm setup.sh
rm -rf Spotify-eink
```