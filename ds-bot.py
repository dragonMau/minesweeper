import json


import discord, cv2
from py_expression_eval import Expression, Parser
from io import BytesIO

import minesweeper
import painter


def update_field(game) -> BytesIO:
    arr = painter.from_2d(game.get_field(), painter.maps.default)
    return discord.File(BytesIO(cv2.imencode(".png", arr)[1]), "field.png")

def open_cell(ooo):
    while True:
        a = ooo.upper()
        if len(a) != 3:
            print(f"index must be formattede as A00")
            continue
        try:
            r0 = "ABCDEFGHIJKLMNOPQ".find(a[0])
            r1 = int(a[1:3])
        except:
            print(f"index must be formattede as A00")
            continue
        if r0 == -1 or r1 < 0 or r1 > 29:
            print(f"no such cell {a}")
            continue
        return r0, r1

class MyBot(discord.Client):
    data: dict
    
    def __init__(self, *, loop=None, **options):
        with open("d://Users/mseli/data/2.txt", "r") as f:
            self.data = json.load(f)
            
        self.data["parser"] = Parser()
        
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(loop=loop, intents=intents, **options)
        
    async def on_ready(self):
        print(f"logged in as {self.user.name}")
        # await self.close()
        
    async def on_message(self, message: discord.Message):
        if message.channel.id not in self.data["play_channels"]: return
        if message.content.startswith("md!"):
            command, *args = message.content[3:].strip().split()
            async with message.channel.typing():
                match command:
                    case "calc":
                        try:
                            exp: Expression = self.data["parser"].parse(''.join(args))
                            await message.reply(f"={exp.evaluate({})}")
                        except Exception as e:
                            await message.reply(f"{e}")
                    case "play":
                        if self.data["game_id"] == 0:
                            self.data["game_id"] = message.id
                            self.data["game_admin"] = message.author
                            self.data["game"] = minesweeper.Game((30, 17), 100)
                            self.data["players"] = [i for i in message.mentions if i != self.user]+[message.author]
                            self.data["turn"] = self.data["players"][0]
                            self.data["blown"] = {}
                            for i in self.data["players"]:
                                self.data["blown"][i] = False
                            await message.reply(f"minesweeper; players:\n  - "+\
                                "\n  - ".join(map(lambda e: e.name+'#'+e.discriminator,self.data['players']))+\
                                "\nsend `md!start` to start this game or `md!stop` to cancel")
                        else:
                            await message.reply(f"there is an active game")
                    case "stop":
                        if self.data["game_id"] == 0:
                            await message.reply("there is no active games now!")
                            return
                        if any((message.author.guild_permissions.administrator,
                            message.author == self.data["game_admin"])):
                            self.data["game_id"] = 0
                            await message.reply("game stopped")
                        else:
                            await message.reply("you have no permission to stop this game")
                    case "start":
                        if self.data["game_id"] == 0:
                            await message.reply("there is no active games now!")
                            return
                        self.data["game"].field[8][15].mine = False
                        self.data["game"].open(8, 15)
                        await message.reply(
                            f"turn: {self.data['turn'].name}#{self.data['turn'].discriminator};",
                            file=update_field(self.data['game'])
                            )
                    case "move":
                        if self.data["game_id"] == 0:
                            await message.reply("there is no active games now!")
                            return
                        if (t:=self.data["turn"]) != message.author:
                            await message.reply(f"it is {t} turn")
                            return
                        r = self.data["game"].open(*open_cell(''.join(args)))
                        match r[0]:
                            case -1: await message.reply(f"cell {''.join(args)} already opened")
                            case 0:
                                if "won" in r[1]:
                                    await message.reply(f"All mines are defeated!", file=update_field(self.data["game"]))
                                    self.data["game_id"] = 0
                                else:
                                    self.data["game"].over = False
                                    self.data["blown"][t] = True
                                    while True:
                                        self.data["turn"] = self.data["players"][int(
                                            (self.data["players"].index(self.data["turn"])+1)\
                                            %len(self.data["players"]))]
                                        if not self.data["blown"][self.data["turn"]]: break
                                        if self.data["turn"] == t:
                                            self.data["game"].over = True
                                            self.data["game_id"] = 0
                                            await message.reply(f":boom: :boom: :boom:\n"+\
                                                                f"Game over: All players were blown up.",
                                                                file=update_field(self.data["game"]))
                                            return
                                        
                                    await message.reply(f":boom: {t.name}#{t.discriminator} was blown up!"+\
                                                        f"\nturn: {self.data['turn']}",
                                                        file=update_field(self.data["game"]))
                            case 1:
                                while True:
                                    self.data["turn"] = self.data["players"][int(
                                        (self.data["players"].index(self.data["turn"])+1)\
                                        %len(self.data["players"]))]
                                    if not self.data["blown"][self.data["turn"]]: break
                                await message.reply(f"\nturn: {self.data['turn']}",
                                                    file=update_field(self.data["game"]))
                    case c:
                        await message.reply(f"unknown command \"{c}\"")
            
    # on message "start game" should ask 
    # minesweeper game, id; react :play:; game starts in <t:time+5:R>;
    # who will play (get by reactions "i play!")
    # after waiting time should send
    # game started; players; <field.image>; whose turn
    # on "help" send short instruction, [a00, idk]
    # on "stop" from creator stop game
    # on move answer if it is legall move[user, structure] and if it is
    # send players; <field.image>; whose turn; 
    # again (next turn i mean)
    # after someone blows-up add :blow: after his nickname and cut his next turns
    # after everyone blows-up send "you lose" and field with exposed bombs
    # after all bombs defeated send "you won" with all bombs marked (except blown)
    # and winners/loosers/total moves etc.
        
if __name__=="__main__":
    bot = MyBot()
    bot.run(bot.data["token"])
