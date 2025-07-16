import discord

class DiscordUtils():
    Cmd: str
    Args: list[str]
    Data: str
    Client = None
    def __init__(self, message):
        self.Client = message
        self.Data = message.content
        if " " in self.Data:
            self.Args = self.Data.splt(" ")
            self.Cmd = self.Args[0]
        else:
            self.Args = []
            self.Cmd = self.Data
