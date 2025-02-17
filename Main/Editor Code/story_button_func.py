# Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import id
import os
import editor_settings
import test_buttons_func


def style_func():
    s_font_size = 11
    s_style = ttk.Style()
    s_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', s_font_size))
    s_style.configure("TButton", font=('Times New Roman', s_font_size))
    s_style.configure("TLabel", font=('Times New Roman', s_font_size))


# Function to save new stories
def s_new_save():
    # Create a connection to the database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS stories
    (s_id text, 
    s_text text,
    ch_id text)""")

    # Script to create a new story number and to replace a number if a story has been deleted
    c.execute("""SELECT s_id FROM stories ORDER BY s_id""")
    s_new_s_id_list_raw = c.fetchall()
    s_new_s_id_list = id.raw_conv(s_new_s_id_list_raw)

    if s_new_s_id_list:
        s_id_number_list = []
        for s_id in s_new_s_id_list:
            s_id_number_list.append(int(id.id_int(s_id)))

        s_new_s_id_num_max = int(id.max_num(s_id_number_list))

        s_id_number_real_list = []
        for number in range(1, s_new_s_id_num_max + 1):
            s_id_number_real_list.append(number)

        s_id_missing_numbers_list = []
        for number in s_id_number_real_list:
            if number not in s_id_number_list:
                s_id_missing_numbers_list.append(number)

        if s_id_missing_numbers_list:
            s_new_new_p_id = s_id_missing_numbers_list[0]
        else:
            s_new_new_p_id = int(s_new_s_id_num_max) + 1
    else:
        s_new_new_p_id = 1

    # ----------------------------------------

    # Get c_id from character_name
    s_new_ch_name = s_new_ch_name_variable.get()
    c.execute(f"""SELECT ch_id FROM characters WHERE ch_name = '{s_new_ch_name}'""")
    s_new_ch_id_raw = c.fetchall()
    s_new_ch_id = id.raw_conv(s_new_ch_id_raw)[0]

    # Check text length for error
    s_new_text_length = len(s_new_beginning_story_entry.get("1.0", "end"))

    if s_new_text_length != 1:
        c.execute(
            "INSERT INTO stories VALUES (:s_id, :s_text, :ch_id)",
            {
                "s_id": f"{id.s_id(s_new_new_p_id)}",
                "s_text": str(s_new_beginning_story_entry.get("1.0", "end")),
                "ch_id": f"{s_new_ch_id}"
            })
        # Show Success pop-up
        messagebox.showinfo("Success",
                            f"Story Number {s_new_new_p_id} has been created and Character Called '{s_new_ch_name}' has been assigned to it.")
        s_new_beginning_story_entry.delete("1.0", "end")
    else:
        messagebox.showerror("Input Error", "Story Text Is Empty", icon='warning')

    conn.commit()

    s_new_beginning_story_entry.delete("1.0", "end")

    s_new_ch_id_opt_menu()


# Function for new story window
def s_new_window():
    style_func()
    global s_new_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    s_new_wd = Toplevel()
    path = os.path.dirname(__file__)
    s_new_wd.iconbitmap(f'{path}/Illustrations/Icon/editor_icon_2.ico')
    s_new_wd.grab_set()
    s_new_wd.title("Create A New Story")
    screen_x_2 = s_new_wd.winfo_screenwidth()
    screen_y_2 = s_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 545
    s_new_wd.minsize(window_x_2, window_y_2)
    s_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    s_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Info Frame 1
    s_new_info_frame_1 = LabelFrame(s_new_wd, height=window_y_2, width=window_x_2)
    s_new_info_frame_1.pack(fill="both", expand=True)

    s_new_button_frame = LabelFrame(s_new_wd, height=window_y_2, width=window_x_2)
    s_new_button_frame.pack(fill="both")

    s_new_entry_width = 37
    s_new_width = 21
    s_new_pad = 10
    # Labels
    s_new_story_id_label = ttk.Label(s_new_info_frame_1, text="Select Character Who\n Will Play This Story:", width=s_new_width, anchor=W)
    s_new_story_id_label.grid(row=0, column=0, padx=(s_new_pad, s_new_pad+9), pady=s_new_pad, stick="w")

    s_new_beginning_label = ttk.Label(s_new_info_frame_1, text="Beginning Text:", width=s_new_width, anchor=NW)
    s_new_beginning_label.grid(row=1, column=0, padx=(s_new_pad, s_new_pad+3), pady=s_new_pad, stick="nw")

    # Entries
    global s_new_beginning_story_entry
    s_new_beginning_story_entry = Text(s_new_info_frame_1, width=s_new_entry_width)
    s_new_beginning_story_entry.grid(row=1, column=1, padx=s_new_pad, pady=s_new_pad)

    # Buttons
    s_new_button_width = 21
    s_new_save_story_button = ttk.Button(s_new_button_frame, text="Save Story", width=s_new_button_width, command=s_new_save)
    s_new_save_story_button.grid(row=0, column=0, padx=s_new_pad, pady=s_new_pad, stick="w")

    s_new_cancel_button = ttk.Button(s_new_button_frame, text="Cancel", width=s_new_button_width, command=s_new_wd.destroy)
    s_new_cancel_button.grid(row=0, column=1, padx=s_new_pad, pady=s_new_pad, ipadx=70, stick="w")

    global s_new_ch_id_opt_menu

    def s_new_ch_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT ch_id FROM characters EXCEPT SELECT ch_id FROM stories""")
        s_new_ch_id_list_raw = c.fetchall()
        s_new_ch_id_list = id.raw_conv(s_new_ch_id_list_raw)

        s_new_ch_name_list = []
        for ch_id in s_new_ch_id_list:
            c.execute(f"""SELECT ch_name FROM characters WHERE ch_id = '{ch_id}'""")
            s_new_ch_name_list_raw = c.fetchall()
            s_new_ch_name_list_1 = id.raw_conv(s_new_ch_name_list_raw)
            s_new_ch_name_list.append(s_new_ch_name_list_1[0])

        if s_new_ch_name_list:
            global s_new_ch_name_variable
            s_new_ch_name_variable = StringVar()
            s_new_ch_id_opt_menu_var = ttk.OptionMenu(s_new_info_frame_1, s_new_ch_name_variable, s_new_ch_name_list[0], *s_new_ch_name_list)
            s_new_ch_id_opt_menu_var.grid(row=0, column=1, padx=s_new_pad, pady=s_new_pad, stick="ew")

        else:
            s_new_wd.destroy()
            messagebox.showerror("Index Error", "No Available Characters Found")

        conn.commit()

    s_new_ch_id_opt_menu()

    test_buttons_func.error_update()

    s_new_wd.mainloop()


