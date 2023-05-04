import datetime
import streamlit as st
import streamlit_option_menu as om
import bend

st.set_page_config(page_title="TW", layout='centered', initial_sidebar_state="expanded")


if 'user' not in st.session_state:
    st.session_state['user'] = 'x'
if 'opt' not in st.session_state:
    st.session_state['opt'] = 'Home'
if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'userinfo' not in st.session_state:
    st.session_state['userinfo'] = {}
with st.sidebar as sb0:
    if not st.session_state['login']:
        with st.form("login_form"):
            # st.header("Login")
            user_name = st.text_input("User MailId")
            password = st.text_input("Password", type='password')
            form_submit_button = st.form_submit_button(label="LogIn")
            if form_submit_button:
                st.session_state['login'], st.session_state['user'] = bend.sign_in(user_name,password)
            if st.session_state['user'] == '':
                st.error("Wrong credentials")

    opt = om.option_menu(menu_title='TASK WALLET',
                         options=['Home','Calendar', 'Record Expense', 'Expense History', 'Update Tasks', 'Sign up', 'Settings'],
                         default_index=0, menu_icon='bi bi-layers-fill',
                         icons=['bi bi-door-open', 'bi bi-calendar-check', 'bi bi-cash', 'bi bi-clock-history', 'bi bi-card-checklist', 'bi bi-person-plus', 'bi bi-gear'])
    st.session_state['opt'] = opt

if st.session_state['opt'] == 'Home'  and st.session_state['login']:
    st.session_state['userinfo'] = bend.get_user_data(st.session_state['user'])

    if 'home_select' not in st.session_state:
        st.session_state['home_select'] = ''
    st.session_state['home_select'] = om.option_menu(menu_title='', options=['Expenses', 'Tasks'], orientation='horizontal', icons=['bi bi-currency-dollar', 'bi bi-list-task'])
    if st.session_state['home_select'] == 'Expenses':
        st.subheader("Amount spent : " + str(st.session_state['userinfo']['total']))
        st.subheader("Remaining : " + str(st.session_state['userinfo']['pocket_money'] - st.session_state['userinfo']['total']))
        if st.session_state['userinfo']['target_saving'] > (st.session_state['userinfo']['pocket_money'] - st.session_state['userinfo']['total']):
            st.error('You are using money from savings quota')
        st.subheader("This month's overview")
        expense_df = bend.time_line(st.session_state['userinfo'])
        st.line_chart(expense_df, x = 'Date', y = 'Amount')
        pie_fig = bend.show_expenses_piechart(st.session_state['userinfo'])
        st.plotly_chart(pie_fig)
    elif st.session_state['home_select'] == 'Tasks':
        task_list = bend.task_list(datetime.datetime.today().day, st.session_state['userinfo'])
        st.subheader("Today's tasks :")
        c = 1
        if task_list[0] == '':
            st.write("No tasks scheduled")
        else:
            for i in task_list:
                st.write(f'{c}. {i}')
                c += 1
    # st.write(st.session_state['user'])
    # st.write(st.session_state['userinfo'])

elif st.session_state['opt'] == 'Calendar' and st.session_state['login']:
    enddate = 32
    if datetime.datetime.today().month % 2 == 0:
        enddate = 31

    datelist = [i for i in range(1,enddate)]
    month = datetime.datetime.today().month
    for i in range(1, enddate, 1):
        task_list = bend.task_list(i, st.session_state['userinfo'])
        # st.subheader(f'Tasks for {i}/{month}:')
        c = 1
        if task_list[0] == '':
            continue
            # st.write('No tasks scheduled')
            # continue
        st.subheader(f'Tasks for {i}/{month}:')
        for j in task_list:
            st.write(f'{c}. {j}')
            c += 1

elif st.session_state['opt'] == 'Record Expense' and st.session_state['login']:
    with st.form("Record"):
        st.subheader("Expense details")
        reason = st.text_input("Reason")
        day = st.date_input("Date").day
        amt = st.number_input("Amount")
        fsb = st.form_submit_button("Enter record")
    if fsb:
        st.session_state['userinfo'] = bend.record_exp(reason, day, amt, st.session_state['user'], st.session_state['userinfo'])
        st.success("Entry recorded")
elif st.session_state['opt'] == 'Expense History' and st.session_state['login']:
    df = bend.history_df(st.session_state['userinfo'])
    st.table(df)

    @st.experimental_memo
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        f"Download {datetime.datetime.today().month}/23 expenses",
        csv,
        "expenses.csv",
        "text/csv",
    )

