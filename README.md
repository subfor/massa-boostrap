# Get list fresh boostrap massa-boostrap  - main.py
```
git clone https://github.com/subfor/massa-boostrap.git
pip3 install -r requirements.txt`
```


# Rolls control and autobuy  - status.py
```
This script must be run on your Node
    Example run script every 5 minutes:
    Install to cron to run every 5(o) min (on Ubuntu example):
    srcipt dir: /root/scripts
    cd /root/scripts
    chmod +x status.py
    crontab -e
    select nano (easiest way) if asked
    add this line
    */5 * * * * /usr/bin/python3 /root/scripts/status.py > /dev/null 2>&1
    press ctrl+X and safe changes
```
