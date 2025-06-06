import telebot
from telebot import types

f = open('token.ini', 'r', encoding='UTF-8')
TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)
f.close()
game = False
board = [' ' * 9]


def display_board(b):
    line = '|'.join(b[0:3])
    print(line)
    print('-' * 5)
    line = '|'.join(b[3:6])
    print(line)
    print('-')
    line = '|'.join(b[6:9])
    print(line)
def is_empty(b, index):
    return b[index] == ' '
def nbw(b):
    g = False
    for i in range(len(b)):
        if  is_empty(b, i):
            g = True
            break
    return g

def is_valid_move(b, index):
    res = (index >= 0) and (index <= 8) and is_empty(b, index)
    return res
def check_winner(b):
    winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6]]
    for winner in winners:
        if b[winner[0]] == b[winner[1]] == b[winner[2]] and b[winner[0]] != ' ':
            return b[winner[0]]
    return False


def make_move(b, index, symbol):
    b[index] = symbol


def c_k(call):
    reply_markup = types.InlineKeyboardMarkup()
    buttons = []
    for i in range(0, 9):
        if is_empty(board, i):
            buttons.append(types.InlineKeyboardButton(text=' ', callback_data=str(i + 1)))
        else:
            buttons.append(types.InlineKeyboardButton(text=board[i], callback_data=str(i + 1)))
    reply_markup.row(buttons[0], buttons[1], buttons[2])
    reply_markup.row(buttons[3], buttons[4], buttons[5])
    reply_markup.row(buttons[6], buttons[7], buttons[8])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=reply_markup)
@bot.message_handler(commands=['start'])
def start(message):
    global game
    global board
    game = True
    board = [' '] * 9
    reply_markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text='1', callback_data='1'),
        types.InlineKeyboardButton(text='2', callback_data='2'),
        types.InlineKeyboardButton(text='3', callback_data='3'),
        types.InlineKeyboardButton(text='4', callback_data='4'),
        types.InlineKeyboardButton(text='5', callback_data='5'),
        types.InlineKeyboardButton(text='6', callback_data='6'),
        types.InlineKeyboardButton(text='7', callback_data='7'),
        types.InlineKeyboardButton(text='8', callback_data='8'),
        types.InlineKeyboardButton(text='9', callback_data='9'),
    ]
    reply_markup.row(buttons[0], buttons[1], buttons[2],)
    reply_markup.row(buttons[3], buttons[4], buttons[5],)
    reply_markup.row(buttons[6], buttons[7], buttons[8],)
    bot.send_message(message.chat.id, f'Добро пожаловать в игру крестики-нолики \n'
                     f'Нажмите на кнопку для того, чтобы сделать ваш ход', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global game
    global board
    if game:
        index = int(call.data) - 1
        if is_valid_move(board, index):
            make_move(board, index, 'X')
            winner = check_winner(board)
            if winner:
                reply_markup = types.InlineKeyboardMarkup()
                c_k(call)
                reply_markup = types.ReplyKeyboardRemove()
                bot.send_message(call.message.chat.id, f'Выиграли {winner}!', reply_markup=reply_markup)
                game = False
            else:
                if nbw(board):
                    index = get_computer_move(board)
                    print(index)
                    make_move(board, index, 'O')
                    winner = check_winner(board)
                    if winner:
                        c_k(call)

                        reply_markup = types.ReplyKeyboardRemove()
                        bot.send_message(call.message.chat.id, f'Выиграли {winner}!', reply_markup=reply_markup)
                        game = False
                    else:
                        c_k(call)
                else:
                    c_k(call)
                    bot.send_message(call.message.chat.id, f'Победила дружба!')
                    game = False

        else:
                bot.answer_callback_query(call.id, 'Неверный ход. Попробуйте еще раз!')
    else:
        bot.answer_callback_query(call.id, 'Игра окончена. Нажмите /start, чтобы начать новую игру.')
def get_computer_move(b):
    # 1. Если может выиграть — выиграет
    for i in range(9):
        if is_empty(b, i):
            board_copy = b[:]
            make_move(board_copy, i, '0')
            if check_winner(board_copy) == '0':
                return i

    # 2. Если игрок может выиграть — блокирует
    for i in range(9):
        if is_empty(b, i):
            board_copy = b[:]
            make_move(board_copy, i, 'X')
            if check_winner(board_copy) == 'X':
                return i

    # 3. Стратегия хода: центр → угол → сторона
    for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if is_empty(b, i):
            return i
def get_computer_movey(b):
    for i in range(0, 9):
        if is_empty(b, i):
            board_copy = b[:]
            make_move(board_copy, i, '0')
            if check_winner(board_copy):
                return i
    for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if is_empty(b, i):
            return i


bot.polling()