elif st.session_state['opt'] == 'Update Tasks' and st.session_state['login']:
    if 'uopt' not in st.session_state:
        st.session_state['uopt'] = ''
    st.session_state['uopt'] = om.option_menu(menu_title="", options=['Create', 'Delete'], icons=['bi bi-folder-plus','bi bi-folder-minus'] ,orientation='horizontal')
    if st.session_state['uopt'] == 'Create':
        with st.form('Create_Task'):
            date = st.date_input("Task date")
            task = st.text_input("Task")
            day = date.day
            cr_tsk = st.form_submit_button("Schedule task")
        if cr_tsk:
            # st.session_state['userinfo'] = bend.get_user_data(st.session_state['user'])
            st.session_state['userinfo'] = bend.create_task(day, task, st.session_state['userinfo'], st.session_state['user'])
            # st.session_state['userinfo'] = bend.get_user_data(st.session_state['user'])
            st.info("Task created successfully")
    elif st.session_state['uopt'] == 'Delete':
        day = st.date_input("Date").day
        with st.form('Delete_Task'):
            st.subheader('Select tasks to delete')
            task_list = bend.task_list(day, st.session_state['userinfo'])
            check_list = [False for i in range(len(task_list))]
            for i in range(len(task_list)):
                check_list[i] = st.checkbox(f'{task_list[i]}', key=i)
            del_task = st.form_submit_button('Delete')
        if del_task:
            # st.session_state['userinfo'] = bend.get_user_data(st.session_state['user'])
            st.session_state['userinfo'] = bend.del_task(check_list, st.session_state['user'], task_list, st.session_state['userinfo'], day)
            # st.session_state['userinfo'] = bend.get_user_data(st.session_state['user'])
            st.info("Tasks deleted successfully")

elif st.session_state['opt'] == 'Sign up':
    try:
        with st.form('sign_up'):
            mail_id = st.text_input("User Mailid")
            password = st.text_input("Password", type='password')
            pocket_money = st.number_input("Your pocket money")
            target_saving = st.number_input("Target saving")
            sign_up_button = st.form_submit_button("Sign Up")
        if sign_up_button:
            try:
                bend.sign_up(mail_id,password)
                bend.create_user_info(mail_id.replace('.','!'),pocket_money,target_saving)
                st.balloons()
                st.write("Account created successfully")
            except:
                st.error("User already exists!")
    except:
        st.subheader("Refresh the app and sign up again")
elif st.session_state['opt'] == 'Settings' and st.session_state['login']:
    with st.form("reminder"):
        st.subheader("Enable WhatsApp reminding service")
        phno = int(st.number_input("Enter your number"))
        # st.write("To get whatsapp reminders click the link and send prebuilt message")
        # st.write("http://wa.me/+14155238886?text=join%20breath-forth", unsafe_allow_html=True)
        # b = st.button("Send messages to this number")
        fsb = st.form_submit_button("Get notified through WhatsApp")
        if fsb and len(str(phno)) == 10:
            st.session_state['userinfo'] = bend.upload_phno(st.session_state['user'], st.session_state['userinfo'], phno)
            st.write("To get whatsapp reminders click the link and send prebuilt message")
            st.write("If message doesn't get formed automatically, text 'join breath-forth'")
            st.write("http://wa.me/+14155238886?text=join%20breath-forth", unsafe_allow_html=True)
        elif fsb:
            st.write("You entered something wrong")
    with st.form("update"):
        st.subheader("Update info")
        pocket_money = st.number_input("New pocket money")
        target_saving = st.number_input("Target saving")
        setting_button = st.form_submit_button("Update changes")
    if setting_button:
        st.session_state['userinfo'] = bend.update_settings(pocket_money, target_saving, st.session_state['user'])
        st.info("Settings applied")
    # clear_history = st.button("Clear history")
    with st.form('Clear'):
        st.subheader("Clear data")
        clear_history = st.form_submit_button("Clear history")
    if clear_history:
        pm = st.session_state['userinfo']['pocket_money']
        ts = st.session_state['userinfo']['target_saving']
        user = st.session_state['user']
        bend.create_user_info(user, pm, ts)
        st.success("History deleted successfully")

if not(st.session_state['login'] or st.session_state['opt'] == 'Sign up'):
    st.header("Login to your account first")