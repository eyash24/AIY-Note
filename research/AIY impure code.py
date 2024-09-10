# imports
import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import random
import time
import smtplib
import os

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

# global variable
no_section = 2
no_note = 2
dict_section_note = {"section_1": ["note_1", "note_2"], "section_2": ["note_1", "note_2"]}
activelog_section_note_list = [['section_1','note_1']]
entrylog_section = list()
entrylog_note = list()
deleted_section_list = list()
deleted_notes_section_dict = dict()
directory_path_entry_log = list()
directory_section_note_dict = dict()
active_button_feature_panel = list()
count_maindisplay_function_activated = 0
account_no_user = None
active_feature_panel = None
location_AIY_Logo = "AIY LOGO_2.png"

# for trial purposes
account_no_user = "AIY0001"
username_ = "XAY"
login_id_entry_allow = "AIY_login"
login_password_entry_allow = "AIY_password"

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


def donothing():  # function for trial work
    filewin = Toplevel(displaywindow)
    button = Button(filewin, text="Do nothing button", pady=4)
    button.place(x=50, y=50)


def widgets_destroy(widget_list):
    for i in widget_list:
        i.destroy()


def restart(window, list_widgets):
    if window == "maindisplay":
        for i in list_widgets:
            i.destroy()
        maindisplay()
    else:
        pass


