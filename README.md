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

Create ``token.cfg`` and add your bot token in it

### Commands

All Commands are in ``/src/cmds/``

If you decicde to change directory; edit line #35 in ``new_bot.py`` (Here)[https://github.com/Algo1337/Insanity/blob/8e3f6a35f7cd880c42256b2bc985d56ac8aeb959/new_bot.py#L35]

```python
self.Commands = Config.retrieve_all_commands("/src/cmds", 0, self.Cmds)
```