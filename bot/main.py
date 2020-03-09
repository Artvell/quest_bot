# -*- coding:utf-8 -*-
import telebot
from config import token, days
from database import *
from keyboards import *
import calendar as cal

bot = telebot.TeleBot(token)
callback_data = {}  # {some_id:[day,month]}
calend_info = {}  # {some_id:[edit_id,month_id]}
quest_info = {}  # {some_id:quest_name}
indic={} # {some_id:1 or 0}
coords={}
comp={}
genrs={}
flag={}
admin_senders=[348545,153676,145109083,2716821]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "<b>Здравствуйте!</b>\nЯ ваш помощник по поиску информации и бронированию мест в квеструмах Ташкента!\nВыберите категорию:", parse_mode='HTML', reply_markup=main_kb())
    add_user(message.from_user.id)

@bot.message_handler(commands=['stat'])
def st(message):
    if message.from_user.id in admin_senders:
        bot.send_message(message.from_user.id,num_of_users())

@bot.message_handler(commands=['send'])
def send(message):
    if message.from_user.id in admin_senders:
        bot.send_message(message.from_user.id,"Пришлите то, что хотите разослать!\nПоддерживаются:\n- Текстовые сообщения\n- Картинки и фото\n- Видео\n -Видеосообщение (видео в круге)")
        flag[message.from_user.id]=1
        users_list=get_user_id()
        @bot.message_handler(content_types=["text"])
        def send_text(message):
                if flag[message.from_user.id]:
                    for user in users_list:
                        try:
                            bot.send_message(user[0],message.text,parse_mode="HTML")
                            print(user[0])
                        except telebot.apihelper.ApiException as e:
                            print(e)
                            if e.result.status_code==400:
                                delete_user(user[0])
                                continue
                        else:
                                continue
                    flag[message.from_user.id]=0
                    bot.send_message(message.from_user.id,"Разослано!")
        @bot.message_handler(content_types=['photo'])
        def send_photos(message):
                if flag[message.from_user.id]:
                    image_id=message.photo[0].file_id
                    for user in users_list:
                        try:
                            bot.send_photo(chat_id=user[0],photo=image_id,caption=message.caption,parse_mode="HTML")
                        except telebot.apihelper.ApiException as e:
                            if e.result.status_code==400:
                                delete_user(user[0])
                                continue
                        else:
                                continue
                    flag[message.from_user.id]=0
                    bot.send_message(message.from_user.id,"Разослано!")
        @bot.message_handler(content_types=["video"])
        def send_videos(message):
                if flag[message.from_user.id]:
                    video_id=message.video.file_id
                    for user in users_list:
                        try:
                            bot.send_video(user[0],video_id,parse_mode="HTML")
                        except telebot.apihelper.ApiException as e:
                            if e.result.status_code==400:
                                delete_user(user[0])
                                continue
                        else:
                                continue
                    flag[message.from_user.id]=0
                    bot.send_message(message.from_user.id,"Разослано!")
        @bot.message_handler(content_types=["video_note"])
        def send_video_notes(message):
                if flag[message.from_user.id]:
                    video_id=message.video_note.file_id
                    for user in users_list:
                        try:
                            bot.send_video_note(user[0],video_id)
                        except telebot.apihelper.ApiException as e:
                            if e.result.status_code==400:
                                delete_user(user[0])
                                continue
                        else:
                                continue
                    flag[message.from_user.id]=0
                    bot.send_message(message.from_user.id,"Разослано!")


@bot.message_handler(func=lambda message: message.text == "Все КвестРумы ✔️")
def all_quest(message):
    res = get_from_db("company", '', '')
    res = [b[0] for b in res]
    res = set(res)
    res = list(res)
    indic[message.from_user.id]=1
    genrs[message.from_user.id]=0
    bot.send_message(message.from_user.id, "<b>Выберите КвестРум</b>", parse_mode="HTML", reply_markup=all_questrooms(res,''))

@bot.callback_query_handler(func=lambda c: c.data == "Все")
def all_quest1(message):
    res = get_from_db("company", '', '')
    res = [b[0] for b in res]
    res = set(res)
    res = list(res)
    bot.send_message(message.from_user.id, "<b>Выберите КвестРум</b>", parse_mode="HTML", reply_markup=all_questrooms(res,''))

