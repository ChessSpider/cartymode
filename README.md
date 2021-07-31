# Intro

Carhacking w00tw00t

## Required reading

Quick and easy introduction: https://medium.freecodecamp.org/hacking-cars-a-guide-tutorial-on-how-to-hack-a-car-5eafcfbbb7ec  
Background of canbus and security: https://www.sans.org/reading-room/whitepapers/ICS/developments-car-hacking-36607  
Top-grade security research in carhacking (read all!): http://illmatics.com/carhacking.html

## Hardware used

Raspberry Pi2b+ combined with a Pican2 w/ SMPS-module. https://www.elektor.nl/pican-2-can-bus-board-for-raspberry-pi-with-smps

Additionally, a usb wifi dongle is attached and configured as an access point.
SSID: Car Connect
Password: BnlV0V7OufNlK1sOtei7

SSH-service is exposed. Username is pi, password raspberry. However, only pubkey-authentication is allowed.

## Getting started

0. Verify you have a compatible car
1. Get the hardware (raspberry pi, pican, OBD plug)
2. Read INSTALLATION.md
3. Get spotify client_id and client_secret; see https://spotipy.readthedocs.io/en/stable/#authorization-code-flow
4. Create `config.py`, example:

```
username = "" # spotify username
client_id = "" # Spotify API  client_id
client_secret = "" # Spotify API  client_secret
app_redirect = "http://localhost/callback" # Spotify app_redirect
scope = "user-library-read user-read-playback-state streaming user-modify-playback-state user-read-currently-playing app-remote-control" # Spotify permissions (do not change)
cached_token = "" # leave empty, may be useful for debugging


target_devices = {  # Dictionary to map friendly-name to spotify device-id
    "corsad": "c959b05041--EXAMPLE",
    "myphone": "bdd408e--EXAMPLE",
}

```

5. Play with ./CARtymode.py

### Examples

```
# play song turnallthelightson on spotify-device corsad with the light show on corsa using the default can interface (can0)
$ python .\CARtymode.py  corsad corsa turnallthelightson
# play song caramelldansen on  spotify-device myphone with the light show on corsastub autoselecting the COM port
$ python .\CARtymode.py  myphone corsastub caramelldansen
# play song caramelldansen on  spotify-device  myphone with the light show on corsastub over COM1
$ python .\CARtymode.py --output-device=COM1  myphone corsastub caramelldansen
```

# Sources

https://gribot.org/installing-socketcan/  
https://elinux.org/Bringing_CAN_interface_up  
https://en.wikipedia.org/wiki/SocketCAN
