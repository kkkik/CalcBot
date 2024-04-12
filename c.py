# -*- coding: utf-8 -*-
# @autor: t.me/F_E_Y
# Telegram: t.me/Se7en_Eyes

try:
    from telebot import TeleBot
    from telebot.types import InlineKeyboardButton as btn
    from telebot.types import InlineKeyboardMarkup as mk
    from telebot.types import KeyboardButton as kb
    from telebot.types import ReplyKeyboardMarkup as rep
except ImportError:
    try:
        print("Install Telebot Please Wait ...")
        subprocess.check_call(["pip", "install", "telebot"])
        subprocess.check_call("clear", shell=True)
        from kvsqlite.sync import Client
    except ImportError:
        try:
            print("Install Kvsqlite Please Wait ...")
            subprocess.check_call(["pip", "install", "kvsqlite"])
            subprocess.check_call("clear", shell=True)
            import sympy as sp
        except ImportError:
            try:
                print("Install sympy Please Wait ...")
                subprocess.check_call(["pip", "install", "sympy"])
                subprocess.check_call("clear", shell=True)
            except Exception as Erorr:
                print("Error : " +str(Erorr))
                exit(0)
from telebot import TeleBot
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as mk
from telebot.types import KeyboardButton as kb
from kvsqlite.sync import Client
import sympy as sp

db = Client('elhakem.v2', "Calculation")

token = input("Enter Token")

bot = TeleBot(token=token,skip_pending=True, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(regexp='^/start$')
def start_message(message):
    user_id = message.from_user.id
    things = ["C", "⌫", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "00", "0", ".", "="]
    keyboard = mk(row_width=4)
    last_calculation = db.get(f"last_calculation_{user_id}") if db.exists(f"last_calculation_{user_id}") else "0"
    keyboard.add(btn(last_calculation, callback_data="none"))
    buttons = [btn(cu, callback_data=f"{cu}") for cu in things]
    pairs = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
    for pair in pairs:
        keyboard.row(*pair)
    x = bot.reply_to(message,'• مرحبا بك في بوت الالة الحاسبة ، استخدم الازرار الادناة في حل مسألتك الخاصة', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c: True)
def call_data(call):
    message = call.message
    bot.clear_step_handler(message)
    cid, data, mid = call.from_user.id, call.data, call.message.id
    mains = ["÷", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "00", "0", "."]
    
    if data == "C":
        last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
        if last_calculation == "0":
            return bot.answer_callback_query(call.id, text=f'لا يوجد شئ لحذفه!', show_alert=True)
        db.set(f"last_calculation_{cid}", "0")
        edit_message(call)
    
    if data == "%":
        last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
        last_calculation+= "×0.01"
        result = resolve_code(last_calculation)
        result_without_decimal = remove_decimal(float(result))
        db.set(f"last_calculation_{cid}", str(result_without_decimal))
        edit_message(call)
        
    if data in mains:
        last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
        last_calculation+= str(data)
        if last_calculation.lstrip("0") == "":
            db.set(f"last_calculation_{cid}", "0")
            edit_message(call)
        else:
            db.set(f"last_calculation_{cid}", last_calculation.lstrip("0"))
            edit_message(call)
    
    if data == "=":
        last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
        if last_calculation == "0":
            return
        try:
            result = resolve_code(last_calculation.lstrip("0"))
        except:
            return bot.answer_callback_query(call.id, text=f'عملية حسابية خاطئة!', show_alert=True)
        result_without_decimal = remove_decimal(float(result))
        db.set(f"last_calculation_{cid}", str(result_without_decimal))
        edit_message(call)
    
    if data == "⌫":
        last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
        if last_calculation == "0":
            return bot.answer_callback_query(call.id, text=f'لا يوجد شئ لحذفه!', show_alert=True)
        last_calculation = last_calculation[:-1]
        if last_calculation.lstrip("0") == "":
            db.set(f"last_calculation_{cid}", "0")
            edit_message(call)
        else:
            db.set(f"last_calculation_{cid}", last_calculation.lstrip("0"))
            edit_message(call)

        
def edit_message(call):
    cid, data, mid = call.from_user.id, call.data, call.message.id
    things = ["C", "⌫", "%", "÷", "7", "8", "9", "×", "4", "5", "6", "-", "1", "2", "3", "+", "00", "0", ".", "="]
    keyboard = mk(row_width=4)
    last_calculation = db.get(f"last_calculation_{cid}") if db.exists(f"last_calculation_{cid}") else "0"
    keyboard.add(btn(last_calculation, callback_data="none"))
    buttons = [btn(cu, callback_data=f"{cu}") for cu in things]
    pairs = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
    for pair in pairs:
        keyboard.row(*pair)
    try:
        bot.edit_message_text(chat_id=cid, text='• مرحبا بك في بوت الالة الحاسبة ، استخدم الازرار الادناة في حل مسألتك الخاصة', message_id=mid, reply_markup=keyboard)
    except:
        pass
    
def remove_decimal(number):
    return int(number) if number.is_integer() else round(number, 100000)
    
def resolve_code(text):
    text = text.replace("×", "*")
    text = text.replace("÷", "/")
    expression = sp.sympify(text)
    result = expression.evalf()
    return remove_decimal(float(result))


bot.infinity_polling()
