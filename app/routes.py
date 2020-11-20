from app import app, db, telegram_bot
from app.models import User, Room
from config import Config
from app.bot_state import BotSate
from flask import request
from telebot import types
from config import Config
import random
import json
import re
from app.bot_messages import start_message, request_phone_message, request_address_message, phone_button_text, \
    correct_address_text, request_present_message, correct_present_text, room_invitation_text, room_created_message, \
    already_in_room_message, room_dropped_owner_message, room_dropped_participant_message, room_join_alert_message, \
    room_join_message, room_exists_message, room_exit_alert_message, room_exit_message, already_in_room_message2, \
    ready_message, user_ready_alert_message, user_ready_message, user_doesnt_ready_owner_message, \
    user_doesnt_ready_participant_message, room_owner_alone_message, room_everyone_ready_message, secret_santa_message,\
    secret_santa_message_clean, help_message, phone_button_text_denied, not_phone_number_info, inform_alone_message, \
    skip_phone_button_text


# место для вебхука
@app.route('/')
def index():
    return 'HI'


@app.route('/' + Config.BOT_TOKEN, methods=['POST'])
def getMessage():
    telegram_bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/wh")
def webhook():
    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(url='https://secret-santa-kyiv.herokuapp.com/' + Config.BOT_TOKEN)
    return "!", 200


def request_phone_number(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton(text=phone_button_text, request_contact=True))
    markup.add(types.KeyboardButton(text=phone_button_text_denied))
    telegram_bot.send_message(text=request_phone_message, chat_id=chat_id,
                              reply_markup=markup, disable_notification=True)


def confirm_phone_number_lack(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton(text=skip_phone_button_text))
    telegram_bot.send_message(text=not_phone_number_info, chat_id=chat_id, reply_markup=markup,
                              disable_notification=True)


def request_address(chat_id, first_name):
    telegram_bot.send_message(text=request_address_message.format(first_name),
                              chat_id=chat_id, disable_notification=True)


def confirm_address(chat_id):
    user = User.query.get(chat_id)
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton(text='Да',
                                              callback_data=json.dumps({'addr': True})))
        markup.add(types.InlineKeyboardButton(text='Нет',
                                              callback_data=json.dumps({'addr': False})))
        telegram_bot.send_message(text=correct_address_text.format(user.address), chat_id=chat_id,
                                  reply_markup=markup, parse_mode='Markdown', disable_notification=True)
    except Exception as e:
        user.address = None
        db.session.commit()
        request_address(user.id, user.first_name)


def request_present(chat_id):
    telegram_bot.send_message(text=request_present_message, chat_id=chat_id, disable_notification=True)


def confirm_present(chat_id):
    user = User.query.get(chat_id)
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton(text='Да',
                                              callback_data=json.dumps({'prz': True})))
        markup.add(types.InlineKeyboardButton(text='Нет',
                                              callback_data=json.dumps({'prz': False})))
        telegram_bot.send_message(text=correct_present_text.format(user.present), chat_id=chat_id,
                                  reply_markup=markup, parse_mode='Markdown', disable_notification=True)
    except Exception as e:
        user.present = None
        db.session.commit()
        request_present(user.id)


def request_room_invitation(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text='Создать новую комнату',
                                          callback_data=json.dumps({'inv': True})))
    markup.add(types.InlineKeyboardButton(text='Подключится к существующей',
                                          callback_data=json.dumps({'inv': False})))
    telegram_bot.send_message(text=room_invitation_text, chat_id=chat_id,
                              reply_markup=markup, parse_mode='Markdown', disable_notification=True)


def request_room_owner_panel(chat_id, first_name, room_identifier):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text='Старт',
                                          callback_data=json.dumps({'strt': True})))
    telegram_bot.send_message(text=room_created_message.format(room_identifier),
                              chat_id=chat_id, reply_markup=markup, parse_mode='Markdown', disable_notification=True)


def request_ready(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text='Готов!',
                                          callback_data=json.dumps({'rdy': True})))
    telegram_bot.send_message(text=ready_message, chat_id=chat_id,
                              reply_markup=markup, parse_mode='Markdown', disable_notification=True)


@telegram_bot.message_handler(commands=['help'])
def send_help(message):
    telegram_bot.send_message(chat_id=message.from_user.id, text=help_message,
                              parse_mode='Markdown', disable_notification=True)


