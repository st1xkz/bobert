import hikari
import lightbulb
import random


tictactoe_plugin = lightbulb.Plugin("tic-tac-toe")


player1 = ""
player2 = ""
turn = ""
gameOver = ""

board = []


@tictactoe_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="player_one",
    description="the user to play Tic-Tac-Toe with",
)
@lightbulb.option(
    name="player_two",
    description="the user to play Tic-Tac-Toe with",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_tictactoe(ctx: lightbulb.Context) -> None:
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = ["⬜", "⬜", "⬜" "⬜", "⬜", "⬜" "⬜", "⬜", "⬜"]
        turn = ""
        gameOver = False
        count = 0

        player1 = ctx.options.player_one
        player2 = ctx.options.player_two

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.respond(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.respond(f"It is {player1.mention}'s turn!")
        elif num == 2:
            turn = player2
            await ctx.respond(f"It is {player2.mention}'s turn!")

    else:
        await ctx.respond(
            "A game is already in progess! Please finish it before starting a new one."
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tictactoe_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tictactoe_plugin)
