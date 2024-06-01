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
BIG_FONT = ("Helvetica", 55)
MID_FONT = ("Helvetica", 25)
LINE_FONT = ("Helvetica", 20)

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

        # These variables are for the Line Window
        self.dent_line_text = ctk.StringVar()
        self.eye_line_text = ctk.StringVar()
        self.oriental_line_text = ctk.StringVar()
        self.internal_line_text = ctk.StringVar()
        self.fm_line_text = ctk.StringVar()

        self.lines = [self.dental_line, self.eye_line, self.oriental_line, self.internal_line, self.fm_line]
        self.texts = [self.dent_line_text, self.eye_line_text, self.oriental_line_text, self.internal_line_text, self.fm_line_text]
 
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
            lw = ctk.CTkToplevel()
            lw.title("Line Window")
            lw.iconbitmap(True, self.icon_photo)
            lw.geometry("920x500")

            dental_scrollframe = ctk.CTkScrollableFrame(lw, width=160, height=250, label_text="Dental", label_font=LINE_FONT)
            dental_scrollframe.grid(column=0, row=0, padx=20, pady=20)
            eye_scrollframe = ctk.CTkScrollableFrame(lw, width=160, height=250, label_text="Eye", label_font=LINE_FONT)
            eye_scrollframe.grid(column=1, row=0, padx=20, pady=20, sticky=W)
            oriental_scrollframe = ctk.CTkScrollableFrame(lw, width=160, height=250, label_text="Oriental", label_font=LINE_FONT)
            oriental_scrollframe.grid(column=2, row=0, padx=20, pady=20, sticky=W)
            internal_scrollframe = ctk.CTkScrollableFrame(lw, width=160, height=250, label_text="Internal", label_font=LINE_FONT)
            internal_scrollframe.grid(column=0, row=1, padx=20, pady=20)
            fm_scrollframe = ctk.CTkScrollableFrame(lw, width=160, height=250, label_text="Foot Massage", label_font=LINE_FONT)
            fm_scrollframe.grid(column=1, row=1, padx=20, pady=20)

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
            dental_line = ctk.CTkLabel(dental_scrollframe, textvariable=self.dent_line_text, font=LINE_FONT)
            dental_line.grid(column=1, row=0, sticky="N", padx=50)

            eye_line = ctk.CTkLabel(eye_scrollframe, textvariable=self.eye_line_text, font=MID_FONT)
            eye_line.grid(column=1, row=0, sticky="N", padx=50)

            oriental_line = ctk.CTkLabel(oriental_scrollframe, textvariable=self.oriental_line_text, font=LINE_FONT)
            oriental_line.grid(column=1, row=0, sticky="N", padx=50)

            # BOTTOM ROW
            internal_line = ctk.CTkLabel(internal_scrollframe, textvariable=self.internal_line_text, font=LINE_FONT)
            internal_line.grid(column=1, row=0, sticky="N", padx=50)

            fm_line = ctk.CTkLabel(fm_scrollframe, textvariable=self.fm_line_text, font=LINE_FONT)
            fm_line.grid(column=1, row=0, sticky="N", padx=50)

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

            self.liner(new_patient, self.patient_num_assign)
            self.record(new_patient)
            # update line window to have new patient included in lines
            # self.deploy_line_window()

            # Counter on the UI
            self.patient_num_assign += 1
            self.counter_label.configure(text=self.patient_num_assign)
            self.clear_inputs()

            self.testing_bot()

    def liner(self, new_patient, id):
        """Puts ID's in line"""
        sorted_services = self.sort_the_lines()

        for service in sorted_services:
            # service is a service in string form
            if new_patient[service] == 1:
                match service:
                    # case {service}:
                    #   put id in line, sort it

                    case "Dental":
                        self.dental_line.append(id)
                        sliced_list = self.dental_line[1::]
                        sliced_list.sort()
                        sliced_list.insert(0, self.dental_line[0])
                        self.dent_line_text.set("\n".join(map(self.stringify, sliced_list)))
                    case "Oriental":
                        self.oriental_line.append(id)
                        sliced_list = self.oriental_line[1::]
                        sliced_list.sort()
                        sliced_list.insert(0, self.oriental_line[0])
                        self.oriental_line_text.set("\n".join(map(self.stringify, sliced_list)))

                    case "Eye":
                        self.eye_line.append(id)
                        sliced_list = self.eye_line[1::]
                        sliced_list.sort()
                        sliced_list.insert(0, self.eye_line[0])
                        self.eye_line_text.set("\n".join(map(self.stringify, sliced_list)))
                    case "Internal":
                        self.internal_line.append(id)
                        sliced_list = self.internal_line[1::]
                        sliced_list.sort()
                        sliced_list.insert(0, self.internal_line[0])
                        self.internal_line_text.set("\n".join(map(self.stringify, sliced_list)))

                    case "Fm":
                        self.fm_line.append(id)
                        sliced_list = self.fm_line[1::]
                        sliced_list.sort()
                        sliced_list.insert(0, self.fm_line[0])
                        self.fm_line_text.set("\n".join(map(self.stringify, sliced_list)))

                # mark that service so we don't run into it again in self.re_enter()
                new_patient[service] = 0
                break
            else:
                print('found no match')  

    def stringify(self, num):
        return str(num)

    def record(self, new_patient):
        '''Puts patients in line, records information into csv'''

        record_patients_data = pandas.read_csv(os.path.join("Amherst", "Databases", "record_patients.csv"))
        new_data = pandas.DataFrame(new_patient, index=[0])
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


    def tick_counter(self):
        

        with open(os.path.join("Amherst", "Lines", "index.txt"), mode='w') as back_in_index:
            back_in_index.write(str(self.patient_num_assign))


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