import telebot

TOKEN = "8121545603:AAH7h6MRaKMi8b_Q1n0_0tUwxMAyt7rJgwQ"
bot = telebot.TeleBot(TOKEN)

def process_ticket(message):
    user_contact = message.text
    user = message.chat.username if message.chat.username else "Неизвестный пользователь"
    idd = message.chat.id
    print(f"Новый тикет от {user}: {user_contact}, ")  # Отправляем тикет в консоль
    bot.send_message(message.chat.id, "Спасибо! Ваш запрос отправлен. Мы с вами свяжемся.")
    bot.send_message(811933667, f"Новый тикет от {user}: {user_contact}, {idd}")


    

@bot.message_handler(commands = ["start", "services", "pricing", "contact","voicering","sound_recording","editing","voiceover_pricing","sound_recording_price","editing_pricing","info","make_ticket"])
def start_command(message):
    if message.text == "/start":
        bot.send_message(message.chat.id,"""Здравствуйте, вы попали в официальный бот студии звуко-записи "Название"
Использвуйте следуйщие команды для навигации в боте:

/services - ознакомление с нашими услугами

/pricing - сразу узнать расценки на различные услуги

/contact - связаться с менеджером или оставить заявку""")
    if message.text == "/services":
        bot.send_message(message.chat.id,"""Наша студия звукозаписи предлагает разнообразные услуги, включая озвучку, звукозапись, создание звуковых эффектов и музыкальную запись. Мы обеспечиваем высокое качество и индивидуальный подход к каждому проекту.
Для подробного ознакомления воспользуйтесь следующими командами:

/voicering Озвучка вашего текста нашими актерами

/sound_recording Запись на нашей студии

/editing Сведение и улучшение качества звука""")    
    if message.text == "/voicering":
        bot.send_message(message.chat.id,"""Мы можем озвучить ваш текст для рекламы, обучающего контента и тд.
                         
Для ознакомления с ценами /voiceover_pricing

Для заказа или связи с менеджером /contact""")
    if message.text == "/sound_recording":
        bot.send_message(message.chat.id,"""Вы можете записать вокал для музыки или озвучить, что то сами !
                         
Для ознакомления с ценами /sound_recording_price

Для заказа или связи с менеджером /contact""")
    if message.text == "/editing":
        bot.send_message(message.chat.id,"""Мы можем свести вам трек и обработать звук!
                         
Для ознакомления с ценами /editing_pricing

Для заказа или связи с менеджером /contact""")
        
        
    if message.text == "/pricing":
        bot.send_message(message.chat.id,"""Наши цены очень демократичны, ведь мы знаем цену деньгам

/voiceover_pricing - Цены на озвучку

/sound_recording_price  - Цена на запись в нашей студии

/editing_pricing - Цена за сведение""")  
    if message.text == "/voiceover_pricing":
        bot.send_message(message.chat.id,"""Мужской голос 200р за минуту
                         
женский 250р за минуту

Для заказа -> /contact""")
    if message.text == "/sound_recording_price":
        bot.send_message(message.chat.id,"""Дневное время (Час) 10:00 - 18:00 500р
Вечернее время (Час) 18:00 - 23:00 1000р

Для заказа -> /contact""")
    if message.text == "/editing_pricing":
        bot.send_message(message.chat.id,"""Ориентировочная стоимость 5000р за трек длиной до 3 минут

Для заказа -> /contact""")
        
        
    if message.text == "/contact":
        bot.send_message(message.chat.id,"""Контактная информация -> /info
Оставить заявку -> /make_ticket""")
    if message.text == "/make_ticket":
        bot.send_message(message.chat.id, "Напишите сюда свой телефон/телеграм/почту, и мы с вами свяжемся.")
        bot.register_next_step_handler(message, process_ticket)
    if message.text == "/info":
        bot.send_message(message.chat.id,"""Наш адрес - Санкт-Петербург, улица ...
Контактный телефон - +7(999)0000000
Почта - Grob_rec@gmail.com""")











bot.polling(none_stop = True, interval = 0 )