# Function to insert already written text
def s_edt_insert():
    # Delete Previous Input
    s_edt_edit_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    s_edt_s_id = s_edt_s_id_variable.get()

    c.execute(f"""SELECT s_text FROM stories WHERE s_id = '{s_edt_s_id}'""")
    s_edt_text_raw = c.fetchall()
    s_edt_text = ((s_edt_text_raw[0])[0])

    # Input data into text box
    s_edt_edit_text_entry.insert(END, f'{s_edt_text}')

    conn.commit()


# Function to edit stories
def s_edt_edit():
    # Create a connection to the database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Update Table
    s_edt_s_id = s_edt_s_id_variable.get()
    if len(s_edt_edit_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE stories SET s_text = :s_text WHERE s_id = :s_id""",
                  {
                      "s_text": s_edt_edit_text_entry.get("1.0", "end"),
                      "s_id": f'{s_edt_s_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {s_edt_s_id} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Story Text is Empty', icon='warning')

    # Clear the Text Boxes
    s_edt_edit_text_entry.delete("1.0", "end")

    conn.commit()


# Function to delete a story from the delete window
def s_del_delete():
    # Create connection to retrieve data
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()
    s_del_s_id = s_edt_s_id_variable.get()

    s_del_warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete story Number {id.id_int(s_del_s_id)}?', icon='warning')

    if s_del_warning == 'yes':
        c.execute(f"""DELETE FROM stories WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM initial_paragraphs WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM paragraphs_list WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM choices WHERE s_id = '{s_del_s_id}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {id.id_int(s_del_s_id)} has been successfully deleted\nAll Paragraphs And Choices From Story Number {id.id_int(s_del_s_id)} Have Also Been Deleted.")

    conn.commit()

    s_edt_edit_text_entry.delete("1.0", "end")

    s_edt_s_id_opt_menu()


# Function to open edit window
def s_edt_window():
    style_func()
    global s_edt_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    s_edt_wd = Toplevel()
    path = os.path.dirname(__file__)
    s_edt_wd.iconbitmap(f'{path}/Illustrations/Icon/editor_icon_2.ico')
    s_edt_wd.grab_set()
    s_edt_wd.title("Edit A Story")
    screen_x_2 = s_edt_wd.winfo_screenwidth()
    screen_y_2 = s_edt_wd.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 444
    s_edt_wd.minsize(window_x_2, window_y_2)
    s_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    s_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame
    s_edt_info_frame_1 = LabelFrame(s_edt_wd, height=info_frame_height, width=window_x_2)
    s_edt_info_frame_1.pack(fill="both", side=TOP)

    # Buttons Frame
    s_edt_button_frame = LabelFrame(s_edt_wd, height=window_y_2 - frame_height, width=window_x_2)
    s_edt_button_frame.pack(fill="both", side=BOTTOM)

    s_edt_entry_width = 37
    s_edt_width = 42
    s_edt_pad = 10

    # Labels
    s_edt_story_id_label = ttk.Label(s_edt_info_frame_1, text="Select Story ID:", width=int(s_edt_width/2), anchor=W)
    s_edt_story_id_label.grid(row=0, column=0, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_beginning_label = ttk.Label(s_edt_info_frame_1, text="Edit Text:", width=int(s_edt_width/2)-1, anchor=NW)
    s_edt_beginning_label.grid(row=1, column=0, padx=s_edt_pad, pady=s_edt_pad, stick="nw")

    # Text
    global s_edt_edit_text_entry
    s_edt_edit_text_entry = Text(s_edt_info_frame_1, width=s_edt_entry_width, height=20)
    s_edt_edit_text_entry.grid(row=1, column=1, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    # Buttons
    s_edt_width_buttons = 13
    s_edt_save_story_button = ttk.Button(s_edt_button_frame, text="Save Changes", width=s_edt_width_buttons, command=s_edt_edit)
    s_edt_save_story_button.grid(row=0, column=0, padx=(s_edt_pad+3, s_edt_pad), pady=s_edt_pad, stick="w")

    s_edt_load_text_button = ttk.Button(s_edt_button_frame, text="Load Story", width=s_edt_width_buttons, command=s_edt_insert)
    s_edt_load_text_button.grid(row=0, column=1, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_delete_text_button = ttk.Button(s_edt_button_frame, text="Delete Story", width=s_edt_width_buttons, command=s_del_delete)
    s_edt_delete_text_button.grid(row=0, column=2, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_cancel_button = ttk.Button(s_edt_button_frame, text="Cancel", width=s_edt_width_buttons, command=s_edt_wd.destroy)
    s_edt_cancel_button.grid(row=0, column=3, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    global s_edt_s_id_opt_menu

    def s_edt_s_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories ORDER BY s_id""")
        s_edt_s_id_list_raw = c.fetchall()
        s_edt_s_id_list = []
        for tp in s_edt_s_id_list_raw:
            for item in tp:
                s_edt_s_id_list.append(item)

        if s_edt_s_id_list:
            global s_edt_s_id_variable
            s_edt_s_id_variable = StringVar()
            s_edt_s_id_opt_menu_var = ttk.OptionMenu(s_edt_info_frame_1, s_edt_s_id_variable, s_edt_s_id_list[0], *s_edt_s_id_list)
            s_edt_s_id_opt_menu_var.grid(row=0, column=1, padx=s_edt_pad, pady=s_edt_pad, stick="ew")

        else:
            s_edt_wd.destroy()
            messagebox.showerror("Index Error", "No Existing Stories Found")

        conn.commit()

    s_edt_s_id_opt_menu()

    test_buttons_func.error_update()

    s_edt_wd.mainloop()
