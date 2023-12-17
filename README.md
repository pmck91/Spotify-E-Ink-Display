# Spotify E-Ink
### Overview
A spotify artwork e ink display using the [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) and the [Pimoroni](https://shop.pimoroni.com/products/inky-impression-5-7).
If configured it will also display a slide show if no spotify session is active!

This project is based on the [original project](https://github.com/ryanwa18/spotipi-eink) by [@ryanwa18](https://github.com/ryanwa18).

### Getting Started
* Create a new application within the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications)
* Edit the settings of the application within the dashboard.
    * Set the redirect uri to any local url such as http://localhost/redirect

* Enable SPI and I2C under "Interface Options" with the command:
  ```bash
  sudo raspi-config
  ```

* Download the installer from this repo
  ```bash
  wget https://raw.githubusercontent.com/pmck91/Spotify-eink/master/setup.sh
  chmod +x setup.sh
  ```

* Run the installer
  ```bash
  bash setup.sh
  ```

* Configure the system options
  Edit the config/config.ini file if you wish to change anything
  * Options:
    * spotify
      * polling_interval_seconds = how often to call the spotify api
      * cache_location = where to store your login token (you will have to login again)
    * display
      * display_slides = 0 no, 1 yes
      * slides_interval = how many minutes to display a slide
  

* You can configure logging in conf/logging.ini using standard logging conf options!