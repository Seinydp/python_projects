import telebot
from datetime import datetime, timedelta
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7785609486:AAF7f9NJfIHaXFhoWgl6HPZihbz1MAxbQdw"
bot = telebot.TeleBot(TOKEN)

# добавил гитхаб
# тест гит адда 


viewer_text = {
"start": "Приветсвую тебя пользователь." ,
"commands" : "Установить расписание - /set_deff \nОставить сообщение разработчику - /make_ticket",
"ticket" : "Напишите свое обращение тут )"

}

time_tables = {
    "deff_timetable":  [[8,30],[9,15],[9,30],[10,15],[10,35],[11,15],[11,40],[12,20],[12,40],[13,25],[13,45],[14,30],[14,40],[15,25]],
    "every_30min" : [[0, 0], [0, 30], [1, 0], [1, 30], [2, 0], [2, 30], [3, 0], [3, 30], [4, 0], [4, 30], [5, 0], [5, 30], [6, 0], [6, 30], [7, 0], [7, 30], [8, 0], [8, 30], [9, 0], [9, 30], [10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [12, 30], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0], [15, 30], [16, 0], [16, 30], [17, 0], [17, 30], [18, 0], [18, 30], [19, 0], [19, 30], [20, 0], [20, 30], [21, 0], [21, 30], [22, 0], [22, 30], [23, 0], [23, 30]]
}

admin_id = 811933667

def load_from_json(filename): # выгрузка из json
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  

def save_to_json(data, filename): #сохранение в json 
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def change_value_json(id,action,value,object): #изменение значения в файле
    users_data = load_from_json("data.json")
    user_id  = str(id)
    if action == "change":
        users_data[user_id][value] = object
    elif action == "math":
        users_data[user_id][value] = users_data[user_id].get(value,0) + object
    save_to_json(users_data,"data.json")
    

def check_add(message):
    users_data = load_from_json("data.json")
    user_id  = str(message.chat.id)
    # print(user_id)
    mes_us = message.chat.username
    if user_id not in users_data :
        user = {"username": mes_us if mes_us else "unknown user", "visits" : 1}
        users_data[user_id] = user 

    else :
        users_data[user_id]["visits"] = users_data[user_id].get("visits",0) +1
    save_to_json(users_data,"data.json")
    
    return True

       
def time_until_next(message):
    now = datetime.now()
    users_data = load_from_json("data.json")
    user_id  = str(message.chat.id)
    target_times_list = []
    t_t = users_data[user_id]['time_table']
    
    for i in range (len(time_tables[t_t])):
        target_times_list.append(now.replace(hour=time_tables[t_t][i][0], minute=time_tables[t_t][i][1]))
    target_times = [t if t > now else t + timedelta(days=1) for t in target_times_list]
    next_time = min(target_times, key=lambda t: t - now)
    remaining_time = next_time - now
    return remaining_time, next_time.time(), target_times.index(next_time)

def time_table_availability(message):
    users_data = load_from_json("data.json")
    user_id  = str(message.chat.id)
    try:
        return(True if users_data[user_id]['time_table'] != None else False)
    except: return(False)
    
def last_time(remaining_time, next_time , id_chet, message): 
    users_data = load_from_json("data.json")
    user_id  = str(message.chat.id)
    if users_data[user_id]['time_table'] == "deff_timetable":
        if id_chet == 0 or id_chet % 2 == 0:
            answ = (f"Время до НАЧАЛА урока ({next_time}): {remaining_time}")
        else :
            answ = (f"Время до КОНЦА урока ({next_time}): {remaining_time}")
    else: answ = (f"Время до События ({next_time}): {remaining_time}")
    return answ

def make_time_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Узнать время")
    markup.add("Узнать время")
    return markup

def make_but_for_take_time_table(call_back_1,call_back_2,text_1,text_2):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text_1, callback_data=call_back_1)
    button2 = InlineKeyboardButton(text_2, callback_data=call_back_2)
    markup.add(button1, button2)
    return markup

def process_ticket(message):
    user_contact = message.text
    user = message.chat.username if message.chat.username else "Неизвестный пользователь"
    print(f"Новый тикет от {user}: {user_contact}, ")  # Отправляем тикет в консоль
    bot.send_message(message.chat.id, "Спасибо! Ваш запрос отправлен. Мы с вами свяжемся.")
    bot.send_message(admin_id, f"Новый тикет от {user}: {user_contact}")

def show_timetable(massage):
    user_key = str(massage.data)
    if user_key != "yes" and user_key != "no":
        timetable_info = ""
        for item in time_tables[user_key]:
            timetable_info += (f"{item[0]} часов {item[1]} минут\n")
        return timetable_info
    else : return None

def take_time_table(call):
    if call.data == "yes":
        users_data = load_from_json("data.json")
        user_id  = str(call.from_user.id)
        users_data[user_id]['time_table'] = str(call.data)
    else: print("no")


@bot.message_handler(commands = ["start","time","make_ticket","dl","set_deff","clear_deff","check_timetable"])
def start_command(message):
    check_add(message)
    if message.text == "/start":
        bot.send_message(message.chat.id, "Привет, Я бот считающий время!")
        bot.send_message(message.chat.id, "Напиши /set_deff \nВведи /make_ticket, чтобы оставить сообщение разработчику")
    elif message.text == "/make_ticket":
        bot.send_message(message.chat.id, "Свое обращение напиши")
        bot.register_next_step_handler(message, process_ticket)
    elif message.text == "/dl":
        bot.send_message(message.chat.id, "Кнопка убрана", reply_markup=ReplyKeyboardRemove() )
    elif message.text == "/set_deff":
        button_choose = make_but_for_take_time_table("deff_timetable","every_30min","расписание звонков","каждые 30 минут")
        bot.send_message(message.chat.id, "Выберите расписание чтобы ознакомится:", reply_markup=button_choose)
    return True
@bot.message_handler(func=lambda message: message.text == "Узнать время")
def handle_button_click(message):
    
    if check_add(message) == True and time_table_availability(message)== True:
        remaining_time, next_time , id_chet = time_until_next(message)
        bot.send_message(message.chat.id, answ:= last_time(remaining_time, next_time , id_chet,message))
        print(f"==========\n{answ},{datetime.now()}")
    else: bot.send_message(message.chat.id,"Вы не выбрали расписание. /set_deff")
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data != "yes" and call.data != "no":
        change_value_json(call.from_user.id, "change", "check", call.data)
        user_id = str(call.from_user.id)
        yes_no_button = make_but_for_take_time_table("yes","no","yes","no")
        bot.send_message(call.from_user.id, show_timetable(call), reply_markup=yes_no_button)
    elif call.data == "yes":
        print("зашел в ес")
        users_data = load_from_json("data.json")
        user_id  = str(call.from_user.id)
        change_value_json(call.from_user.id, "change", "time_table", users_data[user_id]['check'])
        bot.send_message(call.from_user.id, "Расписание установленно", reply_markup=make_time_button())
        make_time_button
    elif call.data == "no":
        button_choose = make_but_for_take_time_table("deff_timetable","every_30min","расписание звонков","каждые 30 минут")
        bot.send_message(call.from_user.id, "Выберите расписание чтобы ознакомится:", reply_markup=button_choose)
    

    
bot.polling(none_stop = True, interval = 0 )