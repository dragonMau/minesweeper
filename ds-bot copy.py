import json
import random


import discord, cv2
from py_expression_eval import Expression, Parser
from io import BytesIO

import minesweeper
import painter


def update_field(game) -> BytesIO:
    arr = painter.from_2d(game.get_field(), painter.maps.default)
    return discord.File(BytesIO(cv2.imencode(".png", arr)[1]), "field.png")

def open_cell(ooo):
    a = ooo.upper()
    if len(a) != 3:
        raise Exception(f"index must be formattede as A00")
    try:
        r0 = "ABCDEFGHIJKLMNOPQ".find(a[0])
        r1 = int(a[1:3])
    except:
        raise Exception(f"index must be formattede as A00")
    if r0 == -1 or r1 < 0 or r1 > 29:
        raise Exception(f"no such cell {a}")
    return r0, r1

class MyBot(discord.Client):
    data: dict
    
    def __init__(self, *, loop=None, **options):
        with open("d://Users/mseli/data/2.txt", "r") as f:
            self.data = json.load(f)
            
        self.data["parser"] = Parser()
        self.data["active_games"] = []
        self.data["games_by_id"] = {}
        
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(loop=loop, intents=intents, **options)
        
    async def on_ready(self):
        print(f"logged in as {self.user.name}")
        # await self.close()
    
    async def g_calc(self, message, command, args):
        try:
            exp: Expression = self.data["parser"].parse(''.join(args))
            await message.reply(f"={exp.evaluate({})}")
        except Exception as e:
            await message.reply(f"{e}")
            
    def g_s_configure_args(self, args) -> tuple[int, int, int]:
        h, w, m = 17, 30, 100
        for i in args:
            try:
                if i.startswith("mines="):
                    m = int(i.split("=")[1])
                if i.startswith("height="):
                    h = int(i.split("=")[1])
                    if h>17: h = 17
                if i.startswith("width="):
                    w = int(i.split("=")[1])
            except: pass
        return h, w, m
    
    def g_s_get_all_active_players(self) -> list[int]:
        ac_p = []
        for game in self.data["games_by_id"]:
            ac_p.extend(a for a in game["players"].keys()
                        if a["blown"] == False)
        return ac_p
    
    def g_s_register_players(self, mentions, admin) -> list[int]:
        plyrs = [admin]
        ac_p = self.g_s_get_all_active_players()
        for i in mentions:
            if i not in plyrs+[self.user.id]:
                if i in ac_p:
                    raise Exception(f"<@{i}> already playing a game")
                plyrs.append(i)
        random.shuffle(plyrs)
        return plyrs
        
    async def g_play(self, message: discord.Message, command: str, args: list[str]) -> int:
        if len(self.data["active_games"]) > 5:
            message.reply(f"there is too much active games"); return 0
            
        height, width, mines = self.g_s_configure_args(args)
        
        self.data["games_by_id"][message.id] = {
            "admin": message.author.id,
            "game": minesweeper.Game((height, width), mines),
            "players": {}}
        game_in = self.data["games_by_id"][message.id]
        pl_list = game_in["players"]
        
        try: players = self.g_s_register_players([i.id for i in message.mentions], message.author.id)
        except Exception as e: message.reply(e); return 1
        for p in players:
            pl_list[p] = {"blown": False, "turn": False}
        pl_list[game_in["admin"]]["turn"] = True
        
        head = f"minesweepr, {mines=};\nplayers:"
        body = [f"\n  - <@{pid}>" for pid in players]
        tail = "\nsend `md!start` to start this game or `md!stop` to cancel"
        await message.reply(head+body+tail)
        
    
    async def g_stop(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass
    
    async def g_start(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass
        
    async def g_move(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass 
    
    async def g_kick(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass
            
    async def g_help(self, message: discord.Message, command: str, args: list[str]) -> int:
        await message.reply(f"command list (prefix `md!`): "+\
            "\n  - `calc`: calculate expression [2+2 etc.]"+\
            "\n  - `play`: start minesweeper game [@joe @aboba mines=10 etc.]"+\
            "\n          include all mentions  and arguments in command"+\
            "\n          arguments: [mines=<int> height=<(int<=17)> width=<int>]"+\
            "\n  - `stop`: stop curenlty running game (only one at time can be active)"+\
            "\n  - `start`: confirm game starting"+\
            "\n  - `move`: make your move, [move A00 etc.]"+\
            "\n  - `kick`: kick, for example, afk player [kick Joe#3841 etc.]"+\
            "\n  - `help`: shows this message", 
            mention_author=False)
        
    async def on_message(self, message: discord.Message):
        if message.channel.id not in self.data["play_channels"]: return
        if message.content.startswith("md!"):
            command, *args = message.content[3:].strip().lower().split()
            async with message.channel.typing():
                match command:
                    case "calc":  await self.g_calc (message, command, args)
                    case "play":  await self.g_play (message, command, args)
                    case "stop":  await self.g_stop (message, command, args)
                    case "start": await self.g_start(message, command, args)
                    case "move":  await self.g_move (message, command, args)
                    case "kick":  await self.g_kick (message, command, args)
                    case "help":  await self.g_help (message, command, args)
                    case c: await message.reply(f"unknown command \"{c}\"")
        
if __name__=="__main__":
    bot = MyBot()
    bot.run(bot.data["token"])
