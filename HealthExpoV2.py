from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk

from pygame import mixer
import json
import pandas

import os
import random
import time

color1 = "#6E85B7"
color2 = "#B2C8DF"
color3 = "#C4D7E0"
color4 = "#F8F9D7"
BLACK = "#000505"
FONT = ("arial", 16)



with open(os.path.join("Lines", "index.txt")) as assign_index:
    patient_num_assign = int(assign_index.read())

# for audio
mixer.init()

the_key = "key"
first_time = True

################# FUNCTIONALITY ##################


def testing_bot():
    rand_name = random.choice(['John', 'Mary', 'Jerry', 'James', 'Matthew', 'Mark', 'Luke', 'John', 'Daniel', 'Ezekiel',
                               'Esther', 'Melchizideck', 'Solomon', 'David', 'Moses', 'Jacob', 'Esau', 'Joseph',
                               'Marvin', 'Melvin', 'Kyle', 'Kendell', 'Ava', 'Amanda', 'Archie', 'Bo', 'Bob', 'Braden',
                               'Brantley', 'Carter', 'Cam', 'Carly'])

    rand_address = random.choice(["Candy Road", "Walnut Creek road", "my address", "address road", "james road", "john road",
                                  "brantley road", "Johnathan road", "king road", "Violet road", "ava road",
                                  "taylor road", "Oakwood drive", "jamie road", "arkansas road"])

    rand_phone = ''.join([str(num) for num in random.choices(list(range(10)), k=10)])

    name_entry.insert(0, rand_name)
    address_entry.insert(0, rand_address)
    phone_entry.insert(0, rand_phone)


def kick_out_plus_lw():
    kick_out()
    deploy_line_window()


def deploy_line_window():
    global first_time
    scraper()
    if first_time:
        first_time = False

        lw = ctk.CTkToplevel()
        lw.title("Line Window")
        lw.geometry("500x700")

        dental_line = ctk.CTkLabel(lw, textvariable=dent_line_mark, font=FONT)
        dental_line.grid(column=0, row=1, sticky="N")

        dental_label = ctk.CTkLabel(lw, text="Dental", font=FONT)
        dental_label.grid(column=0, row=0, sticky="N")

        mental_line = ctk.CTkLabel(lw, textvariable=ment_line_mark, font=FONT)
        mental_line.grid(column=1, row=1, sticky="N")

        mental_label = ctk.CTkLabel(lw, text="Mental", font=FONT)
        mental_label.grid(column=1, row=0)

        oriental_line = ctk.CTkLabel(lw, textvariable=orient_line_mark, font=FONT)
        oriental_line.grid(column=2, row=1)

        oriental_label = ctk.CTkLabel(lw, text="Oriental", font=FONT)
        oriental_label.grid(column=2, row=0)

        lw.mainloop()


def log_info_format():
    """checks all information put in by the log_tab, formats it"""
    if name_entry.get() == "" or phone_entry.get() == "" or address_entry.get() == "":
        messagebox.showwarning(title="Empty Entries", message="Looks like you have not filled out the entries")

    elif not dental_checked.get() and not mental_checked.get() and not oriental_checked.get():
        messagebox.showwarning(title="Empty Services", message="Looks like you have not filled out the Services")

    else:
        new_patient = [patient_num_assign, name_entry.get(), phone_entry.get(), address_entry.get()]

        # add services here
        if dental_checked.get():
            new_patient.append('Dental')
        else:
            new_patient.append(" ")

        if mental_checked.get():
            new_patient.append("Mental")
        else:
            new_patient.append(" ")

        if oriental_checked.get():
            new_patient.append("Oriental")
        else:
            new_patient.append(" ")

        print(new_patient)

        record(patient_num_assign, new_patient)

        testing_bot()


def record(patient_num, new_patient):
    '''Puts patients in line, records information into csv, links the patient number to the patient list'''

    record_patients_data = pandas.read_csv("record_patients.csv")
    print("permanent saving")
    new_dict = {
        "patient_num": [patient_num],
        "name": [new_patient[1]],
        "phone": [new_patient[2]],
        "address": [new_patient[3]],
        "dental": [new_patient[4]],
        "mental": [new_patient[5]],
        "oriental": [new_patient[6]],
    }

    new_data = pandas.DataFrame(new_dict)
    modified_data = pandas.concat([record_patients_data, new_data], ignore_index=True, join="inner")
    print(modified_data)
    modified_data.to_csv("record_patients.csv", index=False)

    sorted_services = sort_the_lines()

    for service in sorted_services:
        # service is a service in string form
        if service in new_patient:
            print(f"we found it,{service}, we will write in it now")
            write_in_a_file(service, patient_num)
            # mark that service so we don't run into it again in self.re_enter()
            the_service_index = new_patient.index(service)
            new_patient[the_service_index] = service + 'x'
            print(new_patient)
            break
        else:
            print('found no match')

    # add this information to the json file
    new_data = {patient_num: new_patient}
    with open(os.path.join("Databases", "patients.json")) as file:
        data = json.load(file)
    data.update(new_data)
    with open(os.path.join("Databases", "patients.json"), 'w') as file:
        json.dump(data, file, indent=4)

    tick_counter()
    clear_inputs()