@bot.message_handler(func=lambda message: message.text == "📞 Связаться")
def tel(message):
    text="<b>Администратор:</b>\n+998903368866\n"
    bot.send_message(message.from_user.id,text,parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "Поиск по жанрам 🔍")
def genre(message):
    genrs[message.from_user.id]=1
    bot.send_message(message.from_user.id, "<b>Выберите жанр :</b>", parse_mode="HTML", reply_markup=genres())


@bot.message_handler(func=lambda message: message.text == "◀️ Назад")
def back(message):
    bot.send_message(message.from_user.id, "<b>Выберите категорию:</b>", parse_mode='HTML', reply_markup=main_kb())


@bot.message_handler(func=lambda message: message.text == "Перформанс👺👻💀")
def perfomance(message):
    res = get_from_db('name', 'genre', "Перформанс")
    res = [b[0] for b in res]
    indic[message.from_user.id]=1
    bot.send_message(message.from_user.id, "<b>Найдено!</b>", parse_mode="HTML", reply_markup=all_questrooms(res,""))

@bot.message_handler(func=lambda message: message.text == "Логические🕵🏻")
def logic(message):
    res = get_from_db('name', 'genre', "Логические")
    res = [b[0] for b in res]
    indic[message.from_user.id]=1
    bot.send_message(message.from_user.id, "<b>Найдено!</b>", parse_mode="HTML", reply_markup=all_questrooms(res,""))


@bot.message_handler(func=lambda message: message.text == "Детские👨‍👩‍👧‍👦")
def child(message):
    res = get_from_db('name', 'genre', "Детские")
    res = [b[0] for b in res]
    indic[message.from_user.id]=1
    bot.send_message(message.from_user.id, "<b>Найдено!</b>", parse_mode="HTML", reply_markup=all_questrooms(res,""))

@bot.message_handler(func=lambda message:message.text=="Ближайшие КвестРумы 📡")
def nearest(message):
    bot.send_message(message.from_user.id,"<b>Отправьте свои координаты.</b>",parse_mode="HTML",reply_markup=loc())
    @bot.message_handler(content_types=['location'])
    def map(message):
        genrs[message.from_user.id]=0
        coor=(message.location.latitude,message.location.longitude)
        b=near(coor)
        indic[message.from_user.id]=0
        coords[message.from_user.id]=coor
        if len(b)!=0:
            bot.send_message(message.from_user.id,"<b>Ближайшие КвестРумы: </b>", parse_mode="HTML",reply_markup=all_questrooms(b,''))
        else:
            bot.send_message(message.from_user.id,"<b>В пяти километрах от вас не найдено ни одного квеструма</b>",parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data == "/")
