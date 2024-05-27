from tkinter import *
from tkinter import messagebox
import customtkinter as ctk

from pygame import mixer
import json
import pandas

import os
import random

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

class HealthExpo():
    def __init__(self):
        self.first_time = True

        #                    UI                 #
        self.home = ctk.CTk()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        self.home.title("Health Expo")
        self.home.geometry("700x375")
        icon_photo = PhotoImage(os.path.join("Assets", "icon.ico"))
        self.home.iconbitmap(True, icon_photo)
        self.home.resizable(True, True)
        # True -> Width, True-> Height

        self.dental_line = []
        self.oriental_line = []
        self.eye_line = []
        self.fm_line = []
        self.internal_line = []

        # sc_frame variables
        self.confirm_checked = ctk.BooleanVar()
        self.line_to_be_edited = ctk.StringVar()

        # log_frame variables (do we even need them as ctk vars?)
        self.dental_checked = ctk.BooleanVar()
        self.eye_checked = ctk.BooleanVar()
        self.oriental_checked = ctk.BooleanVar()
        self.fm_checked = ctk.BooleanVar()
        self.internal_checked = ctk.BooleanVar()
        self.counter_tick_up = ctk.IntVar()

        # These variables are for the Line Window
        self.dent_line_text = ctk.StringVar()
        self.eye_line_text = ctk.StringVar()
        self.oriental_line_text = ctk.StringVar()
        self.internal_line_text = ctk.StringVar()

        tabs = ctk.CTkTabview(master=self.home, width=700)
        tabs.grid()
        tabs.add("Log")
        tabs.add("Status Change")
        tabs.set("Log")
        log_tab = tabs.tab("Log")

        self.name_label = ctk.CTkLabel(master=log_tab, text="Name", font=FONT)
        self.name_label.grid(column=0, row=0, sticky=EW)
        self.name_label.configure(pady = 20)

        self.name_entry = ctk.CTkEntry(master=log_tab, fg_color=color2, text_color = BLACK, font=FONT)
        self.name_entry.grid(column=0, row=1, sticky=EW)

        # choosing services on log tab
        self.dental_button = ctk.CTkCheckBox(master=log_tab, text="Dental", variable=self.dental_checked, font=FONT)
        self.dental_button.grid(column=1, row=1, sticky=E)
        self.eye_button = ctk.CTkCheckBox(master=log_tab, text="Eye", variable=self.eye_checked, font=FONT)
        self.eye_button.grid(column=1, row=3, sticky=E)
        self.oriental_button = ctk.CTkCheckBox(master=log_tab, text="Oriental", variable=self.oriental_checked, font=FONT)
        self.oriental_button.grid(column=1, row=5, sticky=E)
        self.internal_button = ctk.CTkCheckBox(master=log_tab, text="Internal", variable=self.internal_checked, font=FONT)
        self.internal_button.grid(column=1, row=7, sticky=E)
        self.fm_button = ctk.CTkCheckBox(master=log_tab, text="Foot Massage", variable=self.fm_checked, font=FONT)
        self.fm_button.grid(column=1, row=9, sticky=E)

        self.counter_label = ctk.CTkLabel(master=log_tab, text=patient_num_assign, font=FONT)
        self.counter_label.grid(column=1, row=6)
        self.counter_label.configure(pady=20)

        self.log_submit_button = ctk.CTkButton(master=log_tab, text="Submit", command=self.log_info_format, font=FONT, height=40)
        # add teh command for this button
        self.log_submit_button.grid(column=1, row=7)

        #               sc configs                #
        self.SC_tab = tabs.tab("Status Change")

        self.deploy_line_win_button = ctk.CTkButton(master=self.SC_tab, text="Line Window", command=self.deploy_line_window, font=FONT)
        self.deploy_line_win_button.grid(column=2, row=7, sticky="ES")

        self.patient_num_label = ctk.CTkLabel(master=self.SC_tab, text="Patient Num", font=FONT)
        self.patient_num_label.grid(column=0, row=0, padx=(180, 10))

        self.to_be_SC_entry = ctk.CTkEntry(master=self.SC_tab, font=FONT)
        self.to_be_SC_entry.grid(column=0, row=1, padx=(180, 10))

        self.confirm_button = ctk.CTkCheckBox(master=self.SC_tab, text="Confirm", variable=self.confirm_checked, font=FONT)
        self.confirm_button.grid(column=0, row=3, padx=(180, 10), pady=(0, 10))

        self.sc_submit_button = ctk.CTkButton(master=self.SC_tab, text="Submit", command=self.kick_out_plus_lw, font=FONT)
        self.sc_submit_button.grid(column=0, row=4, padx=(180, 10))

        self.padding_text = ctk.CTkLabel(master=self.SC_tab, text="    ", font=FONT)
        self.padding_text.grid(column=1, row=5)

        self.sc_dental_button = ctk.CTkRadioButton(master=self.SC_tab, text="Dental", variable=self.line_to_be_edited, value='dental', font=FONT)
        self.sc_dental_button.grid(column=2, row=0)
        self.sc_eye_button = ctk.CTkRadioButton(master=self.SC_tab, text="Eye", variable=self.line_to_be_edited, value='eye', font=FONT)
        self.sc_eye_button.grid(column=2, row=1)
        self.sc_oriental_button = ctk.CTkRadioButton(master=self.SC_tab, text="Oriental", variable=self.line_to_be_edited, value='oriental', font=FONT)
        self.sc_oriental_button.grid(column=2, row=2)
        self.sc_internal_button = ctk.CTkRadioButton(master=self.SC_tab, text="Oriental", variable=self.line_to_be_edited, value='oriental', font=FONT)
        self.sc_internal_button.grid(column=2, row=3)

        self.testing_bot()

        self.home.mainloop()
    
    ################# FUNCTIONALITY ##################

    def testing_bot(self):
        """Just for testing purposes, comment out this method when in production"""
        rand_name = random.choice(['John', 'Mary', 'Jerry', 'James', 'Matthew', 'Mark', 'Luke', 'John', 'Daniel', 'Ezekiel',
                                'Esther', 'Melchizideck', 'Solomon', 'David', 'Moses', 'Jacob', 'Esau', 'Joseph',
                                'Marvin', 'Melvin', 'Kyle', 'Kendell', 'Ava', 'Amanda', 'Archie', 'Bo', 'Bob', 'Braden',
                                'Brantley', 'Carter', 'Cam', 'Carly'])

        rand_address = random.choice(["afds", "qwer", "a;lsdkfjas;dlfkjas;d", "address road", "james road", "john road",
                                    "brantley road", "Johnathan road", "kingston pike", "Hardin valley", "ava road",
                                    "taylor road", "Oakwood drive", "jamie road", "arkansas road"])

        rand_phone = ''.join([str(num) for num in random.choices(list(range(10)), k=10)])

        self.name_entry.insert(0, rand_name)

    def kick_out_plus_lw(self):
        self.kick_out()
        self.deploy_line_window()


    def deploy_line_window(self):
        global first_time
        self.scraper()
        if first_time:
            first_time = False

            lw = ctk.CTkToplevel()
            lw.title("Line Window")
            lw.iconbitmap(True, self.icon_photo)
            lw.geometry("500x500")

            dental_line = ctk.CTkLabel(lw, textvariable=self.dent_line_text, font=FONT)
            dental_line.grid(column=0, row=1, sticky="N")

            dental_label = ctk.CTkLabel(lw, text="Dental", font=FONT)
            dental_label.grid(column=0, row=0, padx=(60, 60))

            eye_label = ctk.CTkLabel(lw, textvariable=self.eye_line_text, font=FONT)
            eye_label.grid(column=1, row=1, sticky="N")

            eye_label = ctk.CTkLabel(lw, text="Eye", font=FONT)
            eye_label.grid(column=1, row=0, padx=(60, 60))

            oriental_line = ctk.CTkLabel(lw, textvariable=self.oriental_line_text, font=FONT)
            oriental_line.grid(column=2, row=1)

            oriental_label = ctk.CTkLabel(lw, text="Oriental", font=FONT)
            oriental_label.grid(column=2, row=0, padx=(60, 60))

            internal_line = ctk.CTkLabel(lw, textvariable=self.internal_line_text, font=FONT)
            internal_line.grid(column=3, row=1)

            internal_label = ctk.CTkLabel(lw, text="Internal Med", font=FONT)
            internal_label.grid(column=3, row=0, padx=(60, 60))

            fm_line = ctk.CTkLabel(lw, textvariable=self.internal_line_text, font=FONT)
            fm_line.grid(column=4, row=1)

            fm_label = ctk.CTkLabel(lw, text="Internal Med", font=FONT)
            fm_label.grid(column=4, row=0, padx=(60, 60))

            lw.mainloop()


    def log_info_format(self):
        """verify inputs of log_tab, formats it"""
        if self.name_entry.get() == "":
            messagebox.showwarning(title="Empty Entries", message="Looks like you have not filled out the name entry")

        elif not self.dental_checked.get() and not self.eye_checked.get() and not self.oriental_checked.get() and not self.internal_checked.get() and not self.fm_checked.get():
            messagebox.showwarning(title="Empty Services", message="Looks like you have not filled out any Services")

        else:
            new_patient = {
                "id": patient_num_assign,
                "name": self.name_entry.get(),
            }

            # add services here
            if self.dental_checked.get():
                new_patient["Dental"] = 1
            else:
                new_patient["Dental"] = 0

            if self.eye_checked.get():
                new_patient["Eye"] = 1
            else:
                new_patient["Eye"] = 0

            if self.oriental_checked.get():
                new_patient["Oriental"] = 1
            else:
                new_patient["Oriental"] = 0

            if self.internal_checked.get():
                new_patient["Internal"] = 1
            else:
                new_patient["Internal"] = 0
            
            if self.fm_checked.get():
                new_patient["Fm"] = 1
            else:   
                new_patient["Fm"] = 0

            self.liner(new_patient, patient_num_assign)
            self.record(new_patient)
            # update line window to have new patient included in lines
            self.deploy_line_window()

            self.tick_counter()
            self.clear_inputs()

            self.testing_bot()

    def liner(self, new_patient, id):
        sorted_services = self.sort_the_lines()

        for service in sorted_services:
            # service is a service in string form
            if new_patient[service] == 1:
                match service:
                    case "Dental":
                        self.dental_line.append(id)
                    case "Oriental":
                        self.oriental_line.append(id)
                    case "Eye":
                        self.eye_line.append(id)
                    case "Internal":
                        self.internal_line.append(id)
                    case "Fm":
                        self.fm_line.append(id)

                # mark that service so we don't run into it again in self.re_enter()
                new_patient[service] = 0
                break
            else:
                print('found no match')


    def record(self, new_patient):
        '''Puts patients in line, records information into csv, links the patient number to the patient list'''

        record_patients_data = pandas.read_csv(os.path.join("Databases", "record_patients.csv"))
        new_data = pandas.DataFrame(new_patient)
        modified_data = pandas.concat([record_patients_data, new_data], ignore_index=True, join="inner")
        modified_data.to_csv(os.path.join("Databases", "record_patients.csv"), index=False)

        # add this information to the json file (WHY are we adding it to the JSON file?)
        with open(os.path.join("Databases", "patients.json")) as file:
            data = json.load(file)
        data.update(new_patient)
        with open(os.path.join("Databases", "patients.json"), 'w') as file:
            json.dump(data, file, indent=4)


    def sort_the_lines(self):
        """looks at the lengths of each medical line. returns a list of smallest to largest"""
        lengths = {
            "Dental": len(self.dental_line),
            "Oriental": len(self.oriental_line),
            "Eye": len(self.eye_line),
            "Fm": len(self.fm_line),
            "Internal": len(self.internal_line),
        }
        sorted_list = []

        # I'm pretty proud of this one
        biggest = 0
        for k, v in lengths:
            if v >= biggest:
                sorted_list.insert(0, k)
                biggest = v
            else:
                sorted_list.append(k)
        
        sorted_list = sorted_list.reverse()

        return sorted_list # which has the shortest line first, longest line last


    def write_in_a_file(service, patient_num):
        with open(os.path.join("Lines", f"{service}.txt"), 'a') as file:
            file.write(str(patient_num) + ' ')


    def clear_inputs(self):
        # clear the text edits
        self.name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.address_entry.delete(0, END)

        # clear the checkboxes
        self.dental_button.deselect()
        self.eye_button.deselect()
        self.oriental_button.deselect()

        # for the SC
        self.confirm_button.deselect()
        self.to_be_SC_entry.delete(0, END)


    def tick_counter(self):
        # Counter on the UI
        global patient_num_assign
        patient_num_assign += 1
        with open(os.path.join("Lines", "index.txt"), mode='w') as back_in_index:
            back_in_index.write(str(patient_num_assign))
        self.counter_label.configure(text=str(patient_num_assign))


    def kick_out(self):
        '''takes the first one in a specified line out'''

        with open(os.path.join("Lines", f"{self.line_to_be_edited.get()}.txt")) as selected_file:
            data = selected_file.read()
            data = data.split()

        # check if user chose one service to take out of AND check if the number user typed in matches the first in line
        if self.line_to_be_edited.get() != '' and self.to_be_SC_entry.get() == data[0]:

            data.pop(0)

            with open(os.path.join("Lines", f"{self.line_to_be_edited.get()}.txt"), 'w') as update_file:
                ready_to_write = ' '.join(data) + ' '
                update_file.write(ready_to_write)

            self.re_enter(int(self.to_be_SC_entry.get()))

            mixer.music.load(os.path.join("Assets", "notification_sound2.mp3"))
            mixer.music.play(loops=0)

        else:
            messagebox.showwarning(title="Oops", message="It looks like you either:\ndid not choose a service to edit"
                                                        "\nor\nthe number typed in does not match the first in line!")


    def re_enter(self, patient_num):
        """places the patient num back into another line"""

        with open(os.path.join("Databases", "patients.json")) as file:
            patients = json.load(file)

        patient = patients[str(patient_num)]

        sorted_services = self.sort_the_lines()
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

                with open(os.path.join("Lines", f"{service}.txt"), 'w') as file:
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

        # if check_if_finished_three == 3:
        #     print(f"This patient is finished -> {patient}")


    def scraper(self):
        """Scrapes all the information from {service}.txt files, the only function for linewindow"""
        global dental_line
        global internal_line
        global eye_line
        global oriental_line
        global fm_line
        
        services = ['Dental', "Eye", "Oriental"]

        for service in services:
            with open(os.path.join("Lines", f"{service}.txt")) as file:
                new_patient_line = file.read()
                new_patient_list = new_patient_line.split()
                new_patient_str = '\n'.join(new_patient_list)
                if service == "Dental":
                    self.dent_line_text.set(new_patient_str)
                    dental_line = self.dent_line_text.split("\n")
                elif service == 'Eye':
                    self.eye_line_text.set(new_patient_str)
                elif service == "Oriental":
                    self.oriental_line_text.set(new_patient_str)
                elif service == "Internal":
                    self.internal_line_text.set(new_patient_str)

if __name__=='__main__':
    HealthExpo()