@telegram_bot.message_handler(commands=['start'])
def auth_user(message):
    if User.query.filter_by(id=message.from_user.id).first():
        check_state(message)
    else:
        user = User(id=message.from_user.id,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    state=BotSate.PHONE)

        db.session.add(user)
        db.session.commit()
        telegram_bot.send_message(chat_id=user.id,
                                  text=start_message.format(user.first_name),
                                  disable_notification=True)
        request_phone_number(message.from_user.id)


@telegram_bot.message_handler(commands=['reset'])
def reset_contact_data(message):
    user = User.query.get(message.chat.id)
    if user and user.state == BotSate.ROOM_CHOICE:
        user.address = None
        user.present = None
        user.phone_number = None
        user.state = BotSate.PHONE
        db.session.commit()
        request_phone_number(user.id)


@telegram_bot.message_handler(regexp=r'/drop\w{10}\b')
def drop_room(message, end=False):
    user = User.query.filter_by(id=message.chat.id).first()
    if user.participant is not None:
        room = Room.query.filter_by(identifier=user.participant.identifier).first()
    else:
        room = None

    if room is not None and user.state == BotSate.IN_ROOM_CREATOR and user.id == room.owner_id:
        for u in room.users:
            u.participant = None
            u.state = BotSate.ROOM_CHOICE
            db.session.query(User).filter_by(id=u.id).update({"ready": False})  # сбрасываем готовность
            if u.id == user.id:
                telegram_bot.send_message(chat_id=u.id,
                                          text=room_dropped_owner_message, disable_notification=True)
            else:
                telegram_bot.send_message(chat_id=u.id,
                                          text=room_dropped_participant_message.format(user.first_name),
                                          disable_notification=True)
            if not end:
                request_room_invitation(u.id)
        db.session.delete(room)
        db.session.commit()
    else:
        check_state(message)


@telegram_bot.message_handler(regexp=r'/room\w{10}\b')
def join_room(message):
    identifier = re.search(r'/room\w{10}\b', message.text).group(0)[5:]
    user = User.query.filter_by(id=message.chat.id).first()
    room = Room.query.filter_by(identifier=identifier).first()

    if room is not None and user.state == BotSate.ROOM_CHOICE:
        user.participant = room
        user.state = BotSate.IN_ROOM_USER
        for u in room.users:
            if u.id != user.id:
                telegram_bot.send_message(chat_id=u.id,
                                          text=room_join_alert_message.format(user.first_name,
                                                                              user.participant.identifier),
                                          disable_notification=True)
            else:
                owner_name = User.query.filter_by(id=user.participant.owner_id).first().first_name
                telegram_bot.send_message(chat_id=user.id,
                                          text=room_join_message.format(user.first_name,
                                                                        user.participant.identifier,
                                                                        owner_name),
                                          disable_notification=True)
                request_ready(user.id)
        db.session.commit()
    else:
        check_state(message)


@telegram_bot.message_handler(regexp=r'/exit\w{10}\b')
def exit_room(message):
    identifier = re.search(r'/exit\w{10}\b', message.text).group(0)[5:]
    user = User.query.filter_by(id=message.chat.id).first()
    room = Room.query.filter_by(identifier=identifier).first()

    if room is not None and (user.state == BotSate.IN_ROOM_USER or user.state == BotSate.IN_ROOM_USER_READY):
        user.participant = None
        user.state = BotSate.ROOM_CHOICE
        db.session.query(User).filter_by(id=user.id).update({"ready": False})

        telegram_bot.send_message(chat_id=user.id,
                                  text=room_exit_message.format(user.first_name, room.identifier),
                                  disable_notification=True)

        for u in room.users:
            if u.id != user.id:
                telegram_bot.send_message(chat_id=u.id, text=room_exit_alert_message.format(user.first_name,
                                                                                            room.identifier),
                                          disable_notification=True)
        db.session.commit()
        request_room_invitation(user.id)
    else:
        check_state(message)


@telegram_bot.message_handler(commands=['notify'])
def notify_room_participants(message):
    if message.text == '/notify':
        return
    user = User.query.filter_by(id=message.from_user.id).first()
    if user.state == BotSate.IN_ROOM_CREATOR or user.state == BotSate.IN_ROOM_USER \
            or user.state == BotSate.IN_ROOM_USER_READY:  # отправлять уведомления тем кто в комнате
        telegram_bot.delete_message(message.chat.id, message.message_id)  # удалить сообщение со слэшем
        room_users = user.participant.users
        for room_user in room_users:
            telegram_bot.send_message(chat_id=room_user.id,
                                      text='💬 {}: {}'.format(concatenate_name(user), message.text[8:]),
                                      disable_notification=True)
    else:
        check_state(message)


