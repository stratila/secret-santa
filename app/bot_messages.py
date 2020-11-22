start_message = '''
Привет, {}! 👋 Я бот, который назначит вам тайного Санту. 🤖🎅🏻\n
Но чтобы все сработало хорошо, помоги мне заполнить некоторые контактные данные о вас. ☺️👇
'''

request_phone_message = '''
Пришлите, пожалуйста, свой номер телефона. ➕3️⃣8️⃣0️⃣⛄... (подсказка: нажмите на кнопочку внизу)
Это нужно для того, чтобы тайный Санта знал Ваш контакт для корректного отправления подарка. 🎅🏻📲
'''

phone_button_text = 'Отправить номер телефона'

request_address_message = '''Теперь нужно заполнить контактные данные. 😌🎁📬\n
{}, укажите ваши город, адрес почтового отделения или номер почтового отделения. 🏣📩'''

correct_address_text = 'Правильно ли заполнены контактные данные? (Если нет, тогда нажмите соответвующую \
кнопку и перезаполни)😉👇\n\n`{}`'

request_present_message = '''Теперь подумайте хорошенько, что желаете получить от тайного Санты!
И... напишите мне! 🎁🎅🏻🦌❄️'''

correct_present_text = '''Убедись, что хотите именно "_{}_" в качестве подарка. 🤩🎁✅
Правильно ли сделан выбор?\n
(Если нет, тогда нажмите соответвующую кнопку и перезаполните)😉👇'''

room_invitation_text = '''И так... ☃️ Когда мы пришли к тому, что мы знаем, чего именно хотим, то самое время найти\
 единомышленников - тайных Сант. 🎅🏻👩🏼‍🦰👩🏼‍💼🎁👨‍💻👸🏻⛄️

Поэтому вам нужно либо возглавить содумцев, создав *новую комнату*, либо подключится к *существующей комнате*. 📭

Если вы хотите *изменить* ваши *адрес достваки* и *желаемый подарок*, просто нажмите на команду /reset ✍️

Выбери подходящий вариант! 😌👇
'''

room_created_message = '''Вы создали комнату и готовы! ✅🥳 

*Скопируйте* и *отправьте* идентификатор /room{0} своим друзьям чтобы они вошли в комнату. 📲

❕Когда весь ваш состав присоединится и нажмёт на кнопку *Готов*, нажмите *Старт* для назначения тайного Санты для \
каждого участника комнаты. 🎅🏻🎁🦌👉🏻📭

Вы можете отправить сообщение участникам с помощью команды: _/notify текст сообщения_

P.S Если вы создали комнату ошибочно или хотите распустить участников, отправьте мне команду /drop{0} ☃️'''


already_in_room_message = '''Вы уже находитесь в комнате {0} 🦌😁⛷

P.S Если вы создали комнату ошибочно или хотите распустить участников отправь мне команду /drop{0} 🌨'''

already_in_room_message2 = '''Вы уже находитесь в комнате {0} 🦌😁⛷

P.S Для выхода введите команду /exit{0} 🚪🎅🏻'''

room_dropped_owner_message = '''Вы распустили комнату и удалили всех участников! 🌬🎅🏻'''

room_dropped_participant_message = '''Пользователь {} распустил комнату! ❄️☃️'''

room_join_message = '''{0}, Вы присоединились к комнате, которую создал {2}! 🚪️✅🥳 

Скопируйте и отправьте идентификатор /room{1} своим друзьям чтобы они вошли в комнату. 📲

Вы можете отправить сообщение участникам с помощью команды: /notify текст сообщения

P.S Для выхода введите команду /exit{1}'''

room_exit_message = '{}, Вы покинули комнату {}! 🚷🚪🎅🏻'

room_join_alert_message = '''💡 Пользователь {} присоеденился к комнате {} 🥳'''

room_exit_alert_message = '''💡 Пользователь {} покинул комнату {} 🏃‍♂️'''

room_exists_message = '''Чтобы присоеденится к комнате введите её команду-идентификатор в формате:

 `/room0123456789` 📲🚪
 
Вы можете попросить команду у *своего друга*, который уже *создал комнату*. 😌🎅🏻

Для отображения _предыдущего меню_ о присоединении к комнатам отправьте мне любое сообщение. 📩'''

ready_message = '''Чтобы начать назначение тайного Санты участникам, каждый из присутсвующих в комнате должен\
 подтвердить свою готовность. *Готовы?* 🎅🏻✅'''

user_ready_message = '''✅ Вы готовы принимать участие в конкурсе!
Дождитесь пока остальные участники нажмут кнопку \
*Готов* и создатель комнаты *начнет* конкурс. 🎅🏻'''

user_ready_alert_message = '💡 Пользователь {} готов ✅⛷🎅🏻'

user_doesnt_ready_owner_message = '💡 Пользователь {} не готов. Дождитесь сообщения о его готовности\
 и повторите Старт. 📲🎅🏻'

user_doesnt_ready_participant_message = '''⚠️ Создатель комнаты {} хочет запустить назначение тайного Санты.\
 Нажимите, пожалуйтста, на кнопку Готов для начала назначения. ✅🎅🏻'''