def functions_panel_features(purpose_, list_widgets=None, direct_not=None):
    def widget_shown_destroy(widget):
        if widget.IsShown():
            print(widget + " is shown")
        else:
            print(widget + " is not shown")

    purpose_title = ["+ Add", "Recovery", "About", "- Remove"]
    if purpose_ in purpose_title:
        # feature_panel
        global feature_panel
        feature_panel = PanedWindow(displaywindow, orient="vertical", height=800, width=150, bd=2, bg="#999999")
        feature_panel.pack(side=RIGHT, expand="False")
        feature_panel.configure(sashrelief=FLAT)

        if list_widgets != None:
            global list_widgets_next
            list_widgets.append(feature_panel)
            list_widgets_next = list_widgets
        else:
            pass

        Title_ = Label(feature_panel, text=purpose_, font="calbri 16", bg="#999999")
        Title_.pack(side=TOP)
        feature_panel.add(Title_)

        if purpose_ == "+ Add":
            section_current = activelog_section_note_list[-1][0]
            current_section_ = Label(feature_panel, text="Current Section:", font="calbri 16", pady=4, bg="#999999")
            _current_section_displayed = Label(feature_panel, text=section_current, font="calbri 16", pady=4,
                                               bg="#999999")

            current_section_.pack(side='top')
            feature_panel.add(current_section_)
            _current_section_displayed.pack(side="top")
            feature_panel.add(_current_section_displayed)

            section_add = Button(feature_panel, text="+ Section", pady=4,
                                 command=lambda: [feature_panel_activity(False),
                                                  modify_panel('section', list_widgets_next)])
            note_add = Button(feature_panel, text="+ Note", pady=4,
                              command=lambda: [feature_panel_activity(False),
                                               modify_panel('note', list_widgets_next)])

            section_add.pack(side="top")
            feature_panel.add(section_add)
            note_add.pack(side="top")
            feature_panel.add(note_add)

        elif purpose_ == '- Remove':
            def delete_section_note(purpose_, list_widgets):
                global deleted_section_list, deleted_notes_section_dict

                def delete(purpose_2, list_widgets_2):
                    if combobox_.get() != "":
                        if purpose_2 == "section":
                            deleted_section_list.append(combobox_.get())
                        elif purpose_2 == "note":
                            present_section = present('find_section')
                            list_notes = deleted_notes_section_dict[present_section]
                            if len(list_notes) == 0:
                                deleted_notes_section_dict[present_section] = [combobox_.get()]
                            elif len(list_notes) > 0:
                                list_notes.append(combobox_.get())
                                deleted_notes_section_dict[present_section] = list_notes
                            else:
                                print("not working purpose_2 loop")
                        restart("maindisplay", list_widgets_2)
                    else:
                        print("not working entire delete function ")

                # conditions for proceeding forward
                if purpose_ == "section":
                    name_label = "Section Deletion"
                    instructions = "Please select the section from below:"
                    list_sections = list()
                    if len(deleted_section_list) != 0:
                        for i in entrylog_section:
                            if i not in deleted_section_list:
                                list_sections.append(i)
                            else:
                                pass
                        value_combobox = list_sections
                    else:
                        value_combobox = entrylog_section
                elif purpose_ == "note":
                    name_label = "Note Deletion"
                    instructions = "Please select the note from below:"
                    present_section = present('find_section')
                    list_notes_unverified = dict_section_note[present_section]
                    list_notes_verified = list()
                    if len(deleted_notes_section_dict[present_section]) != 0:
                        for i in list_notes_unverified:
                            if i not in deleted_notes_section_dict[present_section]:
                                list_notes_verified.append(i)
                            else:
                                pass
                    else:
                        list_notes_verified = list_notes_unverified
                    value_combobox = list_notes_verified
                else:
                    name_label = "XYZ"
                    instructions = "XYZ"
                    value_combobox = []

                if len(value_combobox) > 1:
                    # separator widget
                    separator_ = ttk.Separator(feature_panel, orient='horizontal')
                    separator_.pack(side="top")
                    feature_panel.add(separator_)

                    label_name = Label(feature_panel, text=name_label, font="calbri 16", bg='#999999')
                    label_name.pack(side="top")
                    feature_panel.add(label_name)

                    if purpose_ == "note":
                        # extra label for section verification
                        text_selected_section = "Section selected: " + str(present_section)
                        select_section = Label(feature_panel, text=text_selected_section, wraplength=100, bg='#999999')
                        # placement of widget
                        select_section.pack(side="top")
                        feature_panel.add(select_section)
                    else:
                        pass

                    label_instruction = Label(feature_panel, text=instructions, wraplength=100, bg='#999999')
                    Next_ = Button(feature_panel, text="Next", pady=4,
                                   command=lambda: [feature_panel_activity(False), delete(purpose_, list_widgets_next)])
                    Back_ = Button(feature_panel, text="Back", pady=4,
                                   command=lambda: [feature_panel_activity(False),
                                                    restart("maindisplay", list_widgets_next)])
                    combobox_ = ttk.Combobox(feature_panel, text="Options")
                    combobox_["values"] = value_combobox

                    # widget placement
                    label_instruction.pack(side="top")
                    combobox_.pack(side="top")
                    Next_.pack(side="right")
                    Back_.pack(side="left")

                    feature_panel.add(label_instruction)
                    feature_panel.add(combobox_)
                    feature_panel.add(Next_)
                    feature_panel.add(Back_)

                    label_pack = Label(feature_panel, text="", bg="#999999")
                    label_pack.pack(fill=X)
                    feature_panel.add(label_pack)

                elif len(value_combobox) == 1 and purpose_ == "sections":
                    text_messagebox = "The application suggest that at least one " + purpose_ + " be kept undeleted for use."
                    messagebox.showerror("AIY notes", text_messagebox)
                else:
                    print("len(value_combobox) : ", len(value_combobox))
                    text_messagebox = "The application suggest that at least one " + purpose_ + " be kept undeleted for use."
                    messagebox.showerror("AIY notes", text_messagebox)

            if direct_not == "direct_section":
                delete_section_note("section", list_widgets_next)
            elif direct_not == "direct_note":
                delete_section_note("note", list_widgets_next)
            elif direct_not == None:
                text_remove_label = "Select what you want to delete:"
                remove_labal_instruction = Label(feature_panel, text=text_remove_label, wraplength=100, pady=4,
                                                 bg="#999999")
                remove_labal_instruction.pack(side='top')
                feature_panel.add(remove_labal_instruction)

                section_minus = Button(feature_panel, text="- Section", pady=4,
                                       command=lambda: delete_section_note("section", list_widgets_next))
                note_minus = Button(feature_panel, text="- Note", pady=4,
                                    command=lambda: delete_section_note("note", list_widgets_next))

                section_minus.pack(side="top")
                feature_panel.add(section_minus)
                note_minus.pack(side="top")
                feature_panel.add(note_minus)
            else:
                pass

        elif purpose_ == "Recovery":
            def Recovery_function(section_note):
                proceed_recovery = None
                if section_note == "section":
                    if len(deleted_section_list) == 0:
                        text_messagebox = "There is currently no section to be recovered."
                        messagebox.showerror("AIY notes", text_messagebox)
                        proceed_recovey = False
                    else:
                        proceed_recovery = True
                elif section_note == "note":
                    present_section = present('find_section')
                    list_notes = deleted_notes_section_dict[present_section]
                    if len(list_notes) == 0:
                        text_messagebox = "There is currently no note to be recovered."
                        messagebox.showerror("AIY notes", text_messagebox)
                        proceed_recovery = False
                    else:
                        proceed_recovery = True

                def recover(purpose_2, list_widgets_2):
                    if combobox_.get() != "":
                        if purpose_2 == "section":
                            deleted_section_list.remove(combobox_.get())
                        elif purpose_2 == "note":
                            present_section = present('find_section')
                            list_notes = deleted_notes_section_dict[present_section]
                            if combobox_.get() in list_notes:
                                list_notes.remove(combobox_.get())
                                deleted_notes_section_dict[present_section] = list_notes
                            else:
                                print("not working purpose_2 loop")
                        restart("maindisplay", list_widgets_2)
                    else:
                        print("not working entire delete function ")

                if proceed_recovery == True:
                    # separator widget
                    separator_ = ttk.Separator(feature_panel, orient='horizontal')
                    separator_.pack(side="top")
                    feature_panel.add(separator_)

                    if section_note == "section":
                        section_recovery_label = Label(feature_panel, text="Section Recovery", wraplength=100,
                                                       bg="#999999")
                        section_text_label = Label(feature_panel, text="Select the section to recover:", wraplength=100,
                                                   bg="#999999")

                        section_recovery_label.pack(side="top")
                        section_text_label.pack(side="top")
                        feature_panel.add(section_recovery_label)
                        feature_panel.add(section_text_label)
                        value_combobox = deleted_section_list

                    elif section_note == "note":
                        note_recovery_label = Label(feature_panel, text="Section Recovery", wraplength=100,
                                                    bg="#999999")
                        section_current = activelog_section_note_list[-1][0]
                        current_section_text_label = Label(feature_panel, text="Current section:", bg="#999999")
                        current_section_label = Label(feature_panel, text=section_current, bg="#999999")
                        note_text_label = Label(feature_panel, text="Select the note to recover:", wraplength=100,
                                                bg="#999999")

                        note_recovery_label.pack(side="top")
                        current_section_text_label.pack(side="top")
                        current_section_label.pack(side="top")
                        note_text_label.pack(side="top")

                        feature_panel.add(note_recovery_label)
                        feature_panel.add(current_section_text_label)
                        feature_panel.add(current_section_label)
                        feature_panel.add(note_text_label)
                        value_combobox = deleted_notes_section_dict[section_current]

                    Next_ = Button(feature_panel, text="Next", pady=4,
                                   command=lambda: [feature_panel_activity(False),
                                                    recover(section_note, list_widgets_next)])
                    Back_ = Button(feature_panel, text="Back", pady=4,
                                   command=lambda: [feature_panel_activity(False),
                                                    restart("maindisplay", list_widgets_next)])
                    combobox_ = ttk.Combobox(feature_panel, text="Options")
                    combobox_["values"] = value_combobox

                    label_recover_text = Label(feature_panel, text="", bg='#999999')

                    combobox_.pack(side="top")
                    Back_.pack(side="top")
                    Next_.pack(side="top")
                    label_recover_text.pack(fill=X)

                    feature_panel.add(combobox_)
                    feature_panel.add(Back_)
                    feature_panel.add(Next_)
                    feature_panel.add(label_recover_text)

                else:
                    pass

            text_recovery = "Select what you want to recover:"
            recovery_label = Label(feature_panel, text=text_recovery, wraplength=100, bg="#999999", font="calbri 16")
            section_recover = Button(feature_panel, text="Section", pady=4,
                                     command=lambda: Recovery_function("section"))
            note_recover = Button(feature_panel, text='Note', pady=4, command=lambda: Recovery_function("note"))

            recovery_label.pack(side="top")
            section_recover.pack(side="top")
            note_recover.pack(side="top")

            feature_panel.add(recovery_label)
            feature_panel.add(section_recover)
            feature_panel.add(note_recover)

        elif purpose_ == 'About':
            text_about = (
                "This is a computer project undertaken by a few students of The Foundation School, Gunjur,Bangalore. "
                "The aim is to provide a note taking application using python, SQL database and text files."
            )
            about_label = Label(feature_panel, text=text_about, wraplength=100, bg='#999999')
            about_label.pack(side="top")
            feature_panel.add(about_label)
        else:
            pass

        Quit_ = Button(feature_panel, text="Quit", pady=4,
                       command=lambda: [feature_panel_activity(False), feature_panel.destroy()])
        Quit_.pack(side="top")
        feature_panel.add(Quit_)

        label_pack = Label(feature_panel, text="", bg="#999999")
        label_pack.pack(fill=X)
        feature_panel.add(label_pack)
    elif purpose_ == "distroy_feature_panel":
        feature_panel.destroy()
    else:
        pass


