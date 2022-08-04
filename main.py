import concurrent.futures
import threading
import os
import sys
import platform
import pathlib
import requests, json, base64
import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
import time
import psutil




busy = False


threads = 0


pathstickets = str(pathlib.Path.cwd()) + "/NSTU/"
pathgifben = str(pathlib.Path.cwd()) + "/ben/"
pathdalle = str(pathlib.Path.cwd()) + "/dalle/"
deaths = str(pathlib.Path.cwd()) + "/death.txt"
zak = str(pathlib.Path.cwd()) + "/zak.txt"

f = open(deaths,'w+')
if len(f.read()) == 0:
    print("No death")
    f.write("0")
f.close()

BEN = [
    'yes',
    'no',
    'hohoho',
    'ugh'
]

countRecconnect = 0 #пересоздание
messages = [
    "Привет, чекай закреп",
    "Привет, чекни закреп",
    "Привет, закреп чекай",
    "Закреп чекай, привет",
    "Привет, чекай закрепец",
    "закреп привет остальные идите нахуй",
    "Привет, чекай блять закреп",
    "Еще один... Чекай закреп",
    "привет, чекай закреп",
    "привет чекай закреп",
    "привет чекни закреп",
    "привет секнни закреп",
    "привет смотри закреп",
    "привет, смотри закреп",
    "привет наблюдай закреп",
    "Закреп привет, чекай",
    ", Закай чекреп привет",
    "Закай, прикреп чезай",
    "А ты подал согласие, новенький?",
    "    закреп закреп обожаю чекать закреп",
    "привет чекни закрпеп",
    "Привет, чекай мать",
    "Закреп, чекай привет",
    "Привет, чекай Олега"
]

token1 = [
    'vk.1.dawdawdawdawdawd',
    'vk1.a.dawdawdawdawddw'
] #token


if len(token1) == 0:
    print("No tokens")
    exit(404)

checker = [False]*len(token1)

def checkBusy():
    while 1:
        count = 1
        for i in range(len(checker)):
            if checker[i]:
                count += 1
        if count == len(token1):
            print("DETECT NULLBUSY!!!")
            busy = False



def detectPic(path):
    helptext = "Вот че есть: "
    files = os.listdir(path)
    for i in range(len(files)):
        if i < len(files) - 1:
            helptext += "!" + str(files[i]).split('.')[0] + ", "
        else:
            helptext += "!" + str(files[i]).split('.')[0]
    return helptext
def loadPic(user, message,event, session, vk):
    global busy

    if busy == False:
        busy = True

        if message == "help":
            text = detectPic(pathstickets)
            text += ", !ben"
            send(text, session, event, user)
            busy = False
        elif message.split(' ')[0] == "dalle":
            vk.messages.send(peer_id=event.peer_id, message="Обработка... Она займет немного времени",reply_to=int(event.message_id), random_id=0)
            print(user,"  WARNING! thread2 func freeze in some time!!!")
            print(user, "  Taking ","'"+str(message.split('dalle ')[1]) + "'")
            r = requests.post('https://backend.craiyon.com/generate', json={"prompt":message.split('dalle ')[1]}, timeout=800)
            sec = str(r.elapsed.total_seconds())
            if len(r.text) == 0:
                vk.messages.send(peer_id=event.peer_id, message="Запрос слишком большой или сервер DALL-E mini не отвечает\nОбщее время подключения: " + sec + " secs",
                                 reply_to=int(event.message_id), random_id=0,)
            r = json.loads(r.text)['images']
            attachment = []
            upload = VkUpload(session)
            for i in range(len(r)):
                f = open(pathdalle + "file" + str(i) + ".png", 'wb+')
                f.write(base64.b64decode(r[i].replace('\n','')))
                f.close()
                print(user,"Getting data file" + str(i)+".png")
                photo = upload.photo_messages(pathdalle + "file" + str(i) + ".png", event.peer_id)
                attachment.append(f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}_{photo[0]["access_key"]}')
            print(user, "end dalle!!!")
            vk.messages.send(peer_id=event.peer_id, message="Затраченное время ответа: " + sec + " secs", reply_to=int(event.message_id), random_id=0, attachment=attachment)
            busy = False
            return
        elif message == "ben":

            rnd = int(random.randrange(len(BEN)* 10000000000) / 10000000000)

            upload = VkUpload(session)
            photo = upload.document_message(pathgifben + BEN[rnd] + ".gif", event.peer_id)['doc']
            owner_id = photo['owner_id']
            photo_id = photo['id']
            #access_key = photo['access_key']
            busy = False
            attachment = f'doc{owner_id}_{photo_id}'
            vk.messages.send(peer_id=event.peer_id, message=BEN[rnd],reply_to=int(event.message_id),random_id=0, attachment=attachment)

        try:
            open(pathstickets + str(message) + ".png")
        except Exception:

            print(str(user) + ": ", "no file")
            busy = False
            return 0

        print(str(user) + ": ", "Loading file")
        upload = VkUpload(session)
        photo = upload.photo_messages(pathstickets + str(message) + ".png", event.peer_id)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        vk.messages.send(peer_id=event.peer_id, reply_to=int(event.message_id), random_id=0, attachment=attachment)
        busy = False

    else:
        global checker
        checker[int(str(user).split('user')[1])] = True
        print(str(user) + ": ", "user busy")