room_owner_alone_message = '''Вы не можете начать конкурс, пока в комнате *никого нет*.\
 Подождитие присоединения других пользователей. ☃️

Для этого *отправьте* им идентификатор комнаты /room{} 📲🎅🏻'''

inform_alone_message = '💬 Никого нет в комнате'

room_everyone_ready_message = '''Создатель комнаты - {} начал конкурс! \
 Все подтвердили свою готовность к назначению тайных Сант! 🦌🌨🎅🏻'''

secret_santa_message = '''🤫🤫🤫 <b>ВНИМАНИЕ! СЕКРЕТНОЕ СООБЩЕНИЕ! НЕ ПОКАЗЫВАЙ ЕГО ОСТАЛЬНЫМ!</b> 🤫🤫🤫

🎅🏻 Вы назначены тайным Сантой для пользователя {}.

📞 <b>Телефон пользователя:</b> {}

📭 <b>Контактные данные пользователя:</b> {}

🎁 <b>Желание пользователя:</b> {}'''

secret_santa_message_clean = '''🤫🤫🤫 ВНИМАНИЕ! СЕКРЕТНОЕ СООБЩЕНИЕ! НЕ ПОКАЗЫВАЙ ЕГО ОСТАЛЬНЫМ! 🤫🤫🤫

🎅🏻 Вы назначены тайным Сантой для пользователя {}.

📞 Телефон пользователя: {}

📭 Контактные данные пользователя: {}

🎁 Желание пользователя: {}'''

help_message = '''Привет, я бот - Секретный Санта! И в этом сообщении я быстро постараюсь ввести тебя в курс дела.

*Что я делаю?*
Представим, что существует группа людей, которым нужно в тайне друг от друга распределить подарки между собой. 
Никто из этой группы людей распределением заниматься не должен. Эту роль играю я - Бот.

*Что нужно для того, чтобы начать игру?*
В начале работы со мной я запрашиваю некоторую контакную информацию, которая будет использоваться исключительно группой\
 людей, решающих распределить подарки между собой. По пунктам:
*1)* Номер телефона (для того, чтобы ваш знакомый знал, кому отправлять подарок).
*2)* Адрес почтового отделения.
*3)* Желаемый подарок.

*Можно ли изменить введенные данные?*
Да, в любой момент Вы можете нажать на команду /reset и ввести все заново, пока Вы не находитесь в комнате (см. раздел\
 "Каким образом собрать группу людей?")

*Каким образом собрать группу людей?*
Чтобы распределение подарков происходило только между определенной группой людей, в боте существуют *комнаты*.
Комната - вирутальное пространство c уникальным идентификатором, где собираются пользователи бота (что-то вроде чата).
После заполнения контактной информации у Вас спрашивают, хотите ли вы подключиться к *существующей комнате* или создать\
 *новую комнату*?

*Как создать комнату?*
После заполнения контактной информации Вам нужно нажать на кнопку "Создать новую комнату". После этого вы становитесь\
 создателем комнаты и получаете идентификатор комнаты в формате /room0123456789.
Не забудьте поделиться им со своим друзьями. У вас есть возможность начать распределение подарков, после того, когда\
 как минимум еще один пользователь будет в комнате.
Все подключившиеся пользователи должны подтвердить свою готовность, нажав кнопку "Готов" перед распределением подарков.
Создатель комнаты может использовать команду `/notify текст сообщения`, чтобы передать сообщение участникам комнаты.

*Как подключиться к комнате?*
После заполнения контактной информации Вам достаточно отправить идентификатор в формате /room0123456789, полученный\
 от создателя комнаты. Вы подлючитесь к комнате и увидете всю информацию о ней.
У вас будет кнопка "Готов", для подверждения готовности к старту распределения.
Участник комнаты может использовать команду `/notify текст сообщения`, чтобы передать сообщение участникам комнаты.

*Как начать распределение подарков?*
Если вы участник комнаты, нажмите на кнопку "Готов".
Если вы создатель комнаты, нажмите на кнопку "Старт".
Для тех, кто не готов, придет соответсвующее уведомление о том, что им необходимо подтвердить свою готовность.
После того, как создатель комнаты нажмет на старт, каждому участнику комнаты (включая создателя) придет сообщение с\
 информацией: кому он дарит подарок, его контактные данные и непосредственно информацию о желаемом подарке.
Далее комната автоматически удаляется и все участники возращаются к меню выбора комнат, где они могут создать или\
 выбрать комнату, а также изменить контактную информацию и желаемый подарок.

Приятного использования!
'''

phone_button_text_denied = 'Не указывать номер'

not_phone_number_info = '''💁🏻‍♀️ Вы не указали номер телефона. Вы всегда сможете сделать это позже.

⬇️Нажми на кнопку, чтобы продолжить⬇️'''

skip_phone_button_text = 'Продолжить'

proper_usage_of_notify_text = '📝 Корректный формат отправки сообщения: `/notify текст сообщения`'
