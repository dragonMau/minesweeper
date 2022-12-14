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
        raise SyntaxError(f"index must be formattede as A00")
    try:
        r0 = "ABCDEFGHIJKLMNOPQ".find(a[0])
        r1 = int(a[1:3])
    except:
        raise SyntaxError(f"index must be formattede as A00")
    if r0 == -1 or r1 < 0 or r1 > 29:
        raise KeyError(f"no such cell {a}")
    return r0, r1

class MyBot(discord.Client):
    data: dict[
        "parser": Parser,
        "active_games": list[int],
        "token": str,
        "play_channels": list[int],
        "games_by_id": dict[
            int: dict[
                "started": bool,
                "admin": int,
                "game": minesweeper.Game,
                "players": dict[
                    int: dict[
                        "blown": bool,
                        "turn": bool
    ]]]]]
    
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
            
    def g_s_configure_args(self, args: list[str]) -> tuple[int, int, int]:
        h, w, m = 17, 30, None
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
        if m is None: m = int(h*w/4.85)
        return h, w, m
    
    def g_s_get_all_active_players(self, count_blown=False) -> list[int]:
        ac_p = []
        for game in self.data["games_by_id"].values():
            ac_p.extend(id for id, pl in game["players"].items()
                        if not pl["blown"] or count_blown)
        return ac_p
    
    def g_s_register_players(self, mentions, admin) -> list[int]:
        players = []
        ac_p = self.g_s_get_all_active_players()
        for i in mentions+[admin]:
            if i not in players+[self.user.id]:
                if i in ac_p:
                    raise KeyError(f"<@{i}> already playing another game.")
                players.append(i)
        random.shuffle(players)
        return players
    
    def g_s_get_player(self, pid: int) -> tuple[int, bool]:
        """returns tuple (game_id, is_admin)
        
        game_id = 0 if player is not playing"""
        if pid in self.g_s_get_all_active_players(count_blown=True):
            for gid, g in self.data["games_by_id"].items():
                for p in g["players"].keys():
                    if p == pid:
                        return (gid, g["admin"] == p)
        else:
            return (0, False)
    
    def g_s_get_turn(self, game) -> int:
        for k, player in game["players"].items():
            if player["turn"]: return k
        return 0
    
    def g_s_switch_turn(self, game):
        next = False
        for v in game["players"].values():
            if next and not v["blown"]:
                v["turn"] = True; return
            if v["turn"]:
                v["turn"], next = False, True
        for v in game["players"].values():
            if not v["blown"]:
                v["turn"] = True; return
    
    async def g_s_victory(self, message: discord.Message, game: dict):
        pass # todo
    
    async def g_s_loose(self, message: discord.Message, game: dict):
        pass # todo
    
    async def g_s_continue(self, message: discord.Message, game: dict):
        pass # todo
    
    async def g_play(self, message: discord.Message, command: str, args: list[str]) -> int:
        if len(self.data["active_games"]) > 5:
            message.reply(f"There is too much active games now."); return 0
            
        height, width, mines = self.g_s_configure_args(args)
        if height*width < mines:
            await message.reply(
                f"This amount of mines ({mines}) cant fit in field {(width, height)}.".replace(",", ";"))
            return 0
        
        try: players = self.g_s_register_players(
            [i.id for i in message.mentions], message.author.id)
        except KeyError as e: await message.reply(f"{e}"); return 1
        
        self.data["games_by_id"][message.id] = {
            "started": False,
            "admin": message.author.id,
            "game": minesweeper.Game((width, height), mines),
            "players": {p: {"blown": False, "turn": False} for p in players}
        }
        
        head = f"minesweepr, {mines=};\nplayers:"
        body = ''.join([f"\n  - <@{pid}>" for pid in players])
        tail = "\nsend `md!start` to start this game or `md!stop` to cancel"
        await message.reply(head+body+tail)
        return 0
    
    async def g_leave(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass # todo
    
    async def g_stop(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass # todo
    
    async def g_start(self, message: discord.Message, command: str, args: list[str]) -> int:
        gid, isa = self.g_s_get_player(message.author.id)
        if gid == 0: 
            await message.reply("You are not in any game now."); return 0
        game = self.data["games_by_id"][gid]
        
        if game["started"]:
            await message.reply("This game is already started."); return 0
        if not isa:
            await message.reply("Only admin of the game can start it."); return 0
        
        self.g_s_switch_turn()
        cont = f"turn: <@{self.g_s_get_turn(game)}>\n"
        await message.reply(cont, file=update_field(game["game"]))
        return 0
        
    async def g_move(self, message: discord.Message, command: str, args: list[str]) -> int:
        pid = message.author.id
        gid, isa = self.g_s_get_player(pid)
        if gid == 0:
            await message.reply("You are not in any game now.")
            return 0
        
        game = self.data["games_by_id"][gid]
        turn = self.g_s_get_turn(game)
        if turn != pid:
            await message.reply(f"It is <@{turn}> turn!")
            return 0
        try:
            r = game["game"].open(*open_cell(''.join(args)))
        except (SyntaxError, KeyError) as e:
            await message.reply(f"{e}"); return 0
        match r[0]:
            case -1:
                await message.reply(f"cell {''.join(args)} already opened")
            case 0:
                if "won" in r[1]: await self.g_s_victory(message, game)
                else: await self.g_s_loose(message, game)
            case 1: await self.g_s_continue(message, game)
        return 0
    
    async def g_kick(self, message: discord.Message, command: str, args: list[str]) -> int:
        pass # todo
            
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
                    case "leave": await self.g_leave(message, command, args)
                    case c: await message.reply(f"unknown command \"{c}\"")
        
if __name__=="__main__":
    bot = MyBot()
    bot.run(bot.data["token"])
