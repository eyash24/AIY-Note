# login display
from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
import random
from time import *
import smtplib

# login display window
loginwindow = Tk()
loginwindow.title('AIY Notes')
loginwindow.geometry('500x500')
loginwindow.resizable(False, False)
loginwindow["bg"] = '#bfbfbf'

def donothing():
    filewin = Toplevel(loginwindow)
    button = Button(filewin, text="Do nothing button")
    button.place(x=50, y=50)

proceed = False
def activation_procedure(window,list_entry):
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
                print()
                # it means that no button is getting destroyed
        elif email_id != "" or username != "":
            messagebox.showerror("AIY notes", "Please fill in the email id part and username and retry")
        else:
            messagebox.showerror("AIY notes", "Please fill in the email id part and username and retry")
    else:
        messagebox.showerror("AIY notes","Error")

def OTP_system(username_receiver, email_id, otp_purpose):
    Username = username_receiver
    email_reciever = email_id
    sender_email = ""
    password = ""

    # pin_code segment
    global Pin_code
    pincode = str(random.randint(1000, 9999))

    print("starting to send email")
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()

        smtp.login(sender_email, password)
        subject = 'AIY Notes'

        # message and custom subject segment
        global body
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
                    '\n The account recovery has been begun.For the complete authenticity we require you to enter the below display pin code into the program,' \
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

def account_creation(): # create accounts display window
    account_creation_window = Tk()
    account_creation_window.title('AIY Notes')
    account_creation_window.geometry('500x500')
    account_creation_window.resizable(False, False)
    account_creation_window["bg"] = '#bfbfbf'

    # label for creation of new accounts
    Account_creation = Label(account_creation_window, text="Account Creation", font="zapfino 16 bold")
    user_name = Label(account_creation_window, text="Username:")
    DOB = Label(account_creation_window, text="Date of Birth:")
    password = Label(account_creation_window, text="Password:")
    confirm_password = Label(account_creation_window, text="Confirm password:")
    email_id = Label(account_creation_window, text="Email id:")
    ph_no = Label(account_creation_window, text="Phone.no:")

    # Entry widgets for creation of new accounts
    user_name_entry = Entry(account_creation_window)
    DOB_ = Entry(account_creation_window)
    password_ = Entry(account_creation_window)
    confirm_password_ = Entry(account_creation_window)
    email_id_ = Entry(account_creation_window)
    ph_no_ = Entry(account_creation_window)

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
    otp_create = Label(account_creation_window, text="OTP Pin:", font="Calbri 14")
    otp_create_ = Entry(account_creation_window)

    # OTP placement
    otp_create.place(relx=0.1, rely=0.8)
    otp_create_.place(relx=0.4, rely=0.8)

    # buttons for account_creation_window
    send_otp_create = Button(account_creation_window, text="Send otp", command=lambda: [otp_create_.delete(0, END), verification_email_entry("account_creation_window", user_name_entry.get(), email_id_.get(), 'account_activation_otp', send_otp_create)])
    send_otp_create.place(relx=0.4, rely=0.9)

    list_entry_account_creation_window = (user_name_entry.get, DOB_.get(), password_.get(), confirm_password_.get(), email_id_.get(), ph_no_.get(),otp_create_.get())

    Next_ = Button(account_creation_window, text="Next", command=lambda: [account_creation_window.destroy(), activation_procedure(account_creation_window,list_entry_account_creation_window)])
    Next_.place(relx=0.7, rely=0.9)

    Resend_pincode_create = Button(account_creation_window, text="Resend otp", command=lambda: [otp_create.delete(0, END), verification_email_entry("account_creation_window", user_name_entry.get(), email_id_.get(), 'retry_otp')])
    Resend_pincode_create.place(relx=0.1, rely=0.9)

    account_creation_window.mainloop()

    '''create account Incomplete'''

def Forget_password():
    forget_account = Tk()
    forget_account.title('AIY Notes')
    forget_account.geometry('500x500')
    forget_account.resizable(False, False)
    forget_account["bg"] = '#bfbfbf'

    # Label and entry widgets for the forget_account
    # Label widgets
    Forget_label = Label(forget_account, text="Forget_account", font="zapfino 16 bold")
    Username_forget = Label(forget_account, text="Username:")
    Last_password_forget = Label(forget_account, text="Password used: ")
    DoB_forget = Label(forget_account, text="Date of birth:")
    ph_no_forget = Label(forget_account, text="Phone.no:")
    email_forget = Label(forget_account, text="Email id:")

    # Entry widgets
    username_forget_ = Entry(forget_account)
    last_password_forget_ = Entry(forget_account)
    DoB_forget_ = Entry(forget_account)
    Ph_no_forget_ = Entry(forget_account)
    email_forget_ = Entry(forget_account)

    # OTP system recover
    otp_forget = Label(forget_account, text="OTP Pin:")
    otp_forget_ = Entry(forget_account)

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
    send_otp_forget = Button(forget_account, text="Send otp", command=lambda: [otp_forget_.delete(0, END), verification_email_entry("forget_account", username_forget_.get(),email_forget_.get(),'forget_account', send_otp_forget)])
    send_otp_forget.place(relx=0.4, rely=0.9)

    list_entry_forget_account = (username_forget_.get(), last_password_forget_.get(), DoB_forget_.get(), Ph_no_forget_.get(), email_forget_.get(), otp_forget_.get(), otp_forget_.get())
    Next_ = Button(forget_account, text="Next", command=lambda: [forget_account.destroy(), activation_procedure(forget_account, list_entry_forget_account)])
    Next_.place(relx=0.7, rely=0.9)

    Retry_pincode = Button(forget_account, text="Resend pincode", command=lambda: [otp_forget_.delete(0, END), verification_email_entry("forget_account", username_forget_.get(), email_forget_.get(), 'retry_otp')])
    Retry_pincode.place(relx=0.1, rely=0.9)
    print(type(email_forget_.get()))

    forget_account.mainloop()

    '''forget_password Incomplete'''

# Welcome label
wel = Label(loginwindow, text="Welcome To AIY Notes", font="zapfino 16 bold")
signin = Label(loginwindow, text="Sign in", font="calbri 16")
wel.place(relx=0.2)
signin.place(relx=0.3, rely=0.2)

# login and entry
loginid = Label(loginwindow, text="Login id:")
loginid.place(relx=0.1, rely=0.3)
loginpassword = Label(loginwindow, text="password")
loginpassword.place(relx=0.1, rely=0.4)
# entry widgets
id_ = Entry(loginwindow)
password_ = Entry(loginwindow, show="*")

id_.place(relx=0.3, rely=0.3)
password_.place(relx=0.3, rely=0.4)

# Buttons
list_entry_loginwindow = (id_.get(), password_.get())
Next = Button(loginwindow, text="Next", command=lambda: [loginwindow.destroy(), activation_procedure(loginwindow, list_entry_loginwindow)])
Forgotpassword = Button(loginwindow, text="Forgot password", command=lambda: [loginwindow.destroy(), Forget_password()])
Createaccount = Button(loginwindow, text="Create account", command=lambda: [loginwindow.destroy(), account_creation()])

Next.place(relx=0.7, rely=0.6)
Forgotpassword.place(relx=0.1, rely=0.6)
Createaccount.place(relx=0.4, rely=0.6)

loginwindow.mainloop()