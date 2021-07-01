import datetime
from os import abort
from threading import Thread

from models import Message
import array
from flask import Flask, jsonify, request, send_from_directory, redirect
from flask.json.tag import JSONTag
from flask.templating import render_template

last_message_recived = {}
curren_num_message = -1
last_message_recived_for_person = {}
curren_num_message_for_person = {}
messages_for_person = {}
id_users = []
messages = ["message 1", "message 2"]


def add_message_to_broadcast(message):
    messages[curren_num_message] = message


class MyThread(Thread):
    """
    A threading example
    """

    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)

        self.name = name

    def run(self, ):
        """Запуск потока"""
        global curren_num_message
        while True:
            s = input()
            if s.split(" ")[0] == "broadcast":
                messages.append(s.split(" ")[1])
                curren_num_message += 1
                print("broadcast : " + s.split(" ")[1], curren_num_message)
            if s.split(" ")[0] == "person":
                print("to  person{" + s.split(" ")[1] + "} :" + s.split(" ")[2])
                messages_for_person[int(s.split(" ")[1])] = s.split(" ")[2]
                curren_num_message_for_person[int(s.split(" ")[1])] += 1


# broadcast wdgfwd
# person 453101710 ghbnjmk
app = Flask(__name__)
msgsIdCounter = 0

# msgLambda = lambda msg: {'id': msg.id, 'text': msg.text, 'date': msg.date()}

arch = list()
msgs = list([Message(msgsIdCounter, 'Init'),
             Message(msgsIdCounter + 1,
                     'Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti aut dolore asperiores consequuntur suscipit officia similique magni, corrupti, ab eaque incidunt consequatur vero fugit. Quidem aliquid unde porro ducimus cupiditate',
                     )])


@app.route('/')
def index():
    return render_template('index.html', msgs=msgs, arch=arch)


@app.route('/getMessage', methods=['POST'])
def msg_post():
    num_message = request.json.get('num_message')
    print(num_message)
    return {'last': messages[num_message]}


@app.route('/newMessage', methods=['POST'])
def msg_post_():
    num_last_message = request.json.get('num_last_message')
    #    if int(num_last_message) < curren_num_message:
    print(curren_num_message)
    return {'last': curren_num_message}


@app.route('/newm')
def broadcast_message():
    return render_template('messagesALL.html')



def print_person_info(user_id):
    print("person id ", user_id)
    print("{")
    print('last_message_recived_for_person ', last_message_recived_for_person[user_id])
    print('curren_num_message_for_person ', curren_num_message_for_person[user_id])
    print('messages_for_person ', messages_for_person[user_id])
    print("}")


@app.route('/newMessageForPersons', methods=['POST'])
def msg_post_for_person():
    ans = []
    for i in range(len(curren_num_message_for_person)):
        print_person_info(id_users[i])
        print(" - ", id_users[i])
        if curren_num_message_for_person[id_users[i]] > last_message_recived_for_person[id_users[i]]:
            ans.append([id_users[i], curren_num_message_for_person[id_users[i]]])
    print("ans ", ans)
    return {'ans': ans}


@app.route('/addPerson', methods=['POST'])
def msg_post_add_person():
    person_id = request.json.get('person_id')
    # num_message = request.json.get('num_message')
    if person_id not in last_message_recived_for_person:
        last_message_recived_for_person[person_id] = 0
        curren_num_message_for_person[person_id] = 0
        messages_for_person[person_id] = []
        id_users.append(int(person_id))
        print_person_info(person_id)
    return {'last': curren_num_message}


@app.route("/get-pdf")
def get_pdf():
#    file_id = request.json.get('file_id')
    filename = 'https://new.mospolytech.ru/upload/files/mfc-blank/На%20выход%20из%20академического%20отпуска.pdf'
    try:
        return send_from_directory(path=filename, filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# New messages handling with form
@app.route("/newBroadcast", methods=['POST'])
def msg_broadcast():
    msgText = request.form.get('msg')
    # msgReciever=msgReciever+1
    newMsg = Message(msgsIdCounter, msgText)
    msgs.append(newMsg)
    return redirect('/')

@app.route("/newDirect", methods=['POST'])
def msg_direct():
    msgText = request.form.get('msg')
    msgReciever = request.form.get('user_id')
    # msgsIdCounter=msgsIdCounter+1
    newMsg = Message(msgsIdCounter, msgText, reciever=msgReciever)
    msgs.append(newMsg)
    return redirect('/')
# 

@app.route('/getMessagePerson', methods=['POST'])
def get_message_person():
    person_id = request.json.get('person_id')
    num_message_from = request.json.get('num_message_from')
    num_message_to = request.json.get('num_message_to')

    messages = messages_for_person[person_id][num_message_from::]
    print("                                               (", messages, ")", num_message_from, ")", messages_for_person)
    return {'last': messages}


#   return None
# msgText = request.form.get("msg")
# newMsg = Message(msgsIdCounter,msgText, datetime.datetime.now())
# msgsIdCounter=msgsIdCounter+1
# msgs.append(newMsg)


# Получение новых сообщений
@app.route('/gm')
def msg_get():
    resDict = {}
    for i in range(len(msgs)):
        resDict[i] = msgs[i].__repr__()
    arch.extend(msgs)
    msgs.clear()
    return resDict


# Проверка есть ли новые сообщения
# status 1 Есть новые сообщения, 0 - нет
@app.route('/check')
def msg_check():
    return {'status': 1} if len(msgs) > 0 else {'status': 0}


if __name__ == "__main__":
    curren_num_message = 1
    t = MyThread("newThread1")
    t.start()
    app.run()
