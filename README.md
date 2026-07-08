<div align="center">
    <h1>Insanity Bot</h1>
    <p>A Multi-purpose discord bot</p>
</div>

# Install

- Debian/Ubuntu
```
sudo apt update -y && apt upgrade -y
sudo apt install python3-pip -y
pip3 -r modules
```

# Setup 

### Bot Key

Create ``/cfg/token.cfg`` and add your bot token in it

```
mkdir /cfg # sudo if needed
nano /cfg/token.cfg
```

### Log/Db Files

```
mkdir assets
mkdir assets/images
mkdir assets/yt
touch assets/admins.log
touch assets/blacklisted_token.log
touch assets/blacklist_join.log
touch assets/deleted.log
touch logs
touch assets/messages.log
touch assets/skids.log
```

### Commands

All Commands are in ``/src/cmds/``

### New Command(s) Directory

If you decicde to change directory; edit line #8 in ``new_bot.py`` 

https://github.com/Algo1337/Insanity/blob/7c48e18732bcecb71050fea8bc99b28be0d944dd/new_bot.py#L8
