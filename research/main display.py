# imports
import mysql.connector
from tkinter import *
#from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import random
import time
import smtplib
import os

# display window
displaywindow = Tk()
displaywindow.title('AIY Notes')
displaywindow.resizable(False, False)
displaywindow["bg"] = '#000000'

'''
# Connectio to MYSQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)

# create a cursor and initializing sql terminal
my_c = mydb.cursor()
'''

# global variable
no_section = 2
no_note = 2
dict_section_note = {"section_1": ["note_1", "note_2"], "section_2": ["note_1", "note_2"]}
activelog_section = ["section_1"]
activelog_note = list()
entrylog_section = list()
entrylog_note = list()
deleted_section_list = list()
deleted_notes_section_dict = dict()
directory_log = list()
account_no_user = None


# for Trial purposes
account_no_user = "AIY0001"
activelog_note = ["Note_1"]
username_ = "XAY"

def donothing(): # function for trial work
    filewin = Toplevel(displaywindow)
    button = Button(filewin, text="Do nothing button")
    button.place(x=50, y=50)

def restart(window, list_widgets):
    if window == "maindisplay":
        for i in list_widgets:
            i.destroy()
        maindisplay()
    else:
        pass

def directory_creator_finder(path):
    if not os.path.exists(path):
        print("folder is going to be created")
        os.makedirs(path)
        print("folder created ")
    else:
        print('folder already present')

def present(purpose, list_widgets = None, add_what_section_note = None, section_note_name = None):
    global activelog_section,activelog_note
    if purpose == "find_section":
        return activelog_section[-1]
    elif purpose == "find_note":
        return activelog_note[-1][0]
    elif purpose == "add":
        print("section_note_name : ",section_note_name)
        if add_what_section_note is not None:
            if add_what_section_note == "section":
                activelog_section.append(section_note_name)
            elif add_what_section_note == "note":
                activelog_note.append(section_note_name)
        else:
            pass
    else:
        pass

    # Maintainence of entry_log
    if len(activelog_section) > 2:
        activelog_section.pop(0)
    elif len(activelog_note) > 2:
        activelog_note.pop(0)
    else:
        pass
    restart("maindisplay", list_widgets)

def modify_panel(section_note,list_widgets):
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
        messagebox.showerror("AIY notes",text_message)
    else:
        section_note_proceed = True
        pass

    if section_note_proceed == True:
        if section_note == 'section':
            no_section += 1
            section_name_2 = "section_" + str(no_section)
            dict_section_note[section_name_2] = ['note_1','note_2']
            restart("maindisplay", list_widgets)
        elif section_note == 'note':
            note_list = list()
            section_name_2 = present("find_section")
            note_list = dict_section_note[section_name_2]
            no_notes = len(note_list)
            new_note = "note_"+str(no_notes + 1)
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
    if purpose == "creation of folder directory":
        if account_no_user is not None:
            for i in dict_section_note:
                new_path = "AIY/" + str(account_no_user)+"/" + str(i)
                if new_path not in directory_log:
                    directory_log.append(new_path)
                else:
                    #directory_creator_finder(new_path_note)
                    pass
            for path in directory_log:
                print(path)
        else:
            pass