def sort_the_lines():
    """looks at the lengths of each medical line. returns a list of smallest to largest"""
    # this is a sub thing to self.record()

    # read all the lines, defines lengths
    with open(os.path.join("Lines", "Dental.txt")) as d_file:
        d_line_len = len(d_file.read().split())
        # self.d_line_len is a integer that defines the length of the dental line

    with open(os.path.join("Lines", "Mental.txt")) as m_file:
        m_line_len = len(m_file.read().split())

    with open(os.path.join("Lines", "Oriental.txt")) as o_file:
        o_line_len = len(o_file.read().split())

    line_lengths_list = [[d_line_len, "Dental"], [m_line_len, "Mental"], [o_line_len, "Oriental"]]

    x_list = [d_line_len, o_line_len, m_line_len]
    x_list.sort()
    y_list = []
    for length in x_list:
        for pair in line_lengths_list:
            if pair[0] == length:
                y_list.append(pair[1])
                line_lengths_list.remove(pair)
    # will tuple unpacking work here? learn tuple unpacking

    # x_list is a list of services, the first is the shortest line, the last is the longest line
    return y_list


def write_in_a_file(service, patient_num):
    with open(os.path.join("Lines", f"{service}.txt"), 'a') as file:
        file.write(str(patient_num) + ' ')


def clear_inputs():
    # clear the text edits
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    address_entry.delete(0, END)

    # clear the checkboxes
    dental_button.deselect()
    mental_button.deselect()
    oriental_button.deselect()

    # for the SC
    confirm_button.deselect()
    to_be_SC_entry.delete(0, END)
    key_entry.delete(0, END)


def tick_counter():
    # Counter on the UI
    global patient_num_assign
    patient_num_assign += 1
    with open(os.path.join("Lines", "index.txt"), mode='w') as back_in_index:
        back_in_index.write(str(patient_num_assign))
    counter_label.configure(text=str(patient_num_assign))


def kick_out():
    '''takes the first one in a specified line out'''
    global line_to_be_edited

    with open(os.path.join("Lines", f"{line_to_be_edited.get()}.txt")) as selected_file:
        data = selected_file.read()
        data = data.split()

    # check if I chose one service to take out of AND check if the number I typed in matches the first in line
    if line_to_be_edited.get() != '' and to_be_SC_entry.get() == data[0]:
        mixer.music.load("notification_sound2.mp3")
        mixer.music.play(loops=0)

        data.pop(0)

        with open(os.path.join("Lines", f"{line_to_be_edited.get()}.txt", 'w')) as update_file:
            ready_to_write = ' '.join(data) + ' '
            update_file.write(ready_to_write)

        re_enter(int(to_be_SC_entry.get()))

    else:
        messagebox.showwarning(title="Oops", message="It looks like you either:\ndid not choose a service to edit"
                                                     "\nor\nthe number typed in does not match the first in line!")


def re_enter(patient_num):
    """places the patient num back into another line"""

    with open(os.path.join("Databases", "patients.json")) as file:
        patients = json.load(file)

    patient = patients[str(patient_num)]

    sorted_services = sort_the_lines()
    print(patient)

    check_if_finished_three = 0

    for service in sorted_services:
        if service in patient:
            print(f"we found it,{service}, second in that line now")
            with open(os.path.join("Lines", f"{service}.txt")) as file:
                contents = file.read()
                xlist = contents.split()
                xlist.append(str(patient_num))

                sliced_list = xlist[1::]
                sliced_list.sort()
                sliced_list.insert(0, xlist[0])

            with open(os.path.join("Lines", f"{service}.txt", 'w')) as file:
                ready_to_go = ' '.join(sliced_list) + ' '
                file.write(ready_to_go)

            the_service_index = patient.index(service)
            patient[the_service_index] = service + 'x'

            # now that we've marked the service as done with an x, we will now update the patients.json
            with open(os.path.join("Databases", "patients.json"), 'w') as file:
                patients[str(patient_num)] = patient
                json.dump(patients, file, indent=4)
            break
        else:
            check_if_finished_three += 1

    # this is going to check of the patient is done with every service they wanted
    # don't need this though, but it would be nice to know (just in case?)
    if check_if_finished_three == 3:
        print(f"This patient is finished -> {patient}")

    print("ok")


def scraper():
    """Scrapes all the information from {service}.txt files||||| This is the only function for linewindow"""
    global dent_line_mark
    global ment_line_mark
    global orient_line_mark
    services = ['Dental', "Mental", "Oriental"]

    for service in services:
        with open(os.path.join("Lines", f"{service}.txt")) as file:
            new_patient_line = file.read()
            new_patient_list = new_patient_line.split()
            new_patient_str = '\n'.join(new_patient_list)
            if service == "Dental":
                dent_line_mark.set(new_patient_str)
            elif service == 'Mental':
                ment_line_mark.set(new_patient_str)
            elif service == "Oriental":
                orient_line_mark.set(new_patient_str)


