from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import ImageTk, Image

from pygame import mixer
import json
import pandas

import os
import random

SILVER = "#F6F6F6"
SKY = "#D6E4F0"
SEA = "#1E56A0"
NAVY = "#163172"
BLACK = "#000505"
FONT = ("Helvetica", 16)
BIG_FONT = ("Helvetica", 65)
MID_FONT = ("Helvetica", 43)
LINE_FONT = ("Helvetica", 33)

with open(os.path.join("Amherst", "Lines", "index.txt")) as assign_index:
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
        # ctk.set_default_color_theme(os.path.join("Amherst", "coast.json"))
        self.home.title("Health Expo")
        self.home.geometry("700x375")
        self.icon_photo = PhotoImage(os.path.join("Amherst", "Assets", "icon.ico"))
        self.home.iconbitmap(default=self.icon_photo)
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
        self.fm_line_text = ctk.StringVar()

        tabs = ctk.CTkTabview(master=self.home, width=700)
        tabs.grid()
        tabs.add("Log")
        tabs.add("Status Change")
        tabs.set("Log")
        log_tab = tabs.tab("Log")

        self.name_label = ctk.CTkLabel(master=log_tab, text="Name", font=FONT)
        self.name_label.grid(column=0, row=0, sticky=EW)
        self.name_label.configure(pady = 20)

        self.name_entry = ctk.CTkEntry(master=log_tab, fg_color=SKY, text_color = BLACK, font=FONT)
        self.name_entry.grid(column=0, row=1, sticky=EW, padx=20)

        # choosing services on log tab
        self.dental_button = ctk.CTkCheckBox(master=log_tab, text="Dental", variable=self.dental_checked, font=FONT)
        self.dental_button.grid(column=1, row=1, sticky=W, padx=40, pady=10)
        self.eye_button = ctk.CTkCheckBox(master=log_tab, text="Eye", variable=self.eye_checked, font=FONT)
        self.eye_button.grid(column=1, row=3, sticky=W, padx=40, pady=10)
        self.oriental_button = ctk.CTkCheckBox(master=log_tab, text="Oriental", variable=self.oriental_checked, font=FONT)
        self.oriental_button.grid(column=1, row=5, sticky=W, padx=40, pady=10)
        self.internal_button = ctk.CTkCheckBox(master=log_tab, text="Internal", variable=self.internal_checked, font=FONT)
        self.internal_button.grid(column=2, row=1, sticky=W, padx=20, pady=10)
        self.fm_button = ctk.CTkCheckBox(master=log_tab, text="Foot Massage", variable=self.fm_checked, font=FONT)
        self.fm_button.grid(column=2, row=3, sticky=W, padx=20, pady=10)

        self.counter_label = ctk.CTkLabel(master=log_tab, text=patient_num_assign, font=BIG_FONT)
        self.counter_label.grid(column=1, row=6)
        self.counter_label.configure(pady=40)

        self.log_submit_button = ctk.CTkButton(master=log_tab, text="Submit", command=self.log_info_format, font=FONT, height=40)
        # add teh command for this button
        self.log_submit_button.grid(column=2, row=6)

        #               SC configs                # BETTER DESIGN?
        self.SC_tab = tabs.tab("Status Change")

        self.deploy_line_win_button = ctk.CTkButton(master=self.SC_tab, text="Line Window", command=self.deploy_line_window, font=FONT)
        self.deploy_line_win_button.grid(column=3, row=7, sticky="ES")

        self.patient_num_label = ctk.CTkLabel(master=self.SC_tab, text="Patient Num", font=FONT)
        self.patient_num_label.grid(column=0, row=0, padx=(120, 30), sticky=S)

        self.to_be_SC_entry = ctk.CTkEntry(master=self.SC_tab, font=FONT)
        self.to_be_SC_entry.grid(column=0, row=1, padx=(120, 30), sticky=N)

        self.confirm_button = ctk.CTkCheckBox(master=self.SC_tab, text="Confirm", variable=self.confirm_checked, font=FONT)
        self.confirm_button.grid(column=0, row=2, padx=(120, 30))

        self.sc_submit_button = ctk.CTkButton(master=self.SC_tab, text="Submit", command=self.kick_out_plus_lw, font=FONT)
        self.sc_submit_button.grid(column=0, row=3, padx=(120, 30))

        self.sc_dental_button = ctk.CTkRadioButton(master=self.SC_tab, text="Dental", variable=self.line_to_be_edited, value='dental', font=FONT)
        self.sc_dental_button.grid(column=2, row=0, padx=20, pady=20, sticky=W)
        self.sc_eye_button = ctk.CTkRadioButton(master=self.SC_tab, text="Eye", variable=self.line_to_be_edited, value='eye', font=FONT)
        self.sc_eye_button.grid(column=2, row=1, padx=20, pady=20, sticky=W)
        self.sc_oriental_button = ctk.CTkRadioButton(master=self.SC_tab, text="Oriental", variable=self.line_to_be_edited, value='oriental', font=FONT)
        self.sc_oriental_button.grid(column=2, row=2, padx=20, pady=20, sticky=W)
        self.sc_internal_button = ctk.CTkRadioButton(master=self.SC_tab, text="Internal", variable=self.line_to_be_edited, value='internal', font=FONT)
        self.sc_internal_button.grid(column=3, row=1, padx=20, pady=20, sticky=W)
        self.sc_fm_buttom = ctk.CTkRadioButton(master=self.SC_tab, text="Foot Massage", variable=self.line_to_be_edited, value='fm', font=FONT)
        self.sc_fm_buttom.grid(column=3, row=0, padx=20, pady=20, sticky=W)

        self.testing_bot()

        self.home.mainloop()
    
    ################# FUNCTIONALITY ##################

    def testing_bot(self):
        """Just for testing purposes, comment out this method when in production"""
        rand_name = random.choice(['John', 'Mary', 'Jerry', 'James', 'Matthew', 'Mark', 'Luke', 'John', 'Daniel', 'Ezekiel',
                                'Esther', 'Melchizideck', 'Solomon', 'David', 'Moses', 'Jacob', 'Esau', 'Joseph',
                                'Marvin', 'Melvin', 'Kyle', 'Kendell', 'Ava', 'Amanda', 'Archie', 'Bo', 'Bob', 'Braden',
                                'Brantley', 'Carter', 'Cam', 'Carly'])

        self.name_entry.insert(0, rand_name)

    def kick_out_plus_lw(self):
        self.kick_out()
        self.deploy_line_window()


    def deploy_line_window(self):
        if self.first_time:
            self.first_time = False

            lw = ctk.CTkToplevel()
            lw.title("Line Window")
            lw.iconbitmap()
            lw.iconbitmap(True, self.icon_photo)
            lw.geometry("920x500")

            my_img_files = ["dental.png", "eye.png", "oriental.png", "internal.png", "foot.png"]
            for i in range(0, len(my_img_files)):
                file_name = my_img_files[i]
                print(file_name)
                img_file = Image.open(os.path.join("Amherst", "Assets", file_name))
                img_file = img_file.resize((100, 100), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img_file)
                img_label = ctk.CTkLabel(lw, text="", image=img)
                img_label.grid(column=i, row=1)

            dental_line = ctk.CTkLabel(lw, textvariable=self.dent_line_text, font=LINE_FONT)
            dental_line.grid(column=0, row=1, sticky="N")

            dental_label = ctk.CTkLabel(lw, text="Dental", font=MID_FONT)
            dental_label.grid(column=0, row=0, padx=(60, 60))

            eye_label = ctk.CTkLabel(lw, textvariable=self.eye_line_text, font=MID_FONT)
            eye_label.grid(column=1, row=1, sticky="N")

            eye_label = ctk.CTkLabel(lw, text="Eye", font=MID_FONT)
            eye_label.grid(column=1, row=0, padx=(60, 60))

            oriental_line = ctk.CTkLabel(lw, textvariable=self.oriental_line_text, font=LINE_FONT)
            oriental_line.grid(column=2, row=1)

            oriental_label = ctk.CTkLabel(lw, text="Oriental", font=MID_FONT)
            oriental_label.grid(column=2, row=0, padx=(60, 60))

            internal_line = ctk.CTkLabel(lw, textvariable=self.internal_line_text, font=LINE_FONT)
            internal_line.grid(column=3, row=1)

            internal_label = ctk.CTkLabel(lw, text="Internal Med", font=MID_FONT)
            internal_label.grid(column=3, row=0, padx=(60, 60))

            fm_line = ctk.CTkLabel(lw, textvariable=self.fm_line_text, font=LINE_FONT)
            fm_line.grid(column=4, row=1)

            fm_label = ctk.CTkLabel(lw, text="Foot Massage", font=MID_FONT)
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

        record_patients_data = pandas.read_csv(os.path.join("Amherst", "Databases", "record_patients.csv"))
        new_data = pandas.DataFrame(new_patient)
        modified_data = pandas.concat([record_patients_data, new_data], ignore_index=True, join="inner")
        modified_data.to_csv(os.path.join("Amherst", "Databases", "record_patients.csv"), index=False)

        # add this information to the json file (WHY are we adding it to the JSON file?)
        with open(os.path.join("Amherst", "Databases", "patients.json")) as file:
            data = json.load(file)
        data.update(new_patient)
        with open(os.path.join("Amherst", "Databases", "patients.json"), 'w') as file:
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
        with open(os.path.join("Amherst", "Lines", f"{service}.txt"), 'a') as file:
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
        with open(os.path.join("Amherst", "Lines", "index.txt"), mode='w') as back_in_index:
            back_in_index.write(str(patient_num_assign))
        self.counter_label.configure(text=str(patient_num_assign))


    def kick_out(self):
        '''takes the first one in a specified line out'''

        with open(os.path.join("Amherst", "Lines", f"{self.line_to_be_edited.get()}.txt")) as selected_file:
            data = selected_file.read()
            data = data.split()

        # check if user chose one service to take out of AND check if the number user typed in matches the first in line
        if self.line_to_be_edited.get() != '' and self.to_be_SC_entry.get() == data[0]:

            data.pop(0)

            with open(os.path.join("Amherst", "Lines", f"{self.line_to_be_edited.get()}.txt"), 'w') as update_file:
                ready_to_write = ' '.join(data) + ' '
                update_file.write(ready_to_write)

            self.re_enter(int(self.to_be_SC_entry.get()))

            mixer.music.load(os.path.join("Amherst", "Assets", "notification_sound2.mp3"))
            mixer.music.play(loops=0)

        else:
            messagebox.showwarning(title="Oops", message="It looks like you either:\ndid not choose a service to edit"
                                                        "\nor\nthe number typed in does not match the first in line!")


    def re_enter(self, patient_num):
        """places the patient num back into another line"""

        with open(os.path.join("Amherst", "Databases", "patients.json")) as file:
            patients = json.load(file)

        patient = patients[str(patient_num)]

        sorted_services = self.sort_the_lines()
        print(patient)

        check_if_finished_three = 0

        for service in sorted_services:
            if service in patient:
                print(f"we found it,{service}, second in that line now")
                with open(os.path.join("Amherst", "Lines", f"{service}.txt")) as file:
                    contents = file.read()
                    xlist = contents.split()
                    xlist.append(str(patient_num))

                    sliced_list = xlist[1::]
                    sliced_list.sort()
                    sliced_list.insert(0, xlist[0])

                with open(os.path.join("Amherst", "Lines", f"{service}.txt"), 'w') as file:
                    ready_to_go = ' '.join(sliced_list) + ' '
                    file.write(ready_to_go)

                the_service_index = patient.index(service)
                patient[the_service_index] = service + 'x'

                # now that we've marked the service as done with an x, we will now update the patients.json
                with open(os.path.join("Amherst", "Databases", "patients.json"), 'w') as file:
                    patients[str(patient_num)] = patient
                    json.dump(patients, file, indent=4)
                break
            else:
                check_if_finished_three += 1

        # if check_if_finished_three == 3:
        #     print(f"This patient is finished -> {patient}")


    def recover(self):
        """Scrapes all the information from {service}.txt files, puts into lines (the lists)"""
        services = ['Dental', "Eye", "Oriental", "Foot_Massage", "Internal"]

        for service in services:
            with open(os.path.join("Amherst", "Lines", f"{service}.txt")) as file:
                patients_line = file.read()
                patients_list = patients_line.split()
                patients_str = '\n'.join(patients_list)

                # update the lists, update the text to be rendered
                match service:
                    case "Dental":
                        self.dent_line_text.set(patients_str)
                        self.dental_line = patients_list
                    case "Eye":
                        self.eye_line_text.set(patients_str)
                        self.eye_line = patients_list
                    case "Oriental":
                        self.oriental_line_text.set(patients_str)
                        self.oriental_line = patients_list
                    case "Internal":
                        self.internal_line_text.set(patients_str)
                        self.internal_line = patients_list
                    case "Foot_Massage":
                        self.fm_line_text.set(patients_str)
                        self.fm_line = patients_list

if __name__=='__main__':
    HealthExpo()