def feature_panel_activity(bool, purpose_=None, list_widgets=None, direct_not=None):
    global active_feature_panel, active_button_feature_panel
    active_feature_panel = bool

    if active_feature_panel == False:
        active_button_feature_panel = []
    else:
        pass

    if active_feature_panel == True:
        if len(active_button_feature_panel) == 0:
            if purpose_ != None:
                active_button_feature_panel.append(purpose_)
                if direct_not != None:
                    functions_panel_features(purpose_, list_widgets, direct_not)
                else:
                    functions_panel_features(purpose_, list_widgets)
            else:
                pass

        elif len(active_button_feature_panel) > 0:
            functions_panel_features("distroy_feature_panel")
            active_button_feature_panel.pop()
            active_button_feature_panel.append(purpose_)
            if direct_not != None:
                functions_panel_features(purpose_, list_widgets, direct_not)
            else:
                functions_panel_features(purpose_, list_widgets)
        else:
            pass
    else:
        pass


def present(purpose, list_widgets=None, add_what_section_note=None, section_note_name=None):
    global activelog_section_note_list
    if purpose == "find_section":
        return activelog_section_note_list[-1][0]
    elif purpose == "find_note":
        return activelog_section_note_list[-1][1]
    elif purpose == "add":
        if add_what_section_note is not None:
            if add_what_section_note == "section":
                activelog_section_note_list.append([section_note_name,'note_1'])
            elif add_what_section_note == "note":
                activelog_section_note_list.append([present('find_section'),section_note_name])
        else:
            pass
    else:
        pass

    # Maintainence of activelog_log
    if len(activelog_section_note_list) > 3:
        activelog_section_note_list.pop(0)
    else:
        pass