last = ""
def loger(token, user):

    print("Log info", user, "started")
    session = vk_api.VkApi(token=token)
    pol = VkLongPoll(session)
    vk = session.get_api()
    while 1:

        for event in pol.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                try:
                    info = vk.messages.getById(message_ids=event.message_id)['items'][0]
                    #print(info)
                    name1 = vk.users.get(user_ids=event.user_id)[0]
                    name2 = vk.users.get(user_ids=info['reply_message']['from_id'])[0]
                    mess = str(time.strftime('%d.%m.%Y|%H:%M:%S', time.localtime())) + " - " + \
                           str(event.type).split(".")[1] + " " + str(event.peer_id) + " - " + str(event.user_id) + " " + \
                           str(name1['first_name']) + " " + str(name1['last_name']) + \
                           ": " + "'" + event.text + "'" + " -> " + str(name2['first_name']) + " " + \
                           str(name2['last_name']) + ": '" + str(info['reply_message']['text']) + "'"
                    print(str(user + ": "), mess)

                    # try:
                    # print(user, vk.messages.getById(message_ids=event.message_id)['items'][0]['reply_message']['from_id'] == id)
                    # print(vk.messages.getById(message_ids=event.message_id)['items'][0]['reply_message'])
                    # except Exception: print("err")
                except Exception:
                    mess = str(time.strftime('%d.%m.%Y|%H:%M:%S'
                                             '', time.localtime())) + " - " +\
                        str(event.type).split(".")[1] + " " + str(event.peer_id) + " - " + str( \
                        event.user_id) + " " + str(vk.users.get(user_ids=event.user_id)[0]['first_name']) + " " + str( \
                        vk.users.get(user_ids=event.user_id)[0]['last_name']) + ": " + event.text.lower()
                    print(str(user + ": "), mess)
            else:
                break


