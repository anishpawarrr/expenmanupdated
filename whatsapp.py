# import datetime
# import firebase_admin
# import numpy
# from firebase_admin import credentials, db
# from twilio.rest import Client
#
# account_sid = 'ACe37218c83a39cb303ac1a46bff38a56f'
# auth_token = 'e07fde67e6ad3f172ac2ffaedc2ed0dc'
# client = Client(account_sid, auth_token)
#
# def send_today_reminders():
#     # nm = numpy.random.randint(1000)
#     # nm = str(nm)
#     cred = credentials.Certificate("service_account_key.json")
#     app = firebase_admin.initialize_app(cred)
#     root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
#     uref = root.child('Users')
#     # userref = uref.child(user)
#     userdata = uref.get()
#     userdata = dict(userdata)
#     print(userdata)
#     for i in userdata.keys():
#         # print(i)
#         try:
#             phno = str(userdata[i]['phno'])
#             # print(phno)
#         except:
#             # print(i)
#             continue
#         tasklist = userdata[i]['tasks']
#         # print(tasklist)
#         today_task_string = str(tasklist[datetime.datetime.today().day])
#         # print(today_task_string)
#         if today_task_string == '' or today_task_string == ',':
#             continue
#         today_list = today_task_string.split(',')
#         message_list = ''
#         for j in today_list:
#             message_list = message_list + j + '\n'
#         body = 'Hi, your tasks for today->\n' + message_list
#         message = client.messages.create(
#           from_='whatsapp:+14155238886',
#           body=body,
#           to='whatsapp:+91' + phno
#         )
#         print(message.sid + 'Message sent to ' + i)
#         return
#
# def send_tom_reminders():
#     # nm = numpy.random.randint(1000)
#     # nm = str(nm)
#     cred = credentials.Certificate("service_account_key.json")
#     app = firebase_admin.initialize_app(cred)
#     root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
#     uref = root.child('Users')
#     # userref = uref.child(user)
#     userdata = uref.get()
#     userdata = dict(userdata)
#     print(userdata)
#     for i in userdata.keys():
#         # print(i)
#         try:
#             phno = str(userdata[i]['phno'])
#             # print(phno)
#         except:
#             # print(i)
#             continue
#         tasklist = userdata[i]['tasks']
#         # print(tasklist)
#         today_task_string = str(tasklist[datetime.datetime.today().day + 1])
#         print(datetime.datetime.today().day + 1)
#         # print(today_task_string)
#         if today_task_string == '' or today_task_string == ',':
#             continue
#         today_list = today_task_string.split(',')
#         message_list = ''
#         for j in today_list:
#             message_list = message_list + j + '\n'
#         body = 'Hi, your tasks for tomorrow ->\n' + message_list
#         message = client.messages.create(
#             from_='whatsapp:+14155238886',
#             body=body,
#             to='whatsapp:+91' + phno
#         )
#         print(message.sid + 'Message sent to ' + i)
#         return
#
# send_today_reminders()
# send_tom_reminders()
# # http://wa.me/+14155238886?text=join%20breath-forth
# # https://taskwallet.streamlit.app/