################# UI #####################
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
manager_win = ctk.CTk()
manager_win.title("Health Expo")
manager_win.geometry("1200x500")
# below is making the app resizeable
manager_win.resizable(True, True)
# True -> Width, True-> Height

# sc_frame variables
confirm_checked = ctk.BooleanVar()
line_to_be_edited = ctk.StringVar()

# log_frame variables
dental_checked = ctk.BooleanVar()
mental_checked = ctk.BooleanVar()
oriental_checked = ctk.BooleanVar()
counter_tick_up = ctk.IntVar()

# These variables are for the Line Window
dent_line_mark = ctk.StringVar()
ment_line_mark = ctk.StringVar()
orient_line_mark = ctk.StringVar()

my_notebook = ttk.Notebook(manager_win, width=1700, height=704)
my_notebook.grid()

log_frame = ctk.CTkFrame(master=my_notebook, width=1700, height=500)
sc_frame = ctk.CTkFrame(master=my_notebook, width=500, height=500)

# log configs
log_frame.pack(fill=BOTH, expand=0)
my_notebook.add(log_frame, text="LOG")

name_label = ctk.CTkLabel(log_frame, text="Name", font=FONT)
name_label.grid(column=0, row=0, sticky=EW)
name_label.configure(pady=20)
phone_label = ctk.CTkLabel(log_frame, text="Phone #", font=FONT)
phone_label.grid(column=0, row=2, sticky=EW)
phone_label.configure(pady=20)
address_label = ctk.CTkLabel(log_frame, text="Address", font=FONT)
address_label.grid(column=0, row=4, sticky=EW)
address_label.configure(pady=20)

name_entry = ctk.CTkEntry(log_frame, fg_color=color2, text_color = BLACK, font=FONT)
name_entry.grid(column=0, row=1, sticky=EW)
phone_entry = ctk.CTkEntry(log_frame, fg_color=color2, text_color = BLACK, font=FONT)
phone_entry.grid(column=0, row=3, sticky=EW)
address_entry = ctk.CTkEntry(log_frame, fg_color=color2, text_color = BLACK, font=FONT)
address_entry.grid(column=0, row=5, sticky=EW)

# right side of log tab
dental_button = ctk.CTkCheckBox(log_frame, text="Dental", variable=dental_checked, font=FONT)
dental_button.grid(column=1, row=1, sticky=E)
mental_button = ctk.CTkCheckBox(log_frame, text="Mental", variable=mental_checked, font=FONT)
mental_button.grid(column=1, row=3, sticky=E)
oriental_button = ctk.CTkCheckBox(log_frame, text="Oriental", variable=oriental_checked, font=FONT)
oriental_button.grid(column=1, row=5, sticky=E)

counter_label = ctk.CTkLabel(log_frame, text=patient_num_assign, font=FONT)
counter_label.grid(column=1, row=6)
counter_label.configure(pady=20)

deploy_line_win_button = ctk.CTkButton(sc_frame, text="Line Window", command=deploy_line_window, font=FONT)
deploy_line_win_button.grid(column=1, row=7, sticky="ES")

log_submit_button = ctk.CTkButton(log_frame, text="Submit", command=log_info_format, font=FONT, height=40)
# add teh command for this button
log_submit_button.grid(column=1, row=7)

############### sc configs #########
sc_frame.pack(fill=BOTH, expand=1)
my_notebook.add(sc_frame, text="Status Change")

patient_num_label = ctk.CTkLabel(sc_frame, text="Patient Num", font=FONT)
patient_num_label.grid(column=0, row=0)

to_be_SC_entry = ctk.CTkEntry(sc_frame, font=FONT)
to_be_SC_entry.grid(column=0, row=1)

key_entry = ctk.CTkEntry(sc_frame, font=FONT)
key_entry.grid(column=0, row=2)

confirm_button = ctk.CTkCheckBox(sc_frame, text="Confirm", variable=confirm_checked, font=FONT)
confirm_button.grid(column=0, row=3)

sc_submit_button = ctk.CTkButton(sc_frame, text="Submit", command=kick_out_plus_lw, font=FONT)
sc_submit_button.grid(column=0, row=4)

sc_dental_button = ctk.CTkRadioButton(sc_frame, text="Dental", variable=line_to_be_edited, value='dental', font=FONT)
sc_dental_button.grid(column=1, row=0)
sc_mental_button = ctk.CTkRadioButton(sc_frame, text="Mental", variable=line_to_be_edited, value='mental', font=FONT)
sc_mental_button.grid(column=1, row=1)
sc_oriental_button = ctk.CTkRadioButton(sc_frame, text="Oriental", variable=line_to_be_edited, value='oriental', font=FONT)
sc_oriental_button.grid(column=1, row=2)

testing_bot()

manager_win.mainloop()
