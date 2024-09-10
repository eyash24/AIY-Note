# imports
import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import random
from time import *
import smtplib

# display window
displaywindow = Tk()
displaywindow.title('AIY Notes')
displaywindow.geometry('500x500')
displaywindow.resizable(False, False)
displaywindow["bg"] = '#000000'

# Connectio to MYSQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)

# create a cursor and initializing sql terminal
my_c = mydb.cursor()

AIY_notes_database = False
while AIY_notes_database == False:
    my_c.execute("Show databases;")
    list_databases = list()
    for db in my_c:
        list_databases.append(db)
    print()
    databases = list()
    for i in list_databases:
        for e in i:
            databases.append(e)

    if "AIY_notes_database" in databases:
        print("AIY_notes_database exist")
        AIY_notes_database = True
        break
    else:
        my_c.execute("create database AIY_notes_database")

# After creation of AIY_notes_database we verifying and updating the accouts in the user_AIY_notes_database table
user_accounts = False
while user_accounts == False:
    my_c.execute("use AIY_notes_database")
    my_c.execute("show tables")
    list_tables = list()
    for t in my_c:
        list_tables.append(t)
    print()
    tables = list()
    for i in list_tables:
        for e in i:
            tables.append(e)

    if "User_accounts" in tables:
        print("user_accounts exist")
        user_accounts = True
    else:
        my_c.execute("use AIY_notes_database")
        my_c.execute(
            "create table User_accounts(S_no INT ,S_Name VarChar(100),DoB DATE,Password VarChar(100),Account_no VarChar (18),ph_no VarChar(20),email_id VarChar(100))")

    if user_accounts == True:
        if "note_A0001_table" in tables:
            print("note_A001_table exist")
        else:
            my_c.execute("use AIY_notes_database")
            my_c.execute(
                "create table note_A0001_table(S_no INT,Section_no INT,Section_name varchar(150),Note_no INt,Note_name Varchar(150),Date_creation Date,Location Varchar(1000)")
    else:
        my_c.execute("use AIY_notes_database")
        my_c.execute(
            "create table User_accounts(S_no INT ,S_Name VarChar(100),DoB DATE,Password VarChar(100),Account_no VarChar (18),ph_no VarChar(20),email_id VarChar(100))")
        my_c.execute(
            "create table note_A0001_table(S_no INT,Section_no INT,Section_name varchar(150),Note_no INt,Note_name Varchar(150),Date_creation Date,Location Varchar(1000)")

# functions
def donothing():  # fucntion for trial work
    filewin = Toplevel(displaywindow)
    button = Button(filewin, text="Do nothing button")
    button.place(x=50, y=50)

def widgets_destroy(widget_list):
    for i in widget_list:
        i.destroy()

def activation_procedure(window, list_entry,otp=None):
    global proceed
    if len(list_entry) > 0:
        for i in list_entry:
            if i == "":
                proceed_otp = False
                messagebox.showerror("AIY notes", "Please fill the form completely")
                break
            else:
                proceed_otp = True
    else:
        proceed_otp = False

    if otp is not None and window != "loginwindow":
        if proceed_otp == True:
            if pincode == otp:
                proceed_sql = True
            else:
                messagebox.showerror("AIY notes", "OTP is not equal to assigned OTP, please try again.")
        else:
            proceed_sql = False
    elif otp is not None and window == "loginwindow":
        proceed_sql = True
    else:
        proceed_sql = False
        messagebox.showerror("AIY notes", "Please re-fill the form completely")

    if proceed_sql == True:
        if window == "loginwindow":
            if len(list_entry) == 2:
                username = list_entry[0]
                password_account = list_entry[1]
                # SQL part

        elif window == "account_creation_window":
            if len(list_entry) == 7:
                print()
                # sql part

        elif window == "forget_account":
            if len(list_entry) == 6:
                print()
                # sql part
        else:
            messagebox.showerror("AIY notes", "Please fill in the form and retry")
    else:
        pass

# email typed or not verification for otp system and beyond
def verification_email_entry(window, username, email_id, purpose, button_destroy=None):
    if window == "forget_account" or window == "account_creation_window":
        if email_id != "" and username != "":
            OTP_system(username, email_id, purpose)
            if button_destroy is not None:
                button_destroy.destroy()
            else:
                pass
                # it means that no button is getting destroyed
        elif email_id != "" or username != "":
            messagebox.showerror("AIY notes", "Please fill in the email id part and username and retry")
        else:
            messagebox.showerror("AIY notes", "Please fill in the email id part and username and retry")
    else:
        messagebox.showerror("AIY notes", "Error")