def text_frame_configure(present_section, present_note_section, purpose=None):
    def textframe_data_notefile_interchange(purpose, note_directory=None):
        def text_file_existance(path):
            file_accessible = None
            try:
                f = open(path, "r")
                text_file_data_ = f.read()
                print(text_file_data_)
                file_accessible = True
                f.close()
            except IOError:
                print("File not accessible")
                file_accessible = False
            return file_accessible

        list_file_existance_option = ["textframe_data_into_notefile", 'notefile_data_into_textframe']
        print("textframe_data_notefile_interchange purpose: ", purpose)
        print("note_directory: ", note_directory)
        if purpose in list_file_existance_option:
            file_accessible = None
            file_accessible = text_file_existance(note_directory)
            print('file_accessible: ', file_accessible)
            if file_accessible != None:
                if file_accessible == False:
                    with open(note_directory, 'a') as f:
                        f.write("")
                    f.close()
                else:
                    pass
            else:
                pass

            if purpose == "notefile_data_into_textframe":
                print("starting to extract data from notefile")
                with open(note_directory, "r") as file_note:
                    data_infile = file_note.read()
                    print("data_infile : ", data_infile)
                    print("data extracted")
                    my_text.insert(END, data_infile)
                    print("data inserted into text frame")
                file_note.close()
            elif purpose == "textframe_data_into_notefile":
                print("starting to extract data from textframe")
                textframe_data = my_text.get('1.0', END).splitlines()
                print("textframe_data: ", textframe_data)
                print("data extracted")
                textframe_new_data = list()
                with open(note_directory, "w") as file_note:
                    for i in textframe_data:
                        new_data = i + "\n"
                        textframe_new_data.append(new_data)
                    print("textframe_new_data: ", textframe_new_data)
                    file_note.writelines(textframe_new_data)
                    print("data inserted into notefile")
                file_note.close()
        elif purpose == "delete_textframe":
            my_text.delete('1.0', 'end')
        else:
            print("not working")

    if purpose == None:
        # previous_section = None, previous_note_section = None
        print("active section_note: ",activelog_section_note_list)
        if len(activelog_section_note_list) > 1:
            previous_note_section = activelog_section_note_list[-2][1]
            previous_section = activelog_section_note_list[-2][0]
        elif len(activelog_section_note_list) == 1:
            previous_note_section = None
        print("activelog_section: ", activelog_section_note_list[-1][0])

        if previous_section is not None:
            if previous_note_section is not None:
                dict_note = directory_section_note_dict[previous_section]
                note_directory_previous = dict_note[
                                              previous_note_section] + "/" + previous_section + " " + previous_note_section + ".txt"
                textframe_data_notefile_interchange('textframe_data_into_notefile', note_directory_previous)
                textframe_data_notefile_interchange("delete_textframe")
            else:
                pass
        else:
            pass

        if present_section != "":
            if present_note_section != "":
                dict_note = directory_section_note_dict[present_section]
                note_directory_present = dict_note[
                                             present_note_section] + "/" + present_section + " " + present_note_section + ".txt"
                textframe_data_notefile_interchange('notefile_data_into_textframe', note_directory_present)
            else:
                pass
        else:
            pass

        restart("maindisplay", list_maindisplay_widgets)

    elif purpose == 'maindisplay_function_text_frame':
        if present_section != "":
            if present_note_section != "":
                dict_note = directory_section_note_dict[present_section]
                note_directory_present = dict_note[
                                             present_note_section] + "/" + present_section + " " + present_note_section + ".txt"
                textframe_data_notefile_interchange('notefile_data_into_textframe', note_directory_present)
            else:
                pass
        else:
            pass


