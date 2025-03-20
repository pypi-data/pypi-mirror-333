import discord
import pathlib
import sys
import os
ROOT_PATH = pathlib.Path(__file__).parents[1]
sys.path.append(os.path.join(ROOT_PATH, ''))
from operator_precedence_high_roller.parsing.command_parser import CommandParser
from operator_precedence_high_roller.parsing.enums.command_type import CommandType
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.computing.compute import Compute
from operator_precedence_high_roller.json_handling.gambling.gamble import Gamble
from operator_precedence_high_roller.json_handling.roll_saving.roll_save import RollSave
import operator_precedence_high_roller.message_validator as mv

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

async def handle_expr(message: discord.Message, compute: Compute, rollSave: RollSave, commandParser: CommandParser):
    result = (0,0)
    try:
        result = compute.compute_expr(commandParser.stack[1])
    except:
        handle_error(message)
    if compute.error or len(commandParser.stack) != 2:
        handle_error(message)
    else:
        rollSave.add_rolls_to_json()
        to_send = ""
        for i in range(len(compute.cocked_rolls)):
            to_send += 'Honor the cock. Roll ' + str(compute.cocked_rolls[i][1]) + ' was cocked. It would have been ' + str(compute.cocked_rolls[i][0]) + '\n'
        to_send += str(result[0]) + '\nDetails: ' + str(compute.all_lists_of_rolls) + '\nAverage: ' + str(result[1])
        if len(commandParser.stack) != 2 or (len(to_send)) > 2000:
            handle_error(message)
        await message.channel.send(to_send)

async def handle_gamble_start(message: discord.Message, gamble: Gamble):
    if not gamble.gambling():
        await message.channel.send('odds or evens?')
        gamble.update_gambling_state(True)

async def handle_gamble_bet(gamble: Gamble, commandParser: CommandParser):
    valid_bet = False
    try:    
        valid_bet = await gamble.determine_bet(commandParser.stack[1].token_info.lexeme)
    except:
        print('invalid bet')
    if valid_bet and gamble.gambling():
        await gamble.determine_result()
        gamble.update_gambling_state(False)

async def handle_recall_rolls(message: discord.Message, rollSave: RollSave, commandParser: CommandParser):
    if commandParser.command_type == CommandType.ERROR:
        await handle_error(message)
    elif len(commandParser.stack) == 2 and commandParser.stack[1].token_info.TokenType == TokenType.RECALL:
        rollSave.get_rolls_from_json()
        await message.channel.send(file=discord.File('bar_plots/bar_plot_' + message.author.name + '.png'))
    elif len(commandParser.stack) == 5:
        rollSave.get_rolls_from_json(
            die = commandParser.stack[3].token_info.lexeme
        )
        await message.channel.send(file=discord.File('bar_plots/bar_plot_' + message.author.name + '.png'))
    elif len(commandParser.stack) == 7:
        rollSave.get_rolls_from_json(
            hours = int(commandParser.stack[3].token_info.lexeme), 
            die = commandParser.stack[5].token_info.lexeme
        )
        await message.channel.send(file=discord.File('bar_plots/bar_plot_' + message.author.name + '.png'))
    else:
        await handle_error(message)

async def handle_error(message: discord.Message):
    await message.channel.send("https://tenor.com/view/blm-gif-25815938")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message: discord.Message):
    if not mv.channel_valid(message) and mv.message_is_command(message):
        handle_error(message)
    elif mv.message_is_command(message):
        compute = Compute()
        gamble = Gamble(message)
        rollSave = RollSave(message, compute)
        commandParser = CommandParser(message.content.lower())
        commandParser.parse_init()
        match commandParser.command_type:
            case CommandType.EXPR:
                await handle_expr(message, compute, rollSave, commandParser)
            case CommandType.GAMBLE_START:
                await handle_gamble_start(message, gamble)
            case CommandType.GAMBLE_BET:
                await handle_gamble_bet(gamble, commandParser)
            case CommandType.RECALL_ROLLS:
                await handle_recall_rolls(message, rollSave, commandParser)
            case CommandType.ERROR:
                await handle_error(message)
            case _:
                pass
            
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key) 
#python -m unittest discover tests