# навигация по проверке состояния пользователя
@telegram_bot.message_handler(func=lambda message: True)
def check_state(message):
    user = User.query.filter_by(id=message.from_user.id).first()
    if user is None:
        auth_user(message)
        return

    if user.state == BotSate.PHONE:
        if message.text == phone_button_text_denied:
            user.state = BotSate.NO_PHONE
            db.session.commit()
            confirm_phone_number_lack(message.chat.id)
        else:
            request_phone_number(message.chat.id)
    elif user.state == BotSate.NO_PHONE:
        if message.text == skip_phone_button_text:
            user.state = BotSate.ADDRESS
            db.session.commit()
            request_address(user.id, user.first_name)
        else:
            confirm_phone_number_lack(message.chat.id)
    elif user.state == BotSate.ADDRESS:
        if user.address is not None:
            confirm_address(message.chat.id)
        else:
            user.address = message.text
            db.session.commit()
            confirm_address(message.chat.id)
    elif user.state == BotSate.PRESENT:
        if user.present is not None:
            confirm_present(message.chat.id)
        else:
            user.present = message.text
            db.session.commit()
            confirm_present(message.chat.id)
    elif user.state == BotSate.IN_ROOM_CREATOR:
        request_room_owner_panel(message.chat.id, user.first_name, user.participant.identifier)
    elif user.state == BotSate.ROOM_CHOICE:
        request_room_invitation(message.chat.id)
    elif user.state == BotSate.IN_ROOM_USER:
        request_ready(message.chat.id)


@telegram_bot.message_handler(content_types=['contact'])
def handle_phone_number(message):
    user = User.query.get(message.chat.id)
    if user.state == BotSate.PHONE:
        user.state = BotSate.ADDRESS
        user.phone_number = message.contact.phone_number
        db.session.commit()
        request_address(message.chat.id, user.first_name)
    else:
        check_state(message)


@telegram_bot.callback_query_handler(lambda query: json.loads(query.data).get('addr') is not None)
def validate_address(query):
    choice = json.loads(query.data).get('addr')
    user = User.query.get(query.message.chat.id)
    if user.state != BotSate.ADDRESS:
        return
    if choice:
        user.state = BotSate.PRESENT
        db.session.commit()
        telegram_bot.delete_message(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id)
        request_present(query.message.chat.id)
    else:
        user.address = None
        db.session.commit()
        telegram_bot.delete_message(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id)
        request_address(query.message.chat.id, user.first_name)


@telegram_bot.callback_query_handler(lambda query: json.loads(query.data).get('prz') is not None)
def validate_present(query):
    choice = json.loads(query.data).get('prz')
    user = User.query.get(query.message.chat.id)
    if user.state != BotSate.PRESENT:
        return
    if choice:
        user.state = BotSate.ROOM_CHOICE
        db.session.commit()
        telegram_bot.delete_message(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id)
        #telegram_bot.send_message(chat_id=query.message.chat.id, text='Пока что думаем над реализацией')
        #telegram_bot.send_sticker(chat_id=query.message.chat.id,
        #                          data='CAACAgIAAxkBAAIHP1-exwjIqmwebjY-1nACsJOqWG4gAAIaAANaDDcVO0MG9OddsLIeBA')
        request_room_invitation(query.message.chat.id)
    else:
        user.present = None
        db.session.commit()
        telegram_bot.delete_message(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id)
        request_present(query.message.chat.id)


@telegram_bot.callback_query_handler(lambda query: json.loads(query.data).get('inv') is not None)
def handle_room_joining(query):
    choice = json.loads(query.data).get('inv')  # True - кнопка создания, False - кнопка присоединения
    user = User.query.get(query.message.chat.id)
    if user.state < BotSate.ROOM_CHOICE:  # ничего не делать если не в меню выбора кнопок или не в комнате
        return
    if choice:
        if user.room is None:
            room = Room(owner_id=user.id)
            user.participant = room
            user.state = BotSate.IN_ROOM_CREATOR
            # создатель комнаты готов по-умолчанию
            db.session.query(User).filter_by(id=query.message.chat.id).update({"ready": True})
            db.session.add(room)
            db.session.commit()

            request_room_owner_panel(query.message.chat.id, user.first_name, room.identifier)
            telegram_bot.delete_message(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id)
        else:
            if user.id == user.participant.owner_id:
                telegram_bot.send_message(text=already_in_room_message.format(user.participant.identifier),
                                          chat_id=query.message.chat.id, disable_notification=True)
            else:
                telegram_bot.send_message(text=already_in_room_message2.format(user.participant.identifier),
                                          chat_id=query.message.chat.id, disable_notification=True)
    else:
        if user.room is None:
            telegram_bot.send_message(text=room_exists_message,
                                      chat_id=query.message.chat.id,
                                      parse_mode='Markdown', disable_notification=True)
            telegram_bot.delete_message(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id)
        else:
            if user.id == user.participant.owner_id:
                telegram_bot.send_message(text=already_in_room_message.format(user.participant.identifier),
                                          chat_id=query.message.chat.id, disable_notification=True)
            else:
                telegram_bot.send_message(text=already_in_room_message2.format(user.participant.identifier),
                                          chat_id=query.message.chat.id, disable_notification=True)


