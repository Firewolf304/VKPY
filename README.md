# Небольшая лекция по этой штуке

  <div id="header" align="left">
    <img src="https://media.giphy.com/media/R9cQo06nQBpRe/giphy.gif" width="400"/></div>
This is my shit

##### 
Это работает на библиотеке vk_api и не более. Можно добавить сразу несколько аккаунтов в массивы token1 и massAPI и они будут работать все 1 разом на разных потоках. (раздельно данные потому что мне лень   потом листать и находить ошибки в токене, т.к. я балбес)

# Вот типо пример:
    token1 = [
    'vk1.a.fKWDiaDWlkand23123=-f=sf',
    'vk1.a.dawddawdawddwadddd=-f=sf'
    ]
    

А, да, эта хрень может вылететь внезапно из-за потери соединения

# Run
    ========================
    Linux:
    - git clone https://github.com/Firewolf304/PYVK.git
    - sudo pip install -r requirements.txt
    - sudo python3 main.py
    
    Windows:
    - runas /noprofile /user:*your name* "pip install -r requirements.txt"
     or just "pip install -r requirements.txt"
    - python3 main.py
    ========================

# Commands и че за файлы
Вообще все, что находится в папках/файлах, хз, записано в скрипте:

    pathstickets = str(pathlib.Path.cwd()) + "/NSTU/" # using NSTU folder
    pathgifben = str(pathlib.Path.cwd()) + "/ben/"    # using ben folder
    pathgifben = str(pathlib.Path.cwd()) + "/dalle/"  # using dalle folder
    deaths = str(pathlib.Path.cwd()) + "/death.txt"   # using death.txt file
    zak = str(pathlib.Path.cwd()) + "/zak.txt"        # using zak.txt file
#####
    NSTU - для команды !help: что лежит в с названием .png 
           будет выставлено в список. И последующее использование, 
           например, !глеб опубликует в сообщении ответом аргументом reply_to
    ben -  для команды !ben: тупо рандом из фраз переменной BEN (доп. добавление через 
           сумму str к основному тексту) и от каждой фразы загружается файл 
           от текста самой фразы (выпал какой-то текст из переменной и этот текст
           используется для открытия файла, я не понял че за аргумент 
           attachment влияет на ссылки, мне было лень разбирать особо)
    dalle - для команды !dalle *text*: тупо сохраняет туда "кэш" или че-то
           такого рода
    deaths - еще несовсем доработанная хрень с выходящими из беседы
           (выход из беседы или ивенте USER_LEFT)
    zak -  хрень json: штука, которая хранит json документ для отправки
           на сервер через аргумент forward для message.send... Тупо 
           в основном хранит массив conversation_message_ids, что являются
           переменными статического id сообщения определенного чата peer_id

Если Вы прочитали все это и даже че-то поняли, то я охуел с вас официально

# My profiles
<div id="badges">
  <a href="https://vk.com/remonterblyat">
    <img src="https://img.shields.io/badge/VK account-blue?style=for-the-badge&logo=vk&logoColor=cyan" alt="VK"/>
  </a>
  <a href="https://github.com/Firewolf304">
    <img src="https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=GitHub&logoColor=white" alt="GitHub"/>
  </a>
</div>
