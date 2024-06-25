from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import ImageTk, Image
from copy import deepcopy

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
BIG_FONT = ("Helvetica", 55)
MID_FONT = ("Helvetica", 32)
LINE_FONT = ("Helvetica", 20)
INSTR_FONT = ("Helvetica", 15)

NUM_OF_FM_SERVERS = 4

# for audio
mixer.init()

the_key = "key"

class HealthExpo():
    def __init__(self):
        self.first_time = True
        with open(os.path.join("Amherst", "Lines", "index.txt")) as assign_index:
            self.patient_num_assign = int(assign_index.read())

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
        self.is_appointmented = ctk.BooleanVar()

        # These variables are for the Line Window
        self.dental_line_text = ctk.StringVar()
        self.eye_line_text = ctk.StringVar()
        self.oriental_line_text = ctk.StringVar()
        self.internal_line_text = ctk.StringVar()
        self.fm_line_text = ctk.StringVar()

        self.patients = {
            # dict of patients
        }

        self.recover()

        self.service_to_line_info = {
            # string: [line, line_text]
            "Dental": [self.dental_line, self.dental_line_text],
            "Eye": [self.eye_line, self.eye_line_text],
            "Oriental": [self.oriental_line, self.oriental_line_text],
            "Internal": [self.internal_line, self.internal_line_text],
            "Fm": [self.fm_line, self.fm_line_text]
        }

        self.lines = [self.dental_line, self.eye_line, self.oriental_line, self.internal_line, self.fm_line]
        self.texts = [self.dental_line_text, self.eye_line_text, self.oriental_line_text, self.internal_line_text, self.fm_line_text]
 
        tabs = ctk.CTkTabview(master=self.home, width=700)
        tabs.grid()
        tabs.add("Log")
        tabs.add("Status Change")
        tabs.add("Reset")
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

        self.appointment_button = ctk.CTkCheckBox(master=log_tab, text="Appointment", variable=self.is_appointmented, font=FONT)
        self.appointment_button.grid(column=0, row=6)

        self.counter_label = ctk.CTkLabel(master=log_tab, text=self.patient_num_assign, font=BIG_FONT)
        self.counter_label.grid(column=1, row=6, pady=40)

        self.log_submit_button = ctk.CTkButton(master=log_tab, text="Submit", command=self.log_info_format, font=FONT, height=40)
        # add teh command for this button
        self.log_submit_button.grid(column=2, row=6)

        #               SC configs                #
        self.SC_tab = tabs.tab("Status Change")

        self.deploy_line_win_button = ctk.CTkButton(master=self.SC_tab, text="Line Window", command=self.deploy_line_window, font=FONT)
        self.deploy_line_win_button.grid(column=3, row=7, sticky="ES")

        self.patient_num_label = ctk.CTkLabel(master=self.SC_tab, text="Patient Num", font=FONT)
        self.patient_num_label.grid(column=0, row=0, padx=(120, 30), sticky=S)

        self.to_be_SC_entry = ctk.CTkEntry(master=self.SC_tab, font=FONT)
        self.to_be_SC_entry.grid(column=0, row=1, padx=(120, 30), sticky=N)

        self.confirm_button = ctk.CTkCheckBox(master=self.SC_tab, text="Confirm", variable=self.confirm_checked, font=FONT)
        self.confirm_button.grid(column=0, row=2, padx=(120, 30))

        self.sc_submit_button = ctk.CTkButton(master=self.SC_tab, text="Submit", command=self.kick_out, font=FONT)
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

        ################ for reset tab ############### 
        self.reset_tab = tabs.tab("Reset")
        self.reset_button = ctk.CTkButton(self.reset_tab, text="RESET", command=self.reset, font=FONT)
        self.reset_button.grid(column=0, row=0)   # intentionally put in corner to prevent mistake clicks

        self.testing_bot()
        # self.home.after(2000, self.scan_plugin)
        self.home.mainloop()
        
        self.save_changes(self.patients, self.lines)

    ################# FUNCTIONALITY ##################

    def testing_bot(self):
        """Just for testing purposes, comment out this method when in production"""
        rand_name = random.choice(['John', 'Mary', 'Jerry', 'James', 'Matthew', 'Mark', 'Luke', 'John', 'Daniel', 'Ezekiel',
                                'Esther', 'Melchizideck', 'Solomon', 'David', 'Moses', 'Jacob', 'Esau', 'Joseph',
                                'Marvin', 'Melvin', 'Kyle', 'Kendell', 'Ava', 'Amanda', 'Archie', 'Bo', 'Bob', 'Braden',
                                'Brantley', 'Carter', 'Cam', 'Carly'])

        self.name_entry.insert(0, rand_name)


    def reset(self):
        if messagebox.askquestion("Resetting Data", "Do you really want to reset this session's patient data?"):
            for filename in ["Eye.txt", "Dental.txt", "Fm.txt", "Internal.txt", "Oriental.txt"]:
                open(os.path.join("Amherst", "Lines", filename), "w").close()
            with open(os.path.join("Amherst", "Lines","index.txt"), "w") as file:
                file.write("101")

            # PROBLEM WITH OS.LISTDIR    
            # for filename in os.listdir(os.path.join("Amherst", "Lines")):
            #     print("here we go")
            #     print(filename)
            # for filename in os.listdir(os.path.join("Amherst", "Lines")):
            #     with open(filename) as file:
            #         if filename == "index.txt":
            #             file.write("101")
            #         else:
            #             file.write("")

        with open(os.path.join("Amherst", "Databases", "patients.json"), "w") as file:
            json.dump({
            "0": {
                "id": 0,
                "name": "dummyPatient",
                "Dental": 1,
                "Eye": 1,
                "Oriental": 0,
                "Internal": 0,
                "Fm": 1,
                "appointment": 0
            }
            }, file)

        # won't clear csv data, since that is for the record, not the program

        self.dental_line.clear()
        self.oriental_line.clear()
        self.eye_line.clear()
        self.fm_line.clear()
        self.internal_line.clear()
        self.patients.clear()

    # def scan_plugin(self):
    #     with open(os.path.join("Amherst", "plugin.txt")) as file:
    #         ids = [int(i.strip()) for i in file.readlines()]
    #         for to_be_kicked in ids:
    #             print("Lets boot")
    #             self.seek_kick(to_be_kicked)
    #     self.home.after(2000, self.scan_plugin)

    # def seek_kick(self, to_be_kicked):
    #     for line in self.lines:
    #         for id in line:
    #             if id == to_be_kicked:
    #                 line.remove(id)
    #                 self.liner(self.patients[id], id)
    #                 print('kicked')
    #                 break

    def deploy_line_window(self):
            lw = ctk.CTkToplevel()
            lw.title("Line Window")
            lw.iconbitmap(True, self.icon_photo)
            lw.geometry("920x500")

            dental_scrollframe = ctk.CTkScrollableFrame(lw, width=200, height=250, label_text="Dental/치과", label_font=LINE_FONT)
            dental_scrollframe.grid(column=0, row=0, padx=20, pady=20)
            eye_scrollframe = ctk.CTkScrollableFrame(lw, width=200, height=250, label_text="Eye/안과", label_font=LINE_FONT)
            eye_scrollframe.grid(column=1, row=0, padx=20, pady=20, sticky=W)
            oriental_scrollframe = ctk.CTkScrollableFrame(lw, width=200, height=250, label_text="Oriental/한방", label_font=LINE_FONT)
            oriental_scrollframe.grid(column=2, row=0, padx=20, pady=20, sticky=W)
            internal_scrollframe = ctk.CTkScrollableFrame(lw, width=200, height=250, label_text="Internal/내과", label_font=LINE_FONT)
            internal_scrollframe.grid(column=0, row=1, padx=20, pady=20)
            fm_scrollframe = ctk.CTkScrollableFrame(lw, width=200, height=250, label_text="Foot Massage/발마사지", label_font=LINE_FONT)
            fm_scrollframe.grid(column=1, row=1, padx=20, pady=20)

            instructions = ctk.CTkLabel(master=lw, text="1. First in line should head\n to the designated office.\n2. Once finished, come to the signup desk\n3. A ringtone will signify\na change to the lines", font=INSTR_FONT)
            instructions.grid(column=2, row=1, padx=8, pady=8, sticky="W")

            my_img_files = ["dental.png", "eye.png", "oriental.png", "internal.png", "foot.png"]
            my_scrollframes = [dental_scrollframe, eye_scrollframe, oriental_scrollframe, internal_scrollframe, fm_scrollframe]
            for i in range(0, len(my_img_files)):
                file_name = my_img_files[i]
                frame = my_scrollframes[i]
                path = os.path.join("Amherst", "Assets", file_name)
                img = ctk.CTkImage(light_image=Image.open(path),
                                dark_image=Image.open(path),
                                size=(60, 60)
                                )
                img_label = ctk.CTkLabel(frame, text="", image=img)
                img_label.grid(column=0, row=0, sticky=N)

            # TOP ROW
            dental_line = ctk.CTkLabel(dental_scrollframe, textvariable=self.dental_line_text, font=MID_FONT)
            dental_line.grid(column=1, row=0, sticky="N", padx=30)

            eye_line = ctk.CTkLabel(eye_scrollframe, textvariable=self.eye_line_text, font=MID_FONT)
            eye_line.grid(column=1, row=0, sticky="N", padx=30)

            oriental_line = ctk.CTkLabel(oriental_scrollframe, textvariable=self.oriental_line_text, font=MID_FONT)
            oriental_line.grid(column=1, row=0, sticky="N", padx=30)

            # BOTTOM ROW
            internal_line = ctk.CTkLabel(internal_scrollframe, textvariable=self.internal_line_text, font=MID_FONT)
            internal_line.grid(column=1, row=0, sticky="N", padx=30)

            fm_line = ctk.CTkLabel(fm_scrollframe, textvariable=self.fm_line_text, font=MID_FONT)
            fm_line.grid(column=1, row=0, sticky="N", padx=30)

            lw.mainloop()

    def log_info_format(self):
        """verify inputs of log_tab, formats it"""
        if self.name_entry.get() == "":
            messagebox.showwarning(title="Empty Entries", message="Looks like you have not filled out the name entry")

        elif not self.dental_checked.get() and not self.eye_checked.get() and not self.oriental_checked.get() and not self.internal_checked.get() and not self.fm_checked.get():
            messagebox.showwarning(title="Empty Services", message="Looks like you have not filled out any Services")

        else:
            new_patient = {
                "id": self.patient_num_assign,
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

            if self.is_appointmented.get():
                new_patient["appointment"] = 1
            else:
                new_patient["appointment"] = 0

            self.record(new_patient)
            self.patients[self.patient_num_assign] = new_patient
            self.liner(new_patient, self.patient_num_assign)

            # Counter on the UI
            self.patient_num_assign += 1
            self.counter_label.configure(text=self.patient_num_assign)
            self.clear_inputs()

            self.testing_bot()

    def liner(self, new_patient, id):
        """Puts ID's in line"""
        sorted_services = self.sort_the_lines()
        for service in sorted_services:
            line = self.service_to_line_info[service][0]
            text = self.service_to_line_info[service][1]
            # service is a service in string form
            if new_patient[service] == 1:
                # for appointments, they should go second all the time, no matter what
                if new_patient["appointment"] == 1:
                    # for loop through dictionary, until we find person who is NOT appointmented, then enter there
                    if len(line) <= 1:
                        line.append(id)
                    else:
                        line.insert(1, id)

                    if service != "Fm":
                        text.set("\n".join(map(self.stringify, line)))
                    else:
                        self.render_fm()
                # not for appointments
                else:
                    # I present to you, the ASBAL algorithsm
                    # stands for Add (new patient ID) Sort Back (sort everything after first ID) Add Lead (add the previously first ID at the front)
                    line.append(id)
                    sliced_list = line[1::]
                    sliced_list.sort()
                    sliced_list.insert(0, line[0])
                    if service != "Fm":
                        text.set("\n".join(map(self.stringify, sliced_list)))
                    else:
                        self.render_fm()

                # mark that service so we don't place them there again
                new_patient[service] = 0
                break
            else:
                print('found no match')

    def stringify(self, num):
        return str(num)

    def intify(self, a_str):
        return int(a_str)
    
    def render_fm(self):
        final_text = ""
        for i in range(0, len(self.fm_line)):
            if i == NUM_OF_FM_SERVERS:
                final_text += f"\n{self.fm_line[i]}"
            else:
                final_text += f"{self.fm_line[i]}\n"
        self.fm_line_text.set(final_text)

    def save_changes(self, patients: dict, lines: list):
        # save next index number
        with open(os.path.join("Amherst", "Lines", "index.txt"), "w") as assign_index:
            assign_index.write(str(self.patient_num_assign))

        # put into json (to be accessed again for recovery)
        with open(os.path.join("Amherst", "Databases", "patients.json")) as file:
            data = json.load(file)
        data.update(patients)
        with open(os.path.join("Amherst", "Databases", "patients.json"), 'w') as file:
            json.dump(data, file, indent=3)

        # write to each service file
        files = ["Dental", "Eye", "Fm", "Internal", "Oriental"]
        for service in files:
            with open(os.path.join("Amherst", "Lines", f"{service}.txt"), "w") as f:
                f.write("\n".join(map(self.stringify, self.service_to_line_info[service][0])))

    def record(self, new_patient):
        '''Records information into csv'''
        # put into csv
        for_csv_patient = deepcopy(new_patient)
        for k, v in for_csv_patient.items():
            for_csv_patient[k] = [v] # listifying everything to put in csv

        record_patients_data = pandas.read_csv(os.path.join("Amherst", "Databases", "record_patients.csv"))
        new_data = pandas.DataFrame(for_csv_patient)
        modified_data = pandas.concat([record_patients_data, new_data], ignore_index=True, join="inner")
        modified_data.to_csv(os.path.join("Amherst", "Databases", "record_patients.csv"), index=False)

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
        for k, v in lengths.items():
            if v >= biggest:
                sorted_list.insert(0, k)
                biggest = v
            else:
                sorted_list.append(k)
        
        sorted_list.reverse()
        return sorted_list # which has the shortest line first, longest line last


    def write_in_a_file(service, patient_num):
        with open(os.path.join("Amherst", "Lines", f"{service}.txt"), 'a') as file:
            file.write(str(patient_num) + ' ')


    def clear_inputs(self):
        # clear the text edits
        self.name_entry.delete(0, END)

        # clear the checkboxes
        self.dental_button.deselect()
        self.eye_button.deselect()
        self.oriental_button.deselect()
        self.eye_button.deselect()
        self.fm_button.deselect()
        self.internal_button.deselect()

        # for the SC
        self.confirm_button.deselect()
        self.to_be_SC_entry.delete(0, END)


############## UPDATES FOR NEXT YEAR #################
    # def intercept():
    #     """Used for people with appointments"""

    # def emergency_out(self):
    #     remove(index) from a service


    def kick_out(self):
        '''takes the first one in a specified line out'''
        if self.confirm_checked.get():
            edit_line = self.line_to_be_edited.get()

            # authenticate ID typed in
            try:
                entry_ID = int(self.to_be_SC_entry.get())
            except ValueError:
                messagebox.showwarning(title="Number Entry", message="Looks like you have put a letter in the number box where you type in the id. It should not have a letter, only numbers.")
            else:
                # just make sure they chose a line
                if edit_line not in ["dental", "eye", "oriental", "internal", "fm"]:
                    messagebox.showwarning(title="Choose a line", message="It looks like you did not choose a line to take out of.")
                else:
                    show_warning = False
                    match edit_line:
                        case "dental":
                            if len(self.dental_line) == 0 or entry_ID != self.dental_line[0]:
                                    show_warning = True
                            else:
                                del self.dental_line[0]
                        case "oriental":
                            if len(self.oriental_line) == 0 or entry_ID != self.oriental_line[0]:
                                    show_warning = True
                            else:
                                del self.oriental_line[0]
                        case "eye":
                            if len(self.eye_line) == 0 or entry_ID != self.eye_line[0]:
                                    show_warning = True
                            else:
                                del self.eye_line[0]
                        case "internal":
                            if len(self.internal_line) == 0 or entry_ID != self.internal_line[0]:
                                    show_warning = True
                            else:
                                del self.internal_line[0]
                        case "fm":
                            if len(self.fm_line) == 0 or entry_ID not in self.fm_line:
                                show_warning = True
                            else:
                                self.fm_line.remove(entry_ID)
                                
                    if show_warning:
                        messagebox.showwarning(title="Number match", message="Either:\n     The ID you put in does not match the first ID in the line you chose\n     The line you chose is empty")
                    else:
                        print("__________________ We made it ______________")
                        
                        # re-render the line where ID was taken OUT of
                        match edit_line:
                            case "dental":
                                self.dental_line_text.set("\n".join(map(self.stringify, self.dental_line)))
                            case "eye":
                                self.eye_line_text.set("\n".join(map(self.stringify, self.eye_line)))
                            case "oriental":
                                self.oriental_line_text.set("\n".join(map(self.stringify, self.oriental_line)))
                            case "internal":
                                self.internal_line_text.set("\n".join(map(self.stringify, self.internal_line)))
                            case "fm":
                                self.render_fm()

                        self.liner(self.patients[entry_ID], entry_ID)

                        mixer.music.load(os.path.join("Amherst", "Assets", "notification_sound2.mp3"))
                        mixer.music.play(loops=0)
        else:
            messagebox.showwarning(title="Confirm Your Choice", message="Please check the confirm button to confirm your removal.")

    def recover(self):
        """Scrapes all the information from {service}.txt files, puts into lines (the lists)"""
        print("I'm recovering")
        # load from json
        with open(os.path.join("Amherst", "Databases", "patients.json")) as file:
            raw_dict = json.load(file)
            for k, v in raw_dict.items():
                self.patients[int(k)] = v

        # load from individual lines
        files = ["Dental", "Eye", "Fm", "Internal", "Oriental"]
        for service in files:
            with open(os.path.join("Amherst", "Lines", f"{service}.txt")) as f:
                raw_data = f.read()
                print(raw_data.split("\n"))
                if raw_data != "":
                    int_list = list(map(self.intify, raw_data.split("\n")))

                    match service:
                        case "Dental":
                            self.dental_line = int_list
                            self.dental_line_text.set(raw_data)
                        case "Eye":
                            self.eye_line = int_list
                            self.eye_line_text.set(raw_data)
                        case "Fm":
                            self.fm_line = int_list
                            self.render_fm()
                        case "Internal":
                            self.internal_line = int_list
                            self.internal_line_text.set(raw_data)
                        case "Oriental":
                            self.oriental_line = int_list
                            self.oriental_line_text.set(raw_data)

if __name__=='__main__':
    HealthExpo()