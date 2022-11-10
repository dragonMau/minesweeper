import discord, json


class MyBot(discord.Client):
    def __init__(self, *, loop=None, **options):
        with open("d://Users/mseli/2.txt", "r") as f:
            self.data = json.load(f)
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(loop=loop, intents=intents, **options)
        
    async def on_ready(self):
        print(f"logged in as {self.user.name}")
        await self.close()
        
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