proceed = True
if proceed == True:
    # main display
    displaywindow.title("XYZ's Handbook")
    displaywindow.geometry('1000x1000')
    displaywindow["bg"] = '#000000'
    displaywindow.resizable(True, True)

    def functions_panel_features(purpose_, list_widgets=None):
        feature_panel = PanedWindow(displaywindow, orient="vertical", height=800, width=150, bd=2, bg="#999999")
        feature_panel.pack(side=RIGHT, expand="False")
        feature_panel.configure(sashrelief=FLAT)

        global list_widgets_next
        list_widgets.append(feature_panel)
        list_widgets_next = list_widgets

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

                label_name = Label(feature_panel, text=name_label, font="calbri 16",bg='#e6e6e6')
                label_name.pack(side="top")
                feature_panel.add(label_name)

                if purpose_ == "note":
                    # extra label for section verification
                    text_selected_section = "section chose section: " + str(present_section)
                    select_section = Label(feature_panel, text=text_selected_section, wraplength=100, bg='#e6e6e6')
                    # placement of widget
                    select_section.pack(side="top")
                    feature_panel.add(select_section)
                else:
                    pass

                label_instruction = Label(feature_panel, text=instructions,wraplength=100,bg='#e6e6e6')
                Next_ = Button(feature_panel, text="Next", padx=4, command=lambda: delete(purpose_, list_widgets_next))
                Back_ = Button(feature_panel, text="Back", padx=4, command=lambda: [restart("maindisplay", list_widgets_next)])
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
                text_messagebox = "The application suggest that atleast one " + purpose_ + " be kept undeleted for use."
                messagebox.showerror("AIY notes", text_messagebox)
            else:
                print("len(value_combobox) : ", len(value_combobox))
                text_messagebox = "The application suggest that atleast one " + purpose_ + " be kept undeleted for use."
                messagebox.showerror("AIY notes", text_messagebox)

        purpose_title = ["+ Add", "Recovery", "About", "- Remove", "Search"]
        if purpose_ in purpose_title:
            Title_ = Label(feature_panel, text=purpose_, font="calbri 16", bg="#999999")
            Title_.pack(side=TOP)
            feature_panel.add(Title_)

            if purpose_ == "+ Add":
                section_current = activelog_section[-1]
                current_section_ = Label(feature_panel, text="Current Section:", font="calbri 16", pady=4, bg="#e6e6e6")
                _current_section_displayed = Label(feature_panel, text=section_current, font="calbri 16", pady=4,
                                                   bg="#e6e6e6")

                current_section_.pack(side='top')
                feature_panel.add(current_section_)
                _current_section_displayed.pack(side="top")
                feature_panel.add(_current_section_displayed)

                section_add = Button(feature_panel, text="+ Section", bg="#999999", pady=4,
                                     command=lambda: [modify_panel('section', list_widgets_next)])
                note_add = Button(feature_panel, text="+ Note", bg="#999999", pady=4,
                                  command=lambda: [modify_panel('note', list_widgets_next)])

                section_add.pack(side="top")
                feature_panel.add(section_add)
                note_add.pack(side="top")
                feature_panel.add(note_add)

            elif purpose_ == '- Remove':
                section_current = activelog_section[-1]
                current_section_ = Label(feature_panel, text="Current Section:", font="calbri 16", pady=4, bg="#e6e6e6")
                _current_section_displayed = Label(feature_panel, text=section_current, font="calbri 16", pady=4, bg="#e6e6e6")

                current_section_.pack(side='top')
                feature_panel.add(current_section_)
                _current_section_displayed.pack(side="top")
                feature_panel.add(_current_section_displayed)

                section_minus = Button(feature_panel, text="- Section", bg="#999999", pady=4,command=lambda: delete_section_note("section",list_widgets_next))
                note_minus = Button(feature_panel, text="- Note", bg="#999999", pady=4,command=lambda: delete_section_note("note",list_widgets_next))

                section_minus.pack(side="top")
                feature_panel.add(section_minus)
                note_minus.pack(side="top")
                feature_panel.add(note_minus)

            else:
                pass

            Quit_ = Button(feature_panel, text="Quit", bg="#999999", pady=4, command=lambda: feature_panel.destroy())
            Quit_.pack(side="top")
            feature_panel.add(Quit_)

            label_pack = Label(feature_panel, text="", bg="#999999")
            label_pack.pack(fill=X)
            feature_panel.add(label_pack)
        else:
            pass

    def maindisplay():

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
        my_text = Text(text_frame, width=50, height=100, font="calbri 16", selectbackground="#b3ccff",
                       selectforeground="black", undo=True, yscrollcommand=text_scroll_y.set,
                       xscrollcommand=text_scroll_x.set)
        my_text.pack(expand=True, fill=BOTH)

        # configuration of the scrollbar
        text_scroll_x.configure(command=my_text.xview)
        text_scroll_y.configure(command=my_text.yview)

        global list_maindisplay_widgets
        list_maindisplay_widgets = [section_panel, note_panel, text_frame, function_panel]

        '''# image
        # Read the Image
        image = Image.open("/Users/yashlucky/Desktop/AIY LOGO_2.png")
        # Reszie the image using resize() method
        resize_image = image.resize((100, 50))
        img = ImageTk.PhotoImage(resize_image)

        logo_Label = Label(displaywindow, image=img, bg='#000000')
        logo_Label.place(relx=0.001, rely=0.001)'''

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

        current_displayed_section = activelog_section[-1]
        current_displayed_note = activelog_note[-1]
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

        save_ = Button(function_panel, text="Save", bg="#000000",pady=4, command=lambda: functions_panel_features("Save",list_maindisplay_widgets))
        quit_ = Button(function_panel, text="Quit", bg="#000000",pady=4, command=lambda: functions_panel_features("Quit",list_maindisplay_widgets))
        add_ = Button(function_panel, text=" + Add", bg="#000000",pady=4, command=lambda: functions_panel_features("+ Add",list_maindisplay_widgets))
        remove_ = Button(function_panel, text="- Remove", bg="#000000",pady=4, command=lambda: functions_panel_features("- Remove",list_maindisplay_widgets))
        recover_ = Button(function_panel, text="Recover", bg="#000000",pady=4, command=lambda: functions_panel_features("Recovery",list_maindisplay_widgets))
        about_ = Button(function_panel, text="About", bg="#000000",pady=4, command=lambda: functions_panel_features("About"))
        search_ = Button(function_panel, text="Search", bg="#000000",pady=4, command=lambda: functions_panel_features("Search",list_maindisplay_widgets))

        save_.place(rely=0.1, relx=0.475)
        quit_.place(rely=0.1, relx=0.535)
        add_.place(rely=0.1, relx=0.59)
        remove_.place(rely=0.1, relx=0.66)
        recover_.place(rely=0.1, relx=0.75)
        search_.place(rely=0.1, relx=0.83)
        about_.place(rely=0.1, relx=0.905)



        def section_note_formation(section_or_note, text_name, present_name):
            global entrylog_section,entrylog_note
            if section_or_note == "section":
                section_i = Button(section_panel, text=text_name, pady=4, bg="#999999", command=lambda:
                [present("add", list_maindisplay_widgets, "section", present_name)])
                section_i.pack(side=TOP)
                section_panel.add(section_i)

                if present_name not in entrylog_section:
                    entrylog_section.append(present_name)
                    deleted_notes_section_dict[present_name] = []
                else:
                    pass
            elif section_or_note == "note":
                note_i = Button(note_panel, text=text_name, pady=4, bg="#999999", command=lambda:
                [present("add", list_maindisplay_widgets, "note", present_name)])
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
            name_section_text = "Section "+str(i+1)
            name_section_present = "section_"+str(i+1)
            if len(deleted_section_list) != 0:
                if name_section_present not in deleted_section_list:
                    section_note_formation("section",name_section_text,name_section_present)
                else:
                    pass
            else:
                section_note_formation("section", name_section_text, name_section_present)

        # To add new sections
        section_add = Button(section_panel, text="+ Section", pady=4, bg="#999999", command=lambda: [modify_panel('section',list_maindisplay_widgets)])
        section_add.pack(side='bottom')
        section_panel.add(section_add)

        section_subtract = Button(section_panel, text="- Section", pady=4, bg="#999999", command=lambda: functions_panel_features("- Remove",list_maindisplay_widgets))
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
                    section_note_formation("note", name_note_text, name_note_present)
                else:
                    pass
            else:
                section_note_formation("note", name_note_text, name_note_present)

        # To add new notes
        note_add = Button(note_panel, text="+ Note",pady=4, bg="#bfbfbf", command=lambda: [modify_panel('note',list_maindisplay_widgets)])
        note_add.pack(side='bottom')
        note_panel.add(note_add)

        note_subtract = Button(note_panel, text="- Note",pady=4, bg="#bfbfbf", command=lambda: functions_panel_features("- Remove",list_maindisplay_widgets))
        note_subtract.pack(side='bottom')
        note_panel.add(note_subtract)

        l_note_empty = Label(note_panel, text="", bg="#bfbfbf")
        l_note_empty.pack(fill=X)
        note_panel.add(l_note_empty)

        for i in dict_section_note:
            print(i, ":", dict_section_note[i])

        directory_section_note('creation of folder directory')
        print(activelog_section, activelog_note, sep="\n")

        displaywindow.mainloop()

    maindisplay()
else:
    pass
