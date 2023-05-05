import numpy.random
import pyrebase as pb
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore
from pandas import json_normalize
import pandas as pd
import config
import datetime
import streamlit as st
import smtplib
from email.message import EmailMessage


def sign_up(mail_id, password):
    fb = pb.initialize_app(config.firebaseConfig)
    auth = fb.auth()
    auth.create_user_with_email_and_password(mail_id,password)
    signupmail(mail_id)
    del fb
    del auth

    # initialise.giveauth().create_user_with_email_and_password(mail_id,password)

def sign_in(mail_id,password):
    fb = pb.initialize_app(config.firebaseConfig)
    auth = fb.auth()
    try:
        auth.sign_in_with_email_and_password(mail_id, password)
        return True, mail_id.replace('.', '!')
    except:
        return False, ''


def create_user_info(mail_id, pocket_money, target_saving):
    calendar_dict = calendar()
    calendar_dict["pocket_money"] = pocket_money
    calendar_dict['target_saving'] = target_saving
    calendar_dict['Reason'] = ""
    calendar_dict['Amount'] = ""
    calendar_dict['Date'] = ""
    calendar_dict['total'] = 0
    calendar_dict['Travel'] = 0
    calendar_dict['Food'] = 0
    calendar_dict['Entertainment'] = 0
    calendar_dict['Education'] = 0
    calendar_dict['Health'] = 0
    calendar_dict['Personal care'] = 0
    calendar_dict['Debt'] = 0

    udata = {mail_id : calendar_dict}
    # cred = credentials.Certificate("service_account_key.json")
    root = db.reference(url = "https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    uref.update(udata)

# @st.cache(allow_output_mutation= True)
def get_user_data(user):
    try:
        # nm = numpy.random.randint(1000)
        # nm = str(nm)
        cred = credentials.Certificate("service_account_key.json")
        app = firebase_admin.initialize_app(cred)
        root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
        uref = root.child('Users')
        userref = uref.child(user)
        userdata = userref.get()
        return userdata
    except:
        nm = numpy.random.randint(1000)
        nm = str(nm)
        cred = credentials.Certificate("service_account_key.json")
        app = firebase_admin.initialize_app(cred, name=nm)
        root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
        uref = root.child('Users')
        userref = uref.child(user)
        userdata = userref.get()
        return userdata
        # return get_user_data(user)

def update_settings(pocket_money, target_saving, user):
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    userref = uref.child(user)
    userdata = userref.get()
    userdata['pocket_money'] = pocket_money
    userdata['target_saving'] = target_saving
    userref.update(userdata)
    return userdata

def calendar():
    dicti = {"expenses": expense_dict(), "tasks": task_dict()}
    return dicti

def expense_dict():
    ed = {'1':0}
    for i in range(2,32):
        ed[f'{i}'] = 0
    return ed

def task_dict():
    td = {'1':""}
    for i in range(2,32):
        td[f'{i}'] = ""
    return td

def create_task(day, task, userdata,user):
    task+=','
    userdata['tasks'][day] += task
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    userref = uref.child(user)
    userref.update(userdata)
    return userdata

def del_task(bool_list, user, task_list, userdata, day):
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    userref = uref.child(user)
    tasks = ''
    for i in range(len(bool_list)):
        if not bool_list[i]:
            tasks += f'{task_list[i]},'
    userdata['tasks'][day] = tasks
    userref.update(userdata)
    return userdata

def task_list(day, userdata):
    task_string = userdata['tasks'][day]
    task_string = str(task_string)
    task_string = task_string[:-1]
    task_list = task_string.split(',')
    return task_list

def show_expenses_piechart(userdata):
    pie_dict = {"Spent": int(userdata['total']), 'Remaining': int((userdata['pocket_money'] - userdata['total']))}
    fig = go.Figure(data=[go.Pie(labels=list(pie_dict.keys()), values=list(pie_dict.values()))])
    return fig

def show_expense_type_piechart(userdata):
    pie_dict = {"Travel": int(userdata['Travel']),
                "Food": int(userdata['Food']),
                "Entertainment": int(userdata['Entertainment']),
                "Education": int(userdata['Education']),
                "Health": int(userdata['Health']),
                "Personal care": int(userdata['Personal care']),
                "Debt": int(userdata['Debt'])}
    fig = go.Figure(data=[go.Pie(labels=list(pie_dict.keys()), values=list(pie_dict.values()))])
    return fig

def time_line(userdata):
    expen = userdata['expenses']
    dates = [i for i in range(32)]
    dataframe = pd.DataFrame(list(zip(dates,expen)), columns=['Date', 'Amount'])
    return dataframe

def record_exp(exptype, reason, day, amount, user, userdata):
    userdata['expenses'][day] += amount
    userdata['Amount'] += (str(amount) + ",")
    userdata['Reason'] += (reason + ",")
    userdata['Date'] += (str(day) + ',')
    userdata['total'] += amount
    userdata[exptype] += amount
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    userref = uref.child(user)
    userref.update(userdata)
    return userdata

def history_df(userdata):
    reasonstr = str(userdata['Reason'])
    amountstr = str(userdata['Amount'])
    datestr = str(userdata['Date'])
    reasonstr = reasonstr[:-1]
    amountstr = amountstr[:-1]
    datestr = datestr[:-1]
    reasonlist = reasonstr.split(',')
    amountlist = amountstr.split(',')
    datelist = datestr.split(',')
    m = str(datetime.datetime.today().month)
    m = "/"+m
    for i in range(len(datelist)):
        datelist[i] += m
    dicti = {'Date': datelist, 'Reason': reasonlist, 'Amount': amountlist}
    df = pd.DataFrame.from_dict(dicti)
    return df

def new_month():
    cred = credentials.Certificate("service_account_key.json")
    app = firebase_admin.initialize_app(cred)
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    dicti = dict(uref.get())
    for i in dicti.keys():
        pm = dicti[i]['pocket_money']
        ts = dicti[i]['target_saving']
        create_user_info(i, pm, ts)


def upload_phno(user, userdata, phno):
    userdata['phno'] = phno
    root = db.reference(url="https://expensemanager-f165e-default-rtdb.asia-southeast1.firebasedatabase.app/")
    uref = root.child('Users')
    userref = uref.child(user)
    userref.update(userdata)
    return userdata

def sendmail(to, msgbody, subject):
    msg = EmailMessage()
    body = msgbody
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = "vaxer.solutions@gmail.com"
    pw = 'rnjnuaxczxnagewj'
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user="vaxer.solutions@gmail.com", password=pw)
    server.send_message(msg)
    server.quit()

def signupmail(user : str):
    # user = user.replace('!', '.')
    body = "Hello! welcome to TASKWALLET the ultimate task and expense tracker\nvisit https://task-wallet.streamlit.app to use the app"
    sub = "Welcome to TASKWALLET!"
    sendmail(user, body, sub)

def split_mail(mail_list : list, amount_list : list, user):
    length = len(mail_list)
    if (len(amount_list) < length):
        length = len(amount_list)
    for i in range(length):
        body = f"Hi, you owe {amount_list[i]} rupees to {user}"
        sub = "Money reminder"
        sendmail(mail_list[i], body, sub)


# signupmail('anishpurupawar@gmail.com')