def modify_panel(section_note, list_widgets):
    global no_section, no_note
    count = 0
    if section_note == "section":
        for i in entrylog_section:
            if i not in deleted_section_list:
                count += 1
            else:
                pass
    elif section_note == "note":
        _section_name_ = present("find_section")
        _list_notes_ = dict_section_note[_section_name_]
        for i in _list_notes_:
            if i not in deleted_notes_section_dict[_section_name_]:
                count += 1
    else:
        pass

    section_note_proceed = None
    if count == 20:
        section_note_proceed = False
        text_message = "Application has a limit of only 20 " + section_note + "s to be kept in use. If you want to add a new " \
                       + section_note + "s you must delete an existing section."
        messagebox.showerror("AIY notes", text_message)
    else:
        section_note_proceed = True
        pass

    if section_note_proceed == True:
        if section_note == 'section':
            no_section += 1
            section_name_2 = "section_" + str(no_section)
            dict_section_note[section_name_2] = ['note_1', 'note_2']
            activelog_section_note_list.append([section_name_2,'note_1'])
            restart("maindisplay", list_widgets)
        elif section_note == 'note':
            note_list = list()
            section_name_2 = present("find_section")
            note_list = dict_section_note[section_name_2]
            no_notes = len(note_list)
            new_note = "note_" + str(no_notes + 1)
            note_list.append(new_note)
            dict_section_note[section_name_2] = note_list
            restart("maindisplay", list_widgets)
        else:
            pass
    else:
        pass


def directory_section_note(purpose):
    # section_note path creation
    # require - account_no_user of the user
    def directory_creator_finder(path):
        print("path to check : ", path)
        if not os.path.exists(path):
            print("folder is going to be created")
            os.makedirs(path)
            print("folder created ")
        else:
            print('folder already present')

    if purpose == "creation of folder directory":
        if account_no_user is not None:
            for i in dict_section_note:
                new_path = ""
                note_dict = dict()
                for j in dict_section_note[i]:
                    new_path = "AIY/" + str(account_no_user) + "/" + str(i) + "/" + str(j)
                    print()
                    if new_path not in directory_path_entry_log:
                        directory_path_entry_log.append(new_path)
                    else:
                        pass
                    note_dict[j] = new_path
                    directory_section_note_dict[i] = note_dict
                    directory_creator_finder(new_path)
            for path in directory_path_entry_log:
                print(path)
            print(directory_section_note_dict)
        else:
            pass