def OTP_system(username_receiver, email_id, otp_purpose):
    Username = username_receiver
    email_reciever = email_id
    sender_email = ''
    password = ""

    # pin_code segment
    global pincode
    pincode = str(random.randint(1000, 9999))

    print("starting to send email")
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()

        smtp.login(sender_email, password)
        subject = 'AIY Notes'

        # message and custom subject segment
        if otp_purpose == 'account_activation_otp':
            subject = 'AIY Notes Account Activation'
            body = 'Dear ' + Username + ',' \
                                        '\n The account activation process has begun. For the complete creation of the account, we require you to enter the below displayed pin code into the program,' \
                                        "\n " + pincode + \
                   '\n Thank you for your time and consideration.' \
                   '\n Thank you,' \
                   '\n AIY Notes'
        elif otp_purpose == 'forget_account':
            subject = 'AIY Notes Forget Account'
            body = 'Dear ' + Username + ',' \
                                        '\n The account recovery has been begun. For the complete authenticity we require you to enter the below display pin code into the program,' \
                                        "\n " + pincode + \
                   '\n Thank you for your time and consideration.' \
                   '\n Thank you,' \
                   '\n AIY Notes'
        elif otp_purpose == "retry_otp":
            subject = 'AIY Notes New Pin Code'
            body = 'Dear ' + Username + ',' \
                                        '\n The new pin code given below, please try to re-entry the new code.' \
                                        "\n " + pincode + \
                   '\n Thank you for your time and consideration.' \
                   '\n Thank you,' \
                   '\n AIY Notes'

        msg = f'subject:{subject}\n\n{body}'
        smtp.sendmail(sender_email, email_reciever, msg)
        smtp.quit()
    print("email sent")


def Login_window(back_from_window=None, list_window_widget=None):
    # for future back program buttons on other windows
    if back_from_window is not None:
        if back_from_window == "forget_account" or back_from_window == "account_creation_window":
            if list_window_widget is not None:
                for i in list:
                    i.destroy()
            else:
                pass
        else:
            pass
    else:
        pass

    displaywindow["bg"] = '#bfbfbf'
    proceed = False
    # Welcome label
    wel = Label(displaywindow, text="Welcome To AIY Notes", font="zapfino 16 bold")
    signin = Label(displaywindow, text="Sign in", font="calbri 16")
    wel.place(relx=0.2)
    signin.place(relx=0.3, rely=0.2)

    # login and entry
    loginid = Label(displaywindow, text="Login id:")
    loginid.place(relx=0.1, rely=0.3)
    loginpassword = Label(displaywindow, text="password")
    loginpassword.place(relx=0.1, rely=0.4)
    # entry widgets
    global id_lw_2, password_lw_2
    id_lw_2 = Entry(displaywindow)
    password_lw_2 = Entry(displaywindow, show="*")

    id_lw_2.place(relx=0.3, rely=0.3)
    password_lw_2.place(relx=0.3, rely=0.4)

    global loginwindow_list_widgets
    # Buttons
    list_entry_displaywindow = (id_lw_2.get(), password_lw_2.get())
    Next = Button(displaywindow, text="Next", command=lambda: [widgets_destroy(loginwindow_list_widgets),
                                                               activation_procedure('loginwindow',
                                                                                    list_entry_displaywindow)])
    Forgotpassword = Button(displaywindow, text="Forgot password",
                            command=lambda: [widgets_destroy(loginwindow_list_widgets), Forget_password()])
    Createaccount = Button(displaywindow, text="Create account",
                           command=lambda: [widgets_destroy(loginwindow_list_widgets), account_creation()])

    Next.place(relx=0.7, rely=0.6)
    Forgotpassword.place(relx=0.1, rely=0.6)
    Createaccount.place(relx=0.4, rely=0.6)
    loginwindow_list_widgets = (
        wel, signin, loginid, loginpassword, id_lw_2, password_lw_2, Next, Forgotpassword, Createaccount)

def account_creation():  # create accounts display window
    displaywindow["bg"] = '#bfbfbf'

    # destroy login window's widgets
    widgets_destroy(loginwindow_list_widgets)

    # label for creation of new accounts
    Account_creation = Label(displaywindow, text="Account Creation", font="zapfino 16 bold")
    user_name = Label(displaywindow, text="Username:")
    DOB = Label(displaywindow, text="Date of Birth:")
    password = Label(displaywindow, text="Password:")
    confirm_password = Label(displaywindow, text="Confirm password:")
    email_id = Label(displaywindow, text="Email id:")
    ph_no = Label(displaywindow, text="Phone.no:")

    # Entry widgets for creation of new accounts
    global user_name_entry_ac, DOB_ac, password_ac, confirm_password_ac, email_id_ac, ph_no_ac
    user_name_entry_ac = Entry(displaywindow)
    DOB_ac = Entry(displaywindow)
    password_ac = Entry(displaywindow)
    confirm_password_ac = Entry(displaywindow)
    email_id_ac = Entry(displaywindow)
    ph_no_ac = Entry(displaywindow)

    # placement of label and entry widget
    # Label placement
    Account_creation.place(relx=0.3)
    user_name.place(relx=0.1, rely=0.2)
    DOB.place(relx=0.1, rely=0.3)
    password.place(relx=0.1, rely=0.4)
    confirm_password.place(relx=0.1, rely=0.5)
    email_id.place(relx=0.1, rely=0.6)
    ph_no.place(relx=0.1, rely=0.7)

    # Entry widget placement
    user_name_entry_ac.place(relx=0.4, rely=0.2)
    DOB_ac.place(relx=0.4, rely=0.3)
    password_ac.place(relx=0.4, rely=0.4)
    confirm_password_ac.place(relx=0.4, rely=0.5)
    email_id_ac.place(relx=0.4, rely=0.6)
    ph_no_ac.place(relx=0.4, rely=0.7)

    # OTP system activation
    otp_create = Label(displaywindow, text="OTP Pin:", font="Calbri 14")
    otp_create_ = Entry(displaywindow)

    # OTP placement
    otp_create.place(relx=0.1, rely=0.8)
    otp_create_.place(relx=0.4, rely=0.8)

    # buttons for account_creation_window
    send_otp_create = Button(displaywindow, text="Send otp", command=lambda: [otp_create_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "account_creation_window",
                                                                                  user_name_entry_ac.get(),
                                                                                  email_id_ac.get(),
                                                                                  'account_activation_otp',
                                                                                  send_otp_create)])

    list_entry_account_creation_window = (
        user_name_entry_ac.get(), DOB_ac.get(), password_ac.get(), confirm_password_ac.get(), email_id_ac.get(), ph_no_ac.get(),
        otp_create_.get())
    Next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('account_creation_window',
                                                                                     list_entry_account_creation_window,otp_create_.get())])
    Resend_pincode_create = Button(displaywindow, text="Resend otp",
                                   command=lambda: [otp_create_.delete(0, END),
                                                    verification_email_entry("account_creation_window",
                                                                             user_name_entry_ac.get(), email_id_ac.get(),
                                                                             'retry_otp')])
    list_widgets_account_creation = (
    Account_creation, user_name, DOB, password, confirm_password, email_id, ph_no, user_name_entry_ac, DOB_ac,
    password_ac, confirm_password_ac, email_id_ac, ph_no_ac, otp_create, otp_create_, send_otp_create, Next_,
    Resend_pincode_create)

    back_login = Button(displaywindow, text="Back",
                        command=lambda: [back_login.destroy(), widgets_destroy(list_widgets_account_creation),
                                         Login_window("account_creation_window")])

    # buttons placements
    send_otp_create.place(relx=0.25, rely=0.9)
    Next_.place(relx=0.7, rely=0.9)
    Resend_pincode_create.place(relx=0.45, rely=0.9)
    back_login.place(relx=0.1, rely=0.9)

def Forget_password():
    displaywindow["bg"] = '#bfbfbf'

    # destroy login window's widgets
    widgets_destroy(loginwindow_list_widgets)

    # Label and entry widgets for the forget_account
    # Label widgets
    Forget_label = Label(displaywindow, text="Forget_account", font="zapfino 16 bold")
    Username_forget = Label(displaywindow, text="Username:")
    Last_password_forget = Label(displaywindow, text="Password used: ")
    DoB_forget = Label(displaywindow, text="Date of birth:")
    ph_no_forget = Label(displaywindow, text="Phone.no:")
    email_forget = Label(displaywindow, text="Email id:")

    # Entry widgets
    global username_forget_fw, last_password_forget_fw, DoB_forget_fw, Ph_no_forget_fw, email_forget_fw
    username_forget_fw = Entry(displaywindow)
    last_password_forget_fw = Entry(displaywindow)
    DoB_forget_fw = Entry(displaywindow)
    Ph_no_forget_fw = Entry(displaywindow)
    email_forget_fw = Entry(displaywindow)

    # OTP system recover
    otp_forget = Label(displaywindow, text="OTP Pin:")
    otp_forget_ = Entry(displaywindow)

    # Placement of label and entry widgets
    # Label segment of forget_account
    Forget_label.place(relx=0.3)
    Username_forget.place(relx=0.1, rely=0.2)
    Last_password_forget.place(relx=0.1, rely=0.3)
    DoB_forget.place(relx=0.1, rely=0.4)
    ph_no_forget.place(relx=0.1, rely=0.5)
    email_forget.place(relx=0.1, rely=0.6)

    # Entry segment of forget_account
    username_forget_fw.place(relx=0.4, rely=0.2)
    last_password_forget_fw.place(relx=0.4, rely=0.3)
    DoB_forget_fw.place(relx=0.4, rely=0.4)
    Ph_no_forget_fw.place(relx=0.4, rely=0.5)
    email_forget_fw.place(relx=0.4, rely=0.6)

    # OTP segment of forget_account
    otp_forget.place(relx=0.1, rely=0.7)
    otp_forget_.place(relx=0.4, rely=0.7)

    # Button widgets for forget account
    send_otp_forget = Button(displaywindow, text="Send otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_fw.get(),
                                                                                  email_forget_fw.get(),
                                                                                  'forget_account', send_otp_forget)])

    # otp verification
    list_entry_forget_account = (
        username_forget_fw.get(), last_password_forget_fw.get(), DoB_forget_fw.get(), Ph_no_forget_fw.get(),
        email_forget_fw.get(), otp_forget_.get())

    next_fw = Button(displaywindow, text="Next", command=lambda: [activation_procedure('forget_account',
                                                                                     list_entry_forget_account,otp_forget_.get())])
    retry_pincode = Button(displaywindow, text="Resend otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_fw.get(),
                                                                                  email_forget_fw.get(),
                                                                                  'retry_otp')])

    list_widgets_forget_account = (
        Forget_label, Username_forget, Last_password_forget, DoB_forget, ph_no_forget, email_forget,
        username_forget_fw, last_password_forget_fw, DoB_forget_fw, Ph_no_forget_fw, email_forget_fw, otp_forget,
        otp_forget_, next_fw, retry_pincode, send_otp_forget)

    back_login = Button(displaywindow, text="Back",
                        command=lambda: [back_login.destroy(), widgets_destroy(list_widgets_forget_account),
                                         Login_window("forget_account")])

    # Buttons placements of forget account
    next_fw.place(relx=0.7, rely=0.8)
    send_otp_forget.place(relx=0.25, rely=0.8)
    retry_pincode.place(relx=0.45, rely=0.8)
    back_login.place(relx=0.1, rely=0.8)

def Login_window_1():
    displaywindow["bg"] = '#bfbfbf'
    proceed = False
    # Welcome label
    wel = Label(displaywindow, text="Welcome To AIY Notes", font="zapfino 16 bold")
    signin = Label(displaywindow, text="Sign in", font="calbri 16")
    wel.place(relx=0.2)
    signin.place(relx=0.3, rely=0.2)

    # login and entry
    loginid = Label(displaywindow, text="Login id:")
    loginid.place(relx=0.1, rely=0.3)
    loginpassword = Label(displaywindow, text="password")
    loginpassword.place(relx=0.1, rely=0.4)
    # entry widgets
    global id_lw, password_lw
    id_lw = Entry(displaywindow)
    password_lw = Entry(displaywindow, show="*")

    id_lw.place(relx=0.3, rely=0.3)
    password_lw.place(relx=0.3, rely=0.4)

    # Buttons
    list_entry_displaywindow = (id_lw.get(), password_lw.get())
    next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('loginwindow',
                                                                                    list_entry_displaywindow)])
    forgotpassword = Button(displaywindow, text="Forgot password",
                            command=lambda: [widgets_destroy(loginwindow_list_widgets), Forget_password()])
    createaccount = Button(displaywindow, text="Create account",
                           command=lambda: [widgets_destroy(loginwindow_list_widgets), account_creation()])

    next_.place(relx=0.7, rely=0.6)
    forgotpassword.place(relx=0.1, rely=0.6)
    createaccount.place(relx=0.4, rely=0.6)
    loginwindow_list_widgets = (
        wel, signin, loginid, loginpassword, id_lw, password_lw, next_, forgotpassword, createaccount)


# image
# Read the Image
logo_location = "AIY logo.png"
image = Image.open(logo_location)
# Re-szie the image using resize() method
resize_image = image.resize((600, 600))
img = ImageTk.PhotoImage(resize_image)

logo_button = Button(displaywindow, image=img, command=lambda: [logo_button.destroy(), Login_window_1()])
logo_button.pack()
displaywindow.mainloop()
my_c.close()