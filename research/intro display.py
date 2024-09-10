# First display
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
                "create table note_A0001_table(S_no INT,Section_no INT,Section_name varchar(150),Note_no INt,Note_name Varchar(150),Date_creation Date,Location Varchar(1000))")
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

def activation_procedure(window, list_entry):
    global proceed
    if len(list_entry) > 0:
        for i in list_entry:
            if i == "":
                proceed = False
                messagebox.showerror("AIY notes", "Please fill the form completely")
                break
            else:
                proceed = True
    else:
        proceed = False
    # present window closes if proceed = True and the respective next window opens up

# email typed or not verification for otp system and beyond
def verification_email_entry(window, username, email_id, purpose, button_destroy=None):
    if window == "forget_account" or window == "account_creation_window":
        if email_id != "" and username != "":
            OTP_system(username, email_id, purpose)
            if button_destroy != None:
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
                                        '\n The account activation process has begun. For the creation of the account, we require you to enter the below displayed pin code into the program,' \
                                        "\n " + pincode + \
                   '\n Thank you for your time and consideration.' \
                   '\n Thank you,' \
                   '\n AIY Notes'
        elif otp_purpose == 'forget_account':
            subject = 'AIY Notes Forget Account'
            body = 'Dear ' + Username + ',' \
                                        '\n The account recovery has been begun. For authenticity we require you to enter the below display pin code into the program,' \
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
    if back_from_window != None:
        if back_from_window == "forget_account" or back_from_window == "account_creation_window":
            if list_window_widget != None:
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
    id_ = Entry(displaywindow)
    password_ = Entry(displaywindow, show="*")

    id_.place(relx=0.3, rely=0.3)
    password_.place(relx=0.3, rely=0.4)

    # Buttons
    list_entry_displaywindow = (id_.get(), password_.get())
    Next = Button(displaywindow, text="Next", command=lambda: [widgets_destroy(loginwindow_list_widgets),
                                                               activation_procedure('displaywindow',
                                                                                    list_entry_displaywindow)])
    Forgotpassword = Button(displaywindow, text="Forgot password",
                            command=lambda: [widgets_destroy(loginwindow_list_widgets), Forget_password()])
    Createaccount = Button(displaywindow, text="Create account",
                           command=lambda: [widgets_destroy(loginwindow_list_widgets), account_creation()])

    Next.place(relx=0.7, rely=0.6)
    Forgotpassword.place(relx=0.1, rely=0.6)
    Createaccount.place(relx=0.4, rely=0.6)
    global loginwindow_list_widgets
    loginwindow_list_widgets = (
        wel, signin, loginid, loginpassword, id_, password_, Next, Forgotpassword, Createaccount)

    '''Login display Incomplete
    SQL part remaining'''

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
    user_name_entry = Entry(displaywindow)
    DOB_ = Entry(displaywindow)
    password_ = Entry(displaywindow)
    confirm_password_ = Entry(displaywindow)
    email_id_ = Entry(displaywindow)
    ph_no_ = Entry(displaywindow)

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
    user_name_entry.place(relx=0.4, rely=0.2)
    DOB_.place(relx=0.4, rely=0.3)
    password_.place(relx=0.4, rely=0.4)
    confirm_password_.place(relx=0.4, rely=0.5)
    email_id_.place(relx=0.4, rely=0.6)
    ph_no_.place(relx=0.4, rely=0.7)

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
                                                                                  user_name_entry.get(),
                                                                                  email_id_.get(),
                                                                                  'account_activation_otp',
                                                                                  send_otp_create)])
    list_entry_account_creation_window = (
        user_name_entry.get, DOB_.get(), password_.get(), confirm_password_.get(), email_id_.get(), ph_no_.get(),
        otp_create_.get())
    Next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('account_creation_window',
                                                                                     list_entry_account_creation_window)])
    Resend_pincode_create = Button(displaywindow, text="Resend otp",
                                   command=lambda: [otp_create_.delete(0, END),
                                                    verification_email_entry("account_creation_window",
                                                                             user_name_entry.get(), email_id_.get(),
                                                                             'retry_otp')])
    list_widgets_account_creation = (Account_creation,user_name,DOB,password,confirm_password,email_id,ph_no,user_name_entry,DOB_,
                                     password_,confirm_password_,email_id_,ph_no_,otp_create,otp_create_,send_otp_create,Next_,
                                     Resend_pincode_create)

    back_login = Button(displaywindow, text="Back", command=lambda: [back_login.destroy(),widgets_destroy(list_widgets_account_creation),Login_window("account_creation_window")])

    # buttons placements
    send_otp_create.place(relx=0.25, rely=0.9)
    Next_.place(relx=0.7, rely=0.9)
    Resend_pincode_create.place(relx=0.45, rely=0.9)
    back_login.place(relx=0.1, rely=0.9)

    # password verification
    print(password_)
    print(type(password_))

    if password_.get() !="":
        if confirm_password_.get() != "":
            if password != confirm_password_:
                confirm_password_.delete(0, END)
                messagebox.showerror("AIY notes", "Confirm passwword is not equal to password, please try again.")
            else:
                pass
        else:
            pass
    else:
        pass

    # otp verification

    if otp_create_.get() != "":
        if pincode != "":
            if otp_create_ != pincode:
                otp_create_.delete(0, END)
                messagebox.showerror("AIY notes", "OTP is not equal to assigned OTP, please try again.")
            else:
                pass
        else:
            pass
    else:
        pass

    '''create account Incomplete
    SQL part remaining '''


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
    username_forget_ = Entry(displaywindow)
    last_password_forget_ = Entry(displaywindow)
    DoB_forget_ = Entry(displaywindow)
    Ph_no_forget_ = Entry(displaywindow)
    email_forget_ = Entry(displaywindow)

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
    username_forget_.place(relx=0.4, rely=0.2)
    last_password_forget_.place(relx=0.4, rely=0.3)
    DoB_forget_.place(relx=0.4, rely=0.4)
    Ph_no_forget_.place(relx=0.4, rely=0.5)
    email_forget_.place(relx=0.4, rely=0.6)

    # OTP segment of forget_account
    otp_forget.place(relx=0.1, rely=0.7)
    otp_forget_.place(relx=0.4, rely=0.7)

    # Button widgets for forget account
    send_otp_forget = Button(displaywindow, text="Send otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_.get(),
                                                                                  email_forget_.get(),
                                                                                  'forget_account', send_otp_forget)])

    # otp verification
    list_entry_forget_account = (
        username_forget_.get(), last_password_forget_.get(), DoB_forget_.get(), Ph_no_forget_.get(),
        email_forget_.get(),
        otp_forget_.get(), otp_forget_.get())

    Next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('forget_account',
                                                                                     list_entry_forget_account)])
    Retry_pincode = Button(displaywindow, text="Resend otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_.get(),
                                                                                  email_forget_.get(),
                                                                                  'retry_otp')])

    list_widgets_forget_account = (
        Forget_label, Username_forget, Last_password_forget, DoB_forget, ph_no_forget, email_forget,
        username_forget_, last_password_forget_, DoB_forget_, Ph_no_forget_, email_forget_, otp_forget,
        otp_forget_, Next_, Retry_pincode,send_otp_forget)

    back_login = Button(displaywindow, text="Back", command=lambda: [back_login.destroy(),widgets_destroy(list_widgets_forget_account), Login_window("forget_account")])

    # Buttons placements of forget account
    Next_.place(relx=0.7, rely=0.8)
    send_otp_forget.place(relx=0.25, rely=0.8)
    Retry_pincode.place(relx=0.45, rely=0.8)
    back_login.place(relx=0.1, rely=0.8)


    if otp_forget_.get() != "":
        if pincode != "":
            if otp_forget_ != pincode:
                otp_forget_.delete(0, END)
                messagebox.showerror("AIY notes", "OTP is not equal to assigned OTP, please try again.")
            else:
                pass
        else:
            pass
    else:
        pass

    '''forget_password Incomplete
    SQL part remaining '''


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
    id_ = Entry(displaywindow)
    password_ = Entry(displaywindow, show="*")

    id_.place(relx=0.3, rely=0.3)
    password_.place(relx=0.3, rely=0.4)

    # Buttons
    list_entry_displaywindow = (id_.get(), password_.get())
    Next = Button(displaywindow, text="Next", command=lambda: [activation_procedure('displaywindow',
                                                                                    list_entry_displaywindow)])
    Forgotpassword = Button(displaywindow, text="Forgot password",
                            command=lambda: [widgets_destroy(loginwindow_list_widgets), Forget_password()])
    Createaccount = Button(displaywindow, text="Create account",
                           command=lambda: [widgets_destroy(loginwindow_list_widgets), account_creation()])

    Next.place(relx=0.7, rely=0.6)
    Forgotpassword.place(relx=0.1, rely=0.6)
    Createaccount.place(relx=0.4, rely=0.6)
    global loginwindow_list_widgets
    loginwindow_list_widgets = (
        wel, signin, loginid, loginpassword, id_, password_, Next, Forgotpassword, Createaccount)

    '''Login display Incomplete
    SQL part remaining'''


# image
# Read the Image
image = Image.open("AIY LOGO_2.png")
# Reszie the image using resize() method
resize_image = image.resize((600, 600))
img = ImageTk.PhotoImage(resize_image)

logo_button = Button(displaywindow, image=img, command=lambda: [logo_button.destroy(), Login_window_1()])
logo_button.pack()

displaywindow.mainloop()
my_c.close()