def maindisplay():
    # main display
    displaywindow.title("XYZ's Handbook")
    displaywindow.geometry('1000x1000')
    displaywindow["bg"] = '#000000'
    displaywindow.resizable(True, True)

    # function panel bg ="#4d4d4d"
    function_panel = PanedWindow(displaywindow, orient="horizontal", height=60, width=150, bd=4, bg="#000000")
    function_panel.pack(side=TOP, expand=False, fill=X)

    # section panel bg="#999999"
    section_panel = PanedWindow(displaywindow, orient='vertical', height=800, width=150, bd=2, bg="#999999")
    section_panel.pack(side=LEFT, expand="False")
    section_panel.configure(sashrelief=FLAT)

    # note panel bg="#bfbfbf"
    note_panel = PanedWindow(displaywindow, orient='vertical', height=800, width=150, bd=2, bg="#bfbfbf")
    note_panel.pack(side=LEFT, expand="False")
    note_panel.configure(sashrelief=FLAT)

    # text frame
    text_frame = Frame(displaywindow)
    text_frame.pack(side=RIGHT, expand=True, fill=BOTH)

    # Text scrollbar
    text_scroll_y = Scrollbar(text_frame, orient='vertical')
    text_scroll_y.pack(side=RIGHT, fill=Y)

    text_scroll_x = Scrollbar(text_frame, orient='horizontal')
    text_scroll_x.pack(side="bottom", fill=X)

    # Text box
    global my_text
    my_text = Text(text_frame, width=50, height=100, font="calbri 16", selectbackground="#b3ccff",
                   selectforeground="black", undo=True, yscrollcommand=text_scroll_y.set,
                   xscrollcommand=text_scroll_x.set)
    my_text.pack(expand=True, fill=BOTH)

    # configuration of the scrollbar
    text_scroll_x.configure(command=my_text.xview)
    text_scroll_y.configure(command=my_text.yview)

    global list_maindisplay_widgets
    list_maindisplay_widgets = [section_panel, note_panel, text_frame, function_panel]

    # image_2
    logo_Label = Label(displaywindow, image=img_3, bg='#000000')
    logo_Label.place(relx=0.001, rely=0.001)

    separator_1 = ttk.Separator(function_panel, orient='vertical')
    separator_1.place(relx=0.105, rely=0, relheight=1)

    account_name_label = Label(function_panel, text="Username : ", bg="#000000", foreground="white")
    _account_name_display = Label(function_panel, text=username_, bg="#000000", foreground="white")
    account_no_label = Label(function_panel, text="Account No: ", bg="#000000", foreground="white")
    _account_no_display = Label(function_panel, text=account_no_user, bg="#000000", foreground="white")

    account_name_label.place(relx=0.11, rely=0.1)
    _account_name_display.place(relx=0.195, rely=0.1)
    account_no_label.place(relx=0.11, rely=0.5)
    _account_no_display.place(relx=0.195, rely=0.5)

    separator_2 = ttk.Separator(function_panel, orient='vertical')
    separator_2.place(relx=0.265, rely=0, relheight=1)

    current_displayed_section = activelog_section_note_list[-1][0]
    current_displayed_note = activelog_section_note_list[-1][1]
    current_section = Label(function_panel, text="Current Section: ", bg="#000000", foreground="white")
    current_note = Label(function_panel, text="Current Note: ", bg="#000000", foreground="white")
    _section_current_ = Label(function_panel, text=current_displayed_section, bg="#000000", foreground="white")
    _note_current_ = Label(function_panel, text=current_displayed_note, bg="#000000", foreground="white")

    current_section.place(relx=0.27, rely=0.1)
    _section_current_.place(relx=0.38, rely=0.1)
    current_note.place(relx=0.27, rely=0.5)
    _note_current_.place(relx=0.38, rely=0.5)

    separator_3 = ttk.Separator(function_panel, orient='vertical')
    separator_3.place(relx=0.46, rely=0, relheight=1)

    save_ = Button(function_panel, text="Save", pady=4,
                   command=lambda: [feature_panel_activity(True, "Save", list_maindisplay_widgets)])
    quit_ = Button(function_panel, text="Quit", pady=4,
                   command=lambda: displaywindow.destroy())
    add_ = Button(function_panel, text=" + Add", pady=4,
                  command=lambda: [feature_panel_activity(True, "+ Add", list_maindisplay_widgets)])
    remove_ = Button(function_panel, text="- Remove", pady=4,
                     command=lambda: [feature_panel_activity(True, "- Remove", list_maindisplay_widgets)])
    recover_ = Button(function_panel, text="Recover", pady=4,
                      command=lambda: [feature_panel_activity(True, "Recovery", list_maindisplay_widgets)])
    about_ = Button(function_panel, text="About", pady=4,
                    command=lambda: [feature_panel_activity(True, "About", list_maindisplay_widgets)])

    save_.place(rely=0.1, relx=0.475)
    quit_.place(rely=0.1, relx=0.535)
    add_.place(rely=0.1, relx=0.59)
    remove_.place(rely=0.1, relx=0.66)
    recover_.place(rely=0.1, relx=0.75)
    about_.place(rely=0.1, relx=0.83)

    def section_note_formation(section_or_note, text_name, present_name, section_name=None):
        global entrylog_section, entrylog_note
        if section_or_note == "section":
            section_i = Button(section_panel, text=text_name, pady=4, command=lambda:
            [present("add", list_maindisplay_widgets, "section", present_name),
             restart("maindisplay", list_maindisplay_widgets),
             text_frame_configure(present_name, 'note_1', 'maindisplay_function_text_frame'),
             activelog_section_note_list.append([present_name,'note_1'])])
            section_i.pack(side=TOP)
            section_panel.add(section_i)

            if present_name not in entrylog_section:
                entrylog_section.append(present_name)
                deleted_notes_section_dict[present_name] = []
            else:
                pass
        elif section_or_note == "note":
            note_i = Button(note_panel, text=text_name, pady=4, command=lambda:
            [present("add", list_maindisplay_widgets, "note", present_name),
             text_frame_configure(section_name, present_name),
             text_frame_configure(section_name, present_name, 'maindisplay_function_text_frame')])
            note_i.pack(side=TOP)
            note_panel.add(note_i)

            if present_name not in entrylog_note:
                entrylog_note.append(present_name)
            else:
                pass
        else:
            pass

    # section panel
    # buttons and labels
    l_section = Label(section_panel, text="Section", font="calbri 16", bg="#999999")
    l_section.pack(side="top")
    section_panel.add(l_section)

    # section formation
    for i in range(0, no_section):
        name_section_text = "Section " + str(i + 1)
        name_section_present = "section_" + str(i + 1)
        if len(deleted_section_list) != 0:
            if name_section_present not in deleted_section_list:
                section_note_formation("section", name_section_text, name_section_present)
            else:
                pass
        else:
            section_note_formation("section", name_section_text, name_section_present)

    # To add new sections

    section_add = Button(section_panel, text="+ Section", pady=4,
                         command=lambda: [modify_panel('section', list_maindisplay_widgets)])
    section_add.pack(side='bottom')
    section_panel.add(section_add)

    section_subtract = Button(section_panel, text="- Section", pady=4,
                              command=lambda: feature_panel_activity(True, "- Remove", list_maindisplay_widgets,
                                                                     "direct_section"))
    section_subtract.pack(side='bottom')
    section_panel.add(section_subtract)

    label_section = Label(section_panel, text="", bg="#999999")
    label_section.pack(fill=X)
    section_panel.add(label_section)

    # Note's panel
    # buttons and labels
    l_note = Label(note_panel, text="Notes", font="calbri 16", bg="#bfbfbf")
    l_note.pack(side="top")
    note_panel.add(l_note)

    # note formation
    section_name_1 = present("find_section")
    note_list = dict_section_note[section_name_1]
    print("section active: ", section_name_1)
    print("no_note_section: ", note_list)

    for i in note_list:
        list_number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        name_note_text = ""
        new_string = ""
        for j in i:
            if j in list_number:
                new_string += str(j)
            else:
                pass
        name_note_text = "Note " + str(new_string)
        name_note_present = i
        if len(deleted_notes_section_dict[section_name_1]) != 0:
            list_notes_section = deleted_notes_section_dict[section_name_1]
            if name_note_present not in list_notes_section:
                section_note_formation("note", name_note_text, name_note_present, section_name_1)
            else:
                pass
        else:
            section_note_formation("note", name_note_text, name_note_present, section_name_1)

    # To add new notes
    note_add = Button(note_panel, text="+ Note", pady=4,
                      command=lambda: [modify_panel('note', list_maindisplay_widgets)])
    note_add.pack(side='bottom')
    note_panel.add(note_add)

    note_subtract = Button(note_panel, text="- Note", pady=4,
                           command=lambda: feature_panel_activity(True, "- Remove", list_maindisplay_widgets,
                                                                  "direct_note"))
    note_subtract.pack(side='bottom')
    note_panel.add(note_subtract)

    l_note_empty = Label(note_panel, text="", bg="#bfbfbf")
    l_note_empty.pack(fill=X)
    note_panel.add(l_note_empty)

    for i in dict_section_note:
        print(i, ":", dict_section_note[i])

    directory_section_note('creation of folder directory')
    print(activelog_section_note_list)

    def start_note_text_frame(count):
        if count == 0:
            activelog_section_note_list = [["section_1","note_1"]]
            text_frame_configure(activelog_section_note_list[0][0],activelog_section_note_list[0][1], 'maindisplay_function_text_frame')
        else:
            pass

    global count_maindisplay_function_activated
    start_note_text_frame(count_maindisplay_function_activated)
    count_maindisplay_function_activated += 1


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

    # for trial run of whole system (temporary)
    if window == "login_displaywindow":
        login_id = list_entry[0]
        password_ = list_entry[1]
        login_id_entry_allow = "AIY_login"
        login_password_entry_allow = "AIY_password"
        if login_id == login_id_entry_allow and password_ == login_password_entry_allow:
            maindisplay()
        else:
            pass


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
                                        '\n The account activation process has begun. For creation of the account, we require you to enter the below displayed pin code into the program,' \
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
    Next = Button(displaywindow, text="Next", command=lambda: [widgets_destroy(loginwindow_list_widgets),
                                                               activation_procedure('displaywindow',
                                                                                    [id_.get(), password_.get()])])
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

    def verification_password_otp():
        # password verification
        if password_.get() != "":
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

    # buttons for account_creation_window
    send_otp_create = Button(displaywindow, text="Send otp", command=lambda: [otp_create_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "account_creation_window",
                                                                                  user_name_entry.get(),
                                                                                  email_id_.get(),
                                                                                  'account_activation_otp',
                                                                                  send_otp_create)])

    Next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('account_creation_window',
                                                                                     [user_name_entry.get(), DOB_.get(),
                                                                                      password_.get(),
                                                                                      confirm_password_.get(),
                                                                                      email_id_.get(), ph_no_.get(),
                                                                                      otp_create_.get()]),
                                                                verification_password_otp()])
    Resend_pincode_create = Button(displaywindow, text="Resend otp",
                                   command=lambda: [otp_create_.delete(0, END),
                                                    verification_email_entry("account_creation_window",
                                                                             user_name_entry.get(), email_id_.get(),
                                                                             'retry_otp')])
    list_widgets_account_creation = (
        Account_creation, user_name, DOB, password, confirm_password, email_id, ph_no, user_name_entry, DOB_,
        password_, confirm_password_, email_id_, ph_no_, otp_create, otp_create_, send_otp_create, Next_,
        Resend_pincode_create)

    back_login = Button(displaywindow, text="Back",
                        command=lambda: [back_login.destroy(), widgets_destroy(list_widgets_account_creation),
                                         Login_window("account_creation_window")])

    # buttons placements
    send_otp_create.place(relx=0.25, rely=0.9)
    Next_.place(relx=0.7, rely=0.9)
    Resend_pincode_create.place(relx=0.45, rely=0.9)
    back_login.place(relx=0.1, rely=0.9)

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

    def otp_verify():
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

    #   widgets for forget account
    send_otp_forget = Button(displaywindow, text="Send otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_.get(),
                                                                                  email_forget_.get(),
                                                                                  'forget_account', send_otp_forget)])

    Next_ = Button(displaywindow, text="Next", command=lambda: [activation_procedure('forget_account',
                                                                                     [username_forget_.get(),
                                                                                      last_password_forget_.get(),
                                                                                      DoB_forget_.get(),
                                                                                      Ph_no_forget_.get(),
                                                                                      email_forget_.get(),
                                                                                      otp_forget_.get(),
                                                                                      otp_forget_.get()]),
                                                                otp_verify()])
    Retry_pincode = Button(displaywindow, text="Resend otp", command=lambda: [otp_forget_.delete(0, END),
                                                                              verification_email_entry(
                                                                                  "forget_account",
                                                                                  username_forget_.get(),
                                                                                  email_forget_.get(),
                                                                                  'retry_otp')])

    list_widgets_forget_account = (
        Forget_label, Username_forget, Last_password_forget, DoB_forget, ph_no_forget, email_forget,
        username_forget_, last_password_forget_, DoB_forget_, Ph_no_forget_, email_forget_, otp_forget,
        otp_forget_, Next_, Retry_pincode, send_otp_forget)

    back_login = Button(displaywindow, text="Back",
                        command=lambda: [back_login.destroy(), widgets_destroy(list_widgets_forget_account),
                                         Login_window("forget_account")])

    # Buttons placements of forget account
    Next_.place(relx=0.7, rely=0.8)
    send_otp_forget.place(relx=0.25, rely=0.8)
    Retry_pincode.place(relx=0.45, rely=0.8)
    back_login.place(relx=0.1, rely=0.8)

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
    Next = Button(displaywindow, text="Next", command=lambda: [activation_procedure('login_displaywindow',
                                                                                    [id_.get(), password_.get()])])
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
image = Image.open(location_AIY_Logo)
# Resize the image using resize() method
resize_image = image.resize((600, 600))
img = ImageTk.PhotoImage(resize_image)
image.close()

image_3 = Image.open(location_AIY_Logo)
resize_image_3 = image_3.resize((100, 50))
img_3 = ImageTk.PhotoImage(resize_image_3)

logo_button = Button(displaywindow, image=img, command=lambda: [logo_button.destroy(), Login_window_1()])
logo_button.pack()

displaywindow.mainloop()
my_c.close()
