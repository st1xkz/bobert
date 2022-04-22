import hikari
import lightbulb

import random
import asyncio


tfe_plugin = lightbulb.Plugin("2048")


@tfe_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="2048",
    description="Starts a 2048 game",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_twentyfortyeight(ctx: lightbulb.Context) -> None:
    available_commands = ["w", "a", "s", "d", "end"]
    await ctx.respond(
        "2048 has started. Use `WASD` keys to move. Type \"end\" to end the game."
    )
    
    def moveNumbers(input, board):
        up = False
        down = False
        left = False
        right = False
        alreadyMoved = [[False] * 4 for n in range(4)]
        if input == "w":
            up = True
        elif input == "s":
            down = True
        elif input == "a":
            left = True
        else:
            right = True
        
        for k in range(4):
            for l in range(4):
                stop = False
                limit = 0
                if down or right:
                    limit = 3
                a = 0
                b = 0
                if up:
                    a = l
                    b = k
                elif down:
                    a = 3 - l
                    b = k
                elif left:
                    a = k
                    b = l
                else:
                    a = k
                    b = 3 - l
                
                while not stop:
                    if up or down:
                        c = a - 1
                        if down:
                            c = a + 1
                        if a == limit:
                            stop = True
                        else:
                            if board[c][b] == 0:
                                board[c][b] = board[a][b]
                                board[a][b] = 0
                                a = c
                            elif board[c][b] == board[a][b] and alreadyMoved[c][b] != True:
                                board[c][b] = board[c][b] * 2
                                board[a][b] = 0
                                alreadyMoved[c][b] = True
                                stop = True
                            else:
                                stop = True
                    else:
                        c = b - 1
                        if right:
                            c = b + 1
                            if b == limit:
                                stop = True
                            else:
                                if board[a][c] == 0:
                                    board[a][c] = board[a][b]
                                    board[a][b] = 0
                                    b = c
                                elif board[a][c] == board[a][b] and alreadyMoved[a][c] != True:
                                    board[a][c] = board[a][c] * 2
                                    board[a][b] = 0
                                    alreadyMoved[a][c] = True
                                    stop = True
                                else:
                                    stop = True
        
    end = False
    win = False
    start = True
    board = [[0] * 4 for n in range(4)]
    empty2 = 0
    empty = 0
    emptyX = []
    emptyY = []
    input = ''
    counter = 0
    while not end:
        canMove = False
        empty2 = 0
        if start:
            randX = random.randint(0, 3)
            randY = random.randint(0, 3)
            board[randX][randY] = 2
            out = '``` -------------------\n'
            
            for i in range(4):
                for j in range(4):
                    if i == 0:
                        if j == 0:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j - 1]:
                                canMove = True
                        else:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1] or board[i][j] == board[i][j - 1]:
                                canMove = True
                    elif i == 3:
                        if j == 0:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j + 1]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1]:
                                canMove = True
                        else:
                            if board[i][j] == board[i][j + 1] or board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1]:
                                canMove = True
                    else:
                        if j == 0:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j + 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                        else:
                            if board[i][j] == board[i][j + 1] or board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                    
                    if board[i][j] == 2048:
                        win = True
                    if board[i][j] == 0:
                        empty2 += 1
                        out += '|    '
                    elif board[i][j] > 0 and board[i][j] < 10:
                        out += '|  ' + str(board[i][j]) + ' '
                    elif board[i][j] >= 10 and board[i][j] < 100:
                        out += '| ' + str(board[i][j]) + ' '
                    elif board[i][j] >= 100 and board[i][j] < 1000:
                        out += '| ' + str(board[i][j])
                    elif board[i][j] >= 1000 and board[i][j] < 10000:
                        out += '|' + str(board[i][j])
                out += '|\n'
                
                if i != 3:
                    out += '|----+----+----+----|\n'
            out += ' -------------------```'
            if start:
                msg2 = await ctx.respond(out)
            else:
                await msg2.edit(content=out)
            if win:
                await ctx.respond(
                    "You won!"
                )
                self.add_xp(ctx.author.id, 10)
                self.add_badge(ctx.author.id, 1)
                return
            elif empty2 == 0 and not canMove:
                await ctx.respond(
                    "Game over, you lost. Maybe next time!"
                )
                self.add_xp2(ctx.author.id, counter)
                return
            valid = False
            while not valid:
                try:
                    msg = await ctx.bot.wait_for(hikari.GuildMessageCreateEvent, timeout=600)
                except asyncio.TimeoutError:
                    await ctx.respond(
                        "2048 has been timed out due to **10 minutes** of inactivity.",
                        reply=True,
                        mentions_reply=True
                    )
                    return
                if msg.get_channel() == ctx.get_channel() and msg.author == ctx.author:
                    if msg.content in available_commands:
                        content = msg.content
                        if content == "end":
                            await ctx.respond(
                                "Game ended."
                            )
                            return
                        valid = True
                    await msg.message.delete()
            board2 = [row[:] for row in board]
            moveNumbers(content, board)
            for k in range(4):
                for l in range(4):
                    if board[k][l] == 0:
                        empty += 1
                        emptyX.append(k)
                        emptyY.append(l)
                        
            if board != board2 and empty != 0:
                pos = random.randint(0, empty - 1)
                board[emptyX[pos]][emptyY[pos]] = 2 + (random.randint(0, 1) * 2)
                counter += 1
            empty = 0
            emptyX = []
            emptyY = []
            start = False


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tfe_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tfe_plugin)