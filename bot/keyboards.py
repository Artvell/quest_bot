# -*- coding:utf-8 -*-
from telebot.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import calendar
import datetime
from config import months
import calendar
import geopy.distance
from database import get_from_db,get_from_db_maps

def main_kb():
    button1=KeyboardButton('Все КвестРумы ✔️')
    button2=KeyboardButton('Поиск по жанрам 🔍')
    button3=KeyboardButton('Ближайшие КвестРумы 📡')
    button4=KeyboardButton('❗️ Акции ❗️')
    button5=KeyboardButton("📞 Связаться")
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    main_kb.add(button1)
    main_kb.add(button2)
    main_kb.add(button3)
    main_kb.add(button4)
    main_kb.add(button5)
    return main_kb

def all_questrooms(result,dop):
    inline_kb=InlineKeyboardMarkup()
    if len(result)%2==0:
        for i in range(0,len(result),2):
            inline_kb.add(InlineKeyboardButton(result[i],callback_data=result[i]),InlineKeyboardButton(result[i+1],callback_data=result[i+1]))
    else:
        for i in range(0,len(result)-1,2):
            inline_kb.add(InlineKeyboardButton(result[i],callback_data=result[i]),InlineKeyboardButton(result[i+1],callback_data=result[i+1]))
        inline_kb.add(InlineKeyboardButton(result[-1],callback_data=result[-1]))
    if dop!='':
        dop_but=InlineKeyboardButton("⬅️ Назад",callback_data=dop)
        inline_kb.add(dop_but)
    return inline_kb

def loc():
    locat=KeyboardButton("📌Отправить местоположение",request_location=True)
    back=KeyboardButton('◀️ Назад')
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(locat)
    kb.row(back)
    return kb

def near(x):
    distan={}
    company=get_from_db('company','','')
    company=[b[0] for b in company]
    company=set(company)
    company=list(company)
    print(company)
    coords=get_from_db_maps()
    res=[]
    for loc in coords:
        dist=geopy.distance.vincenty(x,loc).km
        cn=get_from_db('company','longitude',loc[0])
        distan[cn[0][0]]=dist
    for com in company:
        print(com)
        if com!="Квестория":
            if distan[com]<5:
                res.append(com)
        else:
            continue
    return res
def genres():
    reply_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    button1=KeyboardButton('Перформанс👺👻💀')
    button2=KeyboardButton('Логические🕵🏻')
    button3=KeyboardButton('Детские👨‍👩‍👧‍👦')
    button4=KeyboardButton('◀️ Назад')
    reply_kb.add(button1)
    reply_kb.add(button2)
    reply_kb.add(button3)
    reply_kb.add(button4)
    return reply_kb

def quests_map(long,lat,com):
    inline_kb=InlineKeyboardMarkup()
    coord="#"+long+"#"+lat
    button1=InlineKeyboardButton("Показать на карте🗺",callback_data=coord)
    button2=InlineKeyboardButton("Выбрать день",callback_data="calendar")
    inline_kb.add(button1)
    inline_kb.add(button2)
    if com!='':
        button3=InlineKeyboardButton("Ассортимент квеструма",callback_data=com)
        inline_kb.add(button3)
    return inline_kb
def calend(k):
    now=datetime.datetime.now()
    cal_kb=InlineKeyboardMarkup(row_width=7)
    b_list=[]
    y,m=0,0
    if now.month+k>12:
        y+=1
        m=(now.month+k)-12
    else:
        m=now.month+k
    t=months[calendar.month_abbr[m]]+" "+str(now.year+y)
    cal_kb.row(InlineKeyboardButton(t,callback_data=' '))
    for i in range(1,calendar.monthrange(now.year+y,m)[1]+1):
        if k==0:
            if i<now.day:
                b_list.append(InlineKeyboardButton(' ',callback_data=" "))
            else:
                b_list.append(InlineKeyboardButton(str(i),callback_data=str(i)))
        else:
            b_list.append(InlineKeyboardButton(str(i),callback_data=str(i)))
    for i in range(0,23,7):
        cal_kb.row(b_list[i],b_list[i+1],b_list[i+2],b_list[i+3],b_list[i+4],b_list[i+5],b_list[i+6])
    if calendar.monthrange(now.year+y,m)[1]==29:
        cal_kb.row(b_list[-1])
    elif calendar.monthrange(now.year+y,m)[1]==30:
        cal_kb.row(b_list[-2],b_list[-1])
    elif calendar.monthrange(now.year+y,m)[1]==31:
        cal_kb.row(b_list[-3],b_list[-2],b_list[-1])
    cal_kb.row(InlineKeyboardButton("⬅️",callback_data="calend_prev"),InlineKeyboardButton("➡️",callback_data="calend_next"))
    return cal_kb

def cont():
    phone=KeyboardButton("📞 Отправить контакт",request_contact=True)
    back=KeyboardButton('◀️ Назад')
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(phone)
    kb.row(back)
    return kb