bye = False
last = ""
def threadVk2(token, user):
    try:
        session = vk_api.VkApi(token=token)
        pol = VkLongPoll(session)
        vk = session.get_api()
        id = vk.account.getProfileInfo()['id']
        print("Token loaded: ID", user, "-", id)
        global bye, last
        if len(last) != 0:
            pol.listen().append(last)
            last = ""
        while 1:
            try:
                for event in pol.listen():
                    last = event
                    # if event.type != "VkEventType.USER_TYPING_IN_CHAT":
                    #print(str(user+": "), event.type)
                    if event.type == VkEventType.MESSAGE_NEW:
                        mes = vk.messages.getById(message_ids=event.message_id)['items'][0]
                        #print(mes)
                        if event.text.lower() == "пинг":
                            send("Да иди ты нахуй", session, event, user)
                            continue
                        elif event.text.lower() == "_debug" and event.user_id == 298669112:
                            #298669112
                            send(infoSys(), session, event, user)
                            continue
                        elif str(event.text.lower()).split('-')[0] == "_termux" and event.user_id == 298669112 and not(bye):
                            bye = True
                            try:
                                text = ""
                                if (sys.platform == "linux"): #"termux-battery-status"
                                    js = os.system(event.text.lower().replace('_',''))
                                    for i in range(len(list(js))):
                                        text += list(js)[i] + ": " + str(js[ list(js)[i]])
                                    send(text, session, event, user)
                                else:
                                    send("Платформа не подходит для данной операции", session, event, user)
                                    bye = False
                            except Exception as e:
                                print(user, "error _termux send:", e)
                                send("Ошибка или неизвестная команда", session, event, user)
                            bye = False
                            continue
                        elif event.text.lower() == "_закреп" and not(bye):
                            # reply + 0 byte
                            # reply + more byte
                            # command
                            bye = True
                            try:
                                #print(vk.messages.getById(message_ids=event.message_id)['items'][0]['reply_message']['id'])
                                #print(vk.messages.getByConversationMessageId(peer_id = event.peer_id, conversation_message_ids=int(vk.messages.getById(message_ids=event.message_id)['items'][0]['conversation_message_id'])))
                                f = open(zak, 'r')
                                f = f.read()

                                if len(f) > 0 and not(mes.get('reply_message')) and not(mes.get('fwd_messages')) and len(mes['attachments']) == 0:
                                    try:
                                        print(user, "_закреп: send ", f)
                                        vk.messages.send(peer_id=event.peer_id, message="", forward=f, random_id=0)
                                    except Exception as e:
                                        bye = False
                                        print(user,"error _закреп send:",e)
                                elif len(f) > 0 and not(mes.get('reply_message')) and not(mes.get('fwd_messages')) and len(mes['attachments']) > 0: # сообщение с вложением
                                    f = open(zak, 'w+')
                                    conv = int(mes['conversation_message_id'])
                                    js = {"owner_id": 0, "peer_id": 0, "conversation_message_ids": [], "message_ids": "",
                                          "is_reply": 0}
                                    conversation_message_ids = mes['conversation_message_id']

                                    ddd = [
                                        id,
                                        event.peer_id,
                                        conversation_message_ids,
                                        "",
                                        0
                                    ]
                                    for i in range(len(js.keys())):
                                        js[str(list(js.keys())[i])] = ddd[i]
                                    f.write(str(js).replace("'", '"'))
                                    f.close()
                                    print(user, "_закреп: loading ", js)
                                    send("Закреп сохранен", session, event, user)
                                elif mes.get('fwd_messages') and event.user_id == 298669112: # на пересланных
                                    f = open(zak, 'w+')
                                    conv = int(mes['conversation_message_id'])
                                    js = {"owner_id": 0, "peer_id": 0, "conversation_message_ids": [], "message_ids": "", "is_reply": 0}
                                    conversation_message_ids = []
                                    message_ids = []
                                    #print(vk.messages.getByConversationMessageId(peer_id=event.peer_id, conversation_message_ids=conv)['items'][0]['fwd_messages'])
                                    for i in vk.messages.getByConversationMessageId(peer_id=event.peer_id, conversation_message_ids=conv)['items'][0]['fwd_messages']:
                                        #f.write(str(i['conversation_message_id']) + ",")
                                        conversation_message_ids.append(i['conversation_message_id'])
                                        message_ids.append(i['id'])

                                    ddd = [
                                        id,
                                        event.peer_id,
                                        conversation_message_ids,
                                        "",
                                        0
                                    ]
                                    for i in range(len(js.keys())):
                                        js[str(list(js.keys())[i])] = ddd[i]
                                    f.write(str(js).replace("'",'"'))
                                    f.close()
                                    print(user, "_закреп: loading ", js)
                                    send("Закреп сохранен", session, event, user)
                                elif mes.get('reply_message') and event.user_id == 298669112: # на ответе (ОДНОМ И ТОЛЬКО ОДНОМ ОТВЕТЕ)
                                    f = open(zak, 'w+')
                                    conv = int(mes['conversation_message_id'])
                                    js = {"owner_id": 0, "peer_id": 0, "conversation_message_ids": [], "message_ids": "", "is_reply": 0}
                                    conversation_message_ids = vk.messages.getByConversationMessageId(peer_id=event.peer_id, conversation_message_ids=conv)['items'][0]['reply_message']['conversation_message_id']

                                    ddd = [
                                        id,
                                        event.peer_id,
                                        conversation_message_ids,
                                        "",
                                        0
                                    ]
                                    for i in range(len(js.keys())):
                                        js[str(list(js.keys())[i])] = ddd[i]
                                    f.write(str(js).replace("'",'"'))
                                    f.close()
                                    print(user, "_закреп: loading ", js)
                                    send("Закреп сохранен", session, event, user)
                                bye = False

                            except Exception as e:
                                bye = False
                                print(user,"error _закреп:",e)
                            continue
                        elif str(event.text.lower()).find("!") > -1 and len(str(event.text.lower()).split('!')) <= 2:
                            print(str(user + ": "), "Detected command", str(event.text).split('!')[1])
                            try:
                                loadPic(user, str(event.text).split('!')[1], event, session, vk)
                            except Exception as e:
                                print(user,"error loadpic:",e)
                        try:
                            if mes['reply_message']['from_id'] == id:
                                if event.text.lower() == "пошел нахуй" or event.text.lower() == "иди нахуй" or event.text.lower() == "пошёл нахуй":
                                    send("Говна сожри", session, event, user)
                                    continue
                        except Exception:0

                    elif event.type == VkEventType.CHAT_UPDATE:
                        if event.update_type == VkChatEventType.USER_JOINED and 0:  # Присоединение к беседе
                            rnd = int(random.randint(0, 5 * 100000000) / 100000000)
                            print(str(user + ": "), "Send '", messages[rnd], "' with waiting", rnd, "seconds")
                            time.sleep(rnd)
                            #print(str(user + ": "), event.update_type)
                            send(messages[rnd], session, event, user)
                            continue
                        elif event.update_type == VkChatEventType.USER_LEFT and 0:

                            if not(bye):
                                bye = True
                                try:
                                    f = open(deaths, 'r+')
                                    num = f.read().split('\n')[0]
                                    print(num)
                                    f.close()
                                except Exception as e:
                                    print("Error read death:", e)
                                    f.close()
                                text = "Я считаю, что он умер очень больно. Считаю, что мучался своей смерти. Жаль, конечно, этого добряка. Конечно он для детей не писал, но пару книжек, конечно, написал для детей... все равно жалко его для... его... Хороший был {0} человек".format(
                                    num)
                                try:
                                    f = open(deaths, 'w')
                                    print(str(int(num) + 1))
                                    f.write(str(int(num) + 1))
                                    f.close()
                                except Exception as e:
                                    print("error write", e)
                                print(str(user + ": "), "Send '", "*прощание*", "' with waiting", 0, "seconds")
                                send(text, session, event, user)
                                bye = False
                            continue
            except Exception as e:
                global countRecconnect
                print(user+" Error event:",e)
                countRecconnect += 1
                if (str(e).find("Read timed out") > -1 | str(e).find("Connection aborted") > -1) and 0:

                    thread = threading.Thread(target=loger, args=(token, user))
                    thread.start()
                    countRecconnect += 1
                    break


    except Exception as e :
        print(user + " Error thread:", e)