@telegram_bot.callback_query_handler(lambda query: json.loads(query.data).get('rdy') is not None)
def handle_room_ready(query):
    ready = json.loads(query.data).get('rdy')
    user = User.query.get(query.message.chat.id)
    if ready and user.state == BotSate.IN_ROOM_USER:
        db.session.query(User).filter_by(id=user.id).update({"ready": True})
        user.state = BotSate.IN_ROOM_USER_READY
        db.session.commit()
        for u in user.participant.users:
            if u.id != user.id:
                telegram_bot.send_message(chat_id=u.id,
                                          text=user_ready_alert_message.format(user.first_name),
                                          disable_notification=True)
            else:
                telegram_bot.delete_message(chat_id=u.id, message_id=query.message.message_id)
                telegram_bot.send_message(chat_id=u.id, text=user_ready_message, parse_mode='Markdown',
                                          disable_notification=True)


# возвращает кол-во готовых пользователей в комнате
# и отсылает уведомления тем, кто не готов
def check_ready(room_users, room_owner):
    ready_users_count = 0
    try:
        for u in room_users:
            if u.ready:
                ready_users_count += 1
            else:
                telegram_bot.send_message(chat_id=room_owner.id,
                                          text=user_doesnt_ready_owner_message.format(u.first_name),
                                          disable_notification=True)
                telegram_bot.send_message(chat_id=u.id,
                                          text=user_doesnt_ready_participant_message.format(room_owner.first_name),
                                          disable_notification=True)
                request_ready(chat_id=u.id)

        # в комнате только создатель
        if ready_users_count == 1:
            telegram_bot.send_message(chat_id=room_owner.id,
                                      text=room_owner_alone_message.format(room_owner.participant.identifier),
                                      parse_mode='Markdown',
                                      disable_notification=True)
        return ready_users_count
    except Exception:
        return ready_users_count


# создать полную текстовую строку пользователя
def concatenate_name(user):
    full = user.first_name
    if user.last_name is not None:
        full += ' ' + user.last_name
    if user.username is not None:
        full += ' (@' + user.username + ')'
    return full


# форматирует сообщение назначения тайного санты
def assign_santa(user, santa):
    contact_data = concatenate_name(santa)
    try:
        message_text = secret_santa_message.format(contact_data, santa.phone_number, santa.address, santa.present)
        telegram_bot.send_message(chat_id=user.id, text=message_text, parse_mode='HTML', disable_notification=True)
    except Exception as e:  # ошибка форматирования HTML
        clean_message_test = secret_santa_message_clean.format(contact_data, santa.phone_number, santa.address,
                                                               santa.present)
        telegram_bot.send_message(chat_id=user.id, text=clean_message_test, disable_notification=True)


@telegram_bot.callback_query_handler(lambda query: json.loads(query.data).get('strt') is not None)
def handle_room_owner_start(query):
    room_owner = User.query.get(query.message.chat.id)  # создатель комнаты
    room_users = room_owner.participant.users  # AppenderBaseQuery все участники комнаты
    room_users_count = User.query.filter_by(room=room_owner.participant.id).count()  # всего участников комнаты
    room_users_ready_count = check_ready(room_users, room_owner)  # кол-во готовых пользователей

    # если в комнате только создатель или не все пользователи готовы
    # отменить распределение тайных сант до тех пор пока все не будут готовы
    if room_users_count == 1 or room_users_count != room_users_ready_count:
        return

    santa_ids = [user.id for user in room_users]

    for user in room_users:
        telegram_bot.send_message(chat_id=user.id, text=room_everyone_ready_message.format(room_owner.first_name),
                                  disable_notification=True)

        santa_for = random.choice(santa_ids)
        while santa_for == user.id:  # никто не может быть тайным сантой для себя самого
            santa_for = random.choice(santa_ids)
        santa_ids.remove(santa_for)

        santa = User.query.filter_by(id=santa_for).first()
        assign_santa(user, santa)  # назначить санту santa для пользователя user

    drop_room(query.message, end=True)