def map1(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    c=callback_query
    user_id = callback_query.from_user.id
    coor=(coords[user_id][0],coords[user_id][1])
    b=near(coor)
    bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    if len(b)!=0:
        bot.send_message(user_id,"<b>Ближайшие КвестРумы: </b>", parse_mode="HTML",reply_markup=all_questrooms(b,''))
    else:
        bot.send_message(user_id,"<b>В пяти километрах от вас не найдено ни одного квеструма</b>",parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == '❗️ Акции ❗️')
def sales(message):
    res = get_from_db('name', 'stock', 1)
    res = [b[0] for b in res]
    indic[message.from_user.id]=1
    genrs[message.from_user.id]=1
    if len(res) != 0:
        bot.send_message(message.from_user.id, "<b>Найдено!</b>", parse_mode="HTML", reply_markup=all_questrooms(res,''))
    else:
        bot.send_message(message.from_user.id, "<b>Нет действующих акций</b>", parse_mode="HTML")


@bot.callback_query_handler(func=lambda c: c.data[0] == "#")
def map(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    c = callback_query
    x, y = c.data.split("#")[1], c.data.split("#")[2]
    bot.send_location(user_id, float(x), float(y))


@bot.callback_query_handler(func=lambda c: c.data in days)
def cal_prev(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    now = datetime.datetime.now()
    ind = 0
    if now.month + calend_info[user_id][1] > 12:
        ind = now.month + calend_info[user_id][1] - 12
    else:
        ind = now.month + calend_info[user_id][1]
    month = months[cal.month_abbr[ind]]
    print(calend_info[user_id][1])
    day = callback_query.data
    callback_data[user_id] = [day, month]
    bot.delete_message(user_id,callback_query.message.message_id)
    bot.send_message(user_id, "<b>Принято.</b>\nПожалуйста отправьте нам свой контакт, в ближайшее время с вами свяжется администратор", parse_mode="HTML", reply_markup=cont())

    @bot.message_handler(content_types=['contact'])
    def phone_number(message):
        bot.send_message(message.from_user.id, "<b>Спасибо!</b>\nСкоро с Вами свяжется наш администратор", parse_mode="HTML", reply_markup=main_kb())
        phone = message.contact.phone_number
        name = message.contact.first_name if message.contact.first_name != None else "Неизвестно"
        surname = message.contact.last_name if message.contact.last_name != None else "Неизвестно"
        day = callback_data[message.from_user.id][0]
        month = callback_data[message.from_user.id][1]
        quest = quest_info[message.from_user.id]
        admin_id = get_from_db('admin_id', 'name', quest)[0][0]
        text = "<b>Имя:</b> {}\n<b>Фамилия:</b> {}\n<b>Квест:</b> {}\n<b>Дата:</b> {}, {}\n<b>Номер:</b> {}".format(name, surname, quest, month, day, phone)
        bot.send_message(admin_id,text,parse_mode="HTML")
        #bot.send_message(348545,text,parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data == "calendar")
def calendar(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    bot.delete_message(user_id,callback_query.message.message_id)
    mes = bot.send_message(user_id, "Пожалуйста, выберите день:", reply_markup=calend(0))
    calend_info[user_id] = [mes.message_id, 0]


@bot.callback_query_handler(func=lambda c: c.data == "calend_next")
def cal_next(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    if calend_info[user_id][1] < 2:
        calend_info[user_id][1] += 1
        bot.edit_message_reply_markup(user_id, message_id=calend_info[user_id][0], reply_markup=calend(calend_info[user_id][1]))


@bot.callback_query_handler(func=lambda c: c.data == "calend_prev")
def cal_prev(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    if calend_info[user_id][1] > 0:
        calend_info[user_id][1] -= 1
        bot.edit_message_reply_markup(user_id, message_id=calend_info[user_id][0], reply_markup=calend(calend_info[user_id][1]))


@bot.callback_query_handler(func=lambda c: (len(get_from_db('*', 'company', c.data)) != 0) and (c.data not in days))
def company_kb(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    c = callback_query
    text = f"КвестРум <b>{c.data}</b> приветствует вас!\nВ нашем ассортименте следующие квесты:"
    res = get_from_db('name', 'company', c.data)
    res = [b[0] for b in res]
    bot.delete_message(user_id,callback_query.message.message_id)
    print(indic[user_id])
    if indic[user_id]==0:
        comp[user_id]=c.data
        bot.send_message(user_id, text, parse_mode="HTML", reply_markup=all_questrooms(res,"/"))
    else:
        comp[user_id]=c.data
        bot.send_message(user_id, text, parse_mode="HTML", reply_markup=all_questrooms(res,''))

@bot.callback_query_handler(func=lambda c: (len(get_from_db('*', 'company', c.data)) == 0) and (c.data not in days))
def quest_kb(callback_query: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    c = callback_query
    image = get_from_db('image_link', 'name', c.data)[0][0]
    text = get_from_db('text', 'name', c.data)[0][0]
    long = get_from_db('longitude', 'name', c.data)[0][0]
    lat = get_from_db('latitude', 'name', c.data)[0][0]
    #text=[b[0] for b in text][0]
    #image=[b[0] for b in image][0]
    quest_info[user_id] = c.data
    #bot.delete_message(user_id,callback_query.message.message_id-1)
    img=f'<a href="{image}"> ‏ </a>'
    text=text+img
    bot.delete_message(user_id,callback_query.message.message_id)
    #bot.send_photo(user_id, image)
    if user_id in comp and genrs[user_id]==0:
        bot.send_message(user_id, text, parse_mode="HTML", reply_markup=quests_map(long, lat,comp[user_id]))
    else:
        bot.send_message(user_id, text, parse_mode="HTML", reply_markup=quests_map(long, lat,''))


bot.polling()