def send(mes, vksession, eventer, user):
    if eventer.from_chat:
        try:
            pol = VkLongPoll(vksession)
            vk = vksession.get_api()
            print(str(user) + ": sending '",str(mes) + "'")
            vksession.method('messages.send',{'chat_id': eventer.chat_id, 'message': mes, 'random_id': random.getrandbits(64)})
        except Exception as e: print(user,"error send:",e)
    #elif event.from_user:
        #session.method('messages.send',{'user_id': event.user_id, 'message': mes, 'random_id': random.getrandbits(64)})






def mem ():
    # mem = psutil.virtual_memory () Просмотр информации о памяти;
	mem_total = int(psutil.virtual_memory()[0]/1024/1024)
	mem_used = int(psutil.virtual_memory()[3] / 1024 / 1024)
	mem_per = int(psutil.virtual_memory()[2])
	mem_info = {
		'mem_total' : mem_total,
		'mem_used' : mem_used,
		'mem_per' : mem_per
	}
	return mem_info
 # Мониторинг использования жесткого диска:
def disk ():
	c_per = int (psutil.disk_usage('C:') [3]) # Просмотр информации об использовании диска: общее пространство, использованное, оставшееся, коэффициент занятости;
	d_per = int(psutil.disk_usage('D:')[3])
	e_per = int(psutil.disk_usage('E:')[3])
	# print(c_per,d_per,e_per,f_per)
	disk_info = {
		'c_per' : c_per,
		'd_per' : d_per,
		'e_per' : e_per,
	}
	return disk_info
 # Мониторинг сетевого трафика:
def network ():
    # network = psutil.net_io_counters () # Просмотр информации о сетевом трафике;
    network_sent = int (psutil.net_io_counters () [0] / 8/1024) #kb в секунду
    network_recv = int(psutil.net_io_counters()[1]/8/1024)
    network_info = {
		'network_sent' : network_sent,
		'network_recv' : network_recv
	}
    return network_info

def infoSys():
    global busy
    if not(busy):
        busy = True
        text = ""
        try:
            info = [' Система: {0} \n',
                    ' Использовано потоков: {0} \n',
                    ' Статус: {0} \n',
                    ' Количество рестартов: {0} \n',
                    ' Добавлено ботов: {0} \n',
                    ' Загрузка процессора: {0} \n================================\n',
                    ' Общий объем памяти (МБ): {0} \n',
                    ' Объем используемой памяти (МБ): {0} \n',
                    ' Использование памяти: {0} \n================================\n',
                    ' Полученный сетевой трафик (МБ): {0} \n',
                    ' Сетевой трафик отправлен (МБ): {0}\n================================\n'
                    #' Использование диска C: {0} \n',
                    #' Использование диска D: {0} \n',
                    #' Использование диска E: {0}'
            ]

            mem_info = mem()
            status = ""
            network_info = network()
            if (threading.active_count() - 1) / (len(token1) * 2) == 1:
                status = "normal"
            elif(threading.active_count() - 1) / (len(token1) * 2) > 1 and (threading.active_count() - 1) / (len(token1) * 2) < 3:
                status = "warning"
            else:
                status = "danger"
            data = [
                str(platform.platform()),
                str(threading.active_count()),
                status,
                countRecconnect,
                len(token1),
                str(int(psutil.cpu_percent(1))),
                mem_info['mem_total'],
                mem_info['mem_used'],
                mem_info['mem_per'],
                network_info['network_sent'],
                network_info['network_recv']
            ]
            if sys.platform == "win32":
                try:
                    disk_info = psutil.disk_partitions()
                    for i in range(len(disk_info)):
                        info.append('Использование диска ' + str(disk_info[i][0]).replace("\\","") + " " + str(int(psutil.disk_usage(str(disk_info[i][0]))[3])) + "\n")

                    #data.append(disk_info['c_per'])
                    #data.append(disk_info['d_per'])
                    #data.append(disk_info['e_per'])
                except Exception: print("Cant error disk")
            else:
                for i in range(3):
                    data.append("Access denied")

            # СДЕЛАТЬ ЧЕРЕЗ ЦИКЛ ЗАПИСЬ, А НЕ ЭТУ ЕБАЛУ

            count = 0
            #print(info)
            for i in range(len(info)):
                try:
                    #text += info[i]%(str(data[i])) # Не нужно,

                    if(info[i].find('{0}') > -1):
                        text += info[i].format(str(data[i]))
                        #print(text)
                    else:
                        text += info[i]
                except Exception as e:
                    print('Ошибка: ', e)
                    text += info[i]



            print(text)
            busy = False
            return text
        except Exception as e:
            print(e)
            busy = False
            return text


def main():
    print("Detected",len(token1),"users")
    #thread = threading.Thread(target=checkBusy)
    #thread.start()
    for i in range(len(token1)):
        print("thread", i, "adding...") #massAPI[i][0], massAPI[i][1], token1[i]
        thread = threading.Thread(target=threadVk2, args=(token1[i], "user"+str(i)))
        thread.start()
        thread = threading.Thread(target=loger, args=(token1[i], "user"+str(i)))
        thread.start()
        print("thread", i, "added")



main()



#--------------END--------------

#for i in range(len(massAPI)):
#    print("thread", i, "adding...") #massAPI[i][0], massAPI[i][1], token1[i]
#    thread = threading.Thread(target=threadVk, args=(massAPI[i][0], massAPI[i][1], token1[i], "user"+str(i)))
#    thread.start()
#    print("thread", i, "added")

