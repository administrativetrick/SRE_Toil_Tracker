import csv
import sqlite3
from datetime import timedelta
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pyperclip

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('toil.db')

# Create table if it doesn't exist
conn.execute('''
    CREATE TABLE IF NOT EXISTS toil_items
    (id INTEGER PRIMARY KEY,
    description TEXT,
    duration INTEGER,
    eliminated INTEGER DEFAULT 0);
''')


def remove_selected_items():
    selected_items = treeview.selection()  # get all selected items
    if not selected_items:
        messagebox.showerror("Error", "No item selected!")
        return
    successful_deletions = 0
    for item in selected_items:
        item_values = treeview.item(item, "values")
        try:
            remove_toil_item(item_values[0])  # remove item from SQLite database
            treeview.delete(item)  # remove item from treeview
            successful_deletions += 1
        except Exception as e:
            print(f"Error removing item with ID {item_values[0]}: {e}")
    if successful_deletions > 0:
        messagebox.showinfo("Items Removed", f"Successfully removed {successful_deletions} items.")
    else:
        messagebox.showinfo("No Items Removed", "No items were removed.")


def show_context_menu(event):
    # Select row under mouse
    treeview.identify_row(event.y)
    if treeview.selection():
        context_menu.post(event.x_root, event.y_root)
    else:
        messagebox.showerror("Error", "No item selected!")


def add_toil_item(description, duration, eliminated):
    try:
        if not description:
            raise ValueError("Description cannot be empty.")
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        conn.execute("INSERT INTO toil_items (description, duration, eliminated) VALUES (?, ?, ?)",
                     (description, duration, eliminated))
        conn.commit()
        messagebox.showinfo("Success", "Toil added successfully!")
        # Clear input fields after successful addition
        toil_description_entry.delete(0, END)
        toil_duration_entry.delete(0, END)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_toil_item(id, description, duration, eliminated):
    conn.execute("UPDATE toil_items SET description = ?, duration = ?, eliminated = ? WHERE id = ?",
                 (description, duration, id, eliminated))
    conn.commit()


def remove_toil_item(id):
    try:
        conn.execute("DELETE FROM toil_items WHERE id = ?", (id,))
        conn.commit()
        messagebox.showinfo("Success", "Toil removed successfully!")
        # Clear input fields after successful removal
        toil_id_entry.delete(0, END)
        toil_description_entry.delete(0, END)
        toil_duration_entry.delete(0, END)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def list_toil_items():
    cursor = conn.execute("SELECT * FROM toil_items ORDER BY duration DESC")
    return cursor.fetchall()


def get_total_toil():
    cursor = conn.execute("SELECT SUM(duration) FROM toil_items")
    total_duration = cursor.fetchone()[0]
    return total_duration if total_duration is not None else 0


def export_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Description", "Duration", "Eliminated"])
        writer.writerows(list_toil_items())
    messagebox.showinfo("Success", "Data exported successfully!")


def calculate_money_saved_and_pending(salary):
    # Assuming 52 weeks in a year and 40 hours a week for the salary
    salary_per_hour = salary / (52 * 40)

    # Calculate money saved
    cursor_saved = conn.execute("SELECT SUM(duration) FROM toil_items WHERE eliminated = 1")
    total_duration_saved = cursor_saved.fetchone()[0]
    if total_duration_saved is None:
        total_duration_saved = 0
    total_days_saved = total_duration_saved / (24 * 3600)  # convert duration from seconds to 24-hour days
    total_workdays_saved = total_days_saved * (5 / 7)  # convert total days to workdays, assuming 5 workdays out of 7
    money_saved = total_workdays_saved * salary_per_hour * 8  # multiply by 8 hours to get the daily rate

    # Calculate money pending
    cursor_pending = conn.execute("SELECT SUM(duration) FROM toil_items WHERE eliminated = 0")
    total_duration_pending = cursor_pending.fetchone()[0]
    if total_duration_pending is None:
        total_duration_pending = 0
    total_days_pending = total_duration_pending / (24 * 3600)  # convert duration from seconds to 24-hour days
    total_workdays_pending = total_days_pending * (5 / 7)  # convert total days to workdays, assuming 5 workdays out of 7
    money_pending = total_workdays_pending * salary_per_hour * 8  # multiply by 8 hours to get the daily rate

    return money_saved, money_pending

def openConversionToolWindow():
    # Top Level Object to be treated as a new Window
    def convert_to_seconds(years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60
        seconds += months * 30 * 24 * 60 * 60  # approximating month to 30 days
        seconds += years * 365 * 24 * 60 * 60  # approximating year to 365 days
        return seconds

    def calculate():
        unit = unit_selector.get()
        value = int(value_entry.get())
        inputs = {unit.lower(): value}
        result = convert_to_seconds(**inputs)
        result_label.config(text=f"Total seconds: {result}")
        return result

    def copy_to_clipboard():
        result = calculate()
        pyperclip.copy(str(result))

    conversion_win = Toplevel(root)
    conversion_win.title('Time Convertsion Tool')

    unit_selector = ttk.Combobox(conversion_win, values=['Years', 'Months', 'Days', 'Hours', 'Minutes'])
    unit_selector.set("Minutes")
    unit_selector.grid(column=0, row=0)

    value_entry = ttk.Entry(conversion_win)
    value_entry.grid(column=1, row=0)

    calculate_button = ttk.Button(conversion_win, text="Calculate", command=calculate)
    calculate_button.grid(column=2, row=0)

    copy_button = ttk.Button(conversion_win, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.grid(column=3, row=0)

    result_label = ttk.Label(conversion_win, text="")
    result_label.grid(column=0, row=1, columnspan=4)

def open_preferences_window():
    def save_preferences():
        try:
            salary = float(salary_entry.get())
            messagebox.showinfo("Success", f"Average Engineer's Salary set to ${salary}")
            pref_win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number.")

    pref_win = Toplevel(root)
    pref_win.title('Preferences')

    salary_label = ttk.Label(pref_win, text="Average Engineer's Salary:")
    salary_label.grid(column=0, row=0)

    salary_entry = ttk.Entry(pref_win)
    salary_entry.grid(column=1, row=0)

    save_button = ttk.Button(pref_win, text="Save", command=save_preferences)
    save_button.grid(column=2, row=0)

# Define the color scheme for the dark mode
dark_color_scheme = {
    "bg": "#2B2B2B",
    "fg": "#D3D3D3",
    "fieldbg": "#414141",
    "selectbg": "#4C78A8",
    "selectfg": "#D3D3D3",
    "text": "#D3D3D3",  # Light gray for dark mode
}

# Define the color scheme for the light mode
light_color_scheme = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "fieldbg": "#FFFFFF",
    "selectbg": "#1E88E5",
    "selectfg": "#FFFFFF",
    "text": "#000000",  # Black for light mode
}

# Set initial color scheme
color_scheme = light_color_scheme

# Initialize tkinter root window
root = Tk()
root.geometry("850x600")
root.title("Toil Tracker")

# Configure root window background color
root.config(bg=color_scheme["bg"])

# Create style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background=color_scheme["bg"],
                foreground=color_scheme["fg"],
                fieldbackground=color_scheme["fieldbg"])
style.map('Treeview', background=[('selected', color_scheme["selectbg"])])


def toggle_theme():
    global color_scheme
    color_scheme = dark_color_scheme if color_scheme == light_color_scheme else light_color_scheme
    root.config(bg=color_scheme["bg"])
    inputs_frame.config(bg=color_scheme["bg"])

    toil_description_label.config(bg=color_scheme["bg"], fg=color_scheme["fg"])
    toil_duration_label.config(bg=color_scheme["bg"], fg=color_scheme["fg"])
    toil_id_label.config(bg=color_scheme["bg"], fg=color_scheme["fg"])
    toil_duration_unit_label.config(bg=color_scheme["bg"], fg=color_scheme["fg"])
    toil_description_entry.config(bg=color_scheme["fieldbg"], fg=color_scheme["fg"],
                                  insertbackground=color_scheme["fg"])
    toil_duration_entry.config(bg=color_scheme["fieldbg"], fg=color_scheme["fg"], insertbackground=color_scheme["fg"])
    toil_id_entry.config(bg=color_scheme["fieldbg"], fg=color_scheme["fg"], insertbackground=color_scheme["fg"])
    add_button.config(bg=color_scheme["bg"], fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                      activeforeground=color_scheme["selectfg"])
    remove_button.config(bg=color_scheme["bg"], fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                         activeforeground=color_scheme["selectfg"])
    edit_button.config(bg=color_scheme["bg"], fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                       activeforeground=color_scheme["selectfg"])
    save_button.config(bg=color_scheme["bg"], fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                       activeforeground=color_scheme["selectfg"])
    total_toil_label.config(bg=color_scheme["bg"], fg=color_scheme["fg"])
    style.configure("Treeview",
                    background=color_scheme["bg"],
                    foreground=color_scheme["text"],  # Apply the new text color here
                    fieldbackground=color_scheme["fieldbg"])
    style.map('Treeview', background=[('selected', color_scheme["selectbg"])])
    # Define the style for the ttk.Combobox
    combobox_style = ttk.Style()
    combobox_style.theme_use("default")
    combobox_style.configure("ComboboxStyle.TCombobox",
                             fieldbackground=color_scheme["fieldbg"],
                             background=color_scheme["bg"],
                             foreground=color_scheme["fg"],
                             selectbackground=color_scheme["selectbg"],
                             selectforeground=color_scheme["selectfg"])

    # Apply the style to the ttk.Combobox widgets
    toil_duration_unit.style = "ComboboxStyle.TCombobox"
    toil_total_duration_unit.style = "ComboboxStyle.TCombobox"

    update_treeview()
    update_total_toil()


# Create menu bar
menubar = Menu(root)

# Create file menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Export to CSV", command=export_to_csv)
file_menu.add_command(label="Toggle Theme", command=toggle_theme)
file_menu.add_command(label="Exit", command=root.quit)
file_menu.add_command(label="Preferences", command=open_preferences_window)
menubar.add_cascade(label="File", menu=file_menu)
tools_menu = Menu(menubar, tearoff=0)
tools_menu.add_command(label="Time Conversion", command=openConversionToolWindow)
menubar.add_cascade(label="Tools", menu=tools_menu)

# Apply menu bar
root.config(menu=menubar)


def update_treeview():
    treeview.delete(*treeview.get_children())
    for i, item in enumerate(list_toil_items()):
        treeview.insert('', 'end', values=item)


def add_button_click():
    try:
        toil_duration = int(toil_duration_entry.get())
        duration_unit = toil_duration_unit.get()
        if duration_unit == "Minutes":
            toil_duration = toil_duration * 60
        elif duration_unit == "Hours":
            toil_duration = toil_duration * 3600
        elif duration_unit == "Days":
            toil_duration = toil_duration * 86400
        add_toil_item(toil_description_entry.get(), toil_duration, int(toil_eliminated_var.get()))
        update_treeview()
        update_total_toil()
    except ValueError:
        messagebox.showerror("Invalid input", "Duration must be a number!")


def remove_button_click():
    try:
        remove_toil_item(int(toil_id_entry.get()))
        update_treeview()
        update_total_toil()
    except ValueError:
        messagebox.showerror("Invalid input", "ID must be a number!")


def edit_button_click():
    try:
        selected_item = treeview.selection()[0]
        selected_item_values = treeview.item(selected_item, "values")
        toil_id_entry.delete(0, END)
        toil_id_entry.insert(0, selected_item_values[0])
        toil_description_entry.delete(0, END)
        toil_description_entry.insert(0, selected_item_values[1])
        toil_duration_entry.delete(0, END)
        toil_duration_entry.insert(0, int(timedelta(seconds=int(selected_item_values[2])).total_seconds()))
        toil_eliminated_var.set(int(selected_item_values[3]))
    except Exception as e:
        messagebox.showerror("Error", "No item selected!")


def save_button_click():
    try:
        toil_duration = int(toil_duration_entry.get())
        duration_unit = toil_duration_unit.get()
        if duration_unit == "Minutes":
            toil_duration = toil_duration * 60
        elif duration_unit == "Hours":
            toil_duration = toil_duration * 3600
        elif duration_unit == "Days":
            toil_duration = toil_duration * 86400
        update_toil_item(int(toil_id_entry.get()), toil_description_entry.get(), toil_duration,
                         toil_eliminated_var.get())
        update_treeview()
        update_total_toil()
        messagebox.showinfo("Success", "Toil updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_total_toil():
    total_toil = get_total_toil()
    duration_unit = toil_total_duration_unit.get()
    if duration_unit == "Minutes":
        total_toil = total_toil / 60
    elif duration_unit == "Hours":
        total_toil = total_toil / 3600
    elif duration_unit == "Days":
        total_toil = total_toil / 86400
    total_toil_label.config(text=f"Total Toil: {total_toil:.2f} {duration_unit}")


def search_items(event=None):  # default parameter for keyboard binding
    # Clear the treeview
    for i in treeview.get_children():
        treeview.delete(i)

    # Get the search term
    search_term = search_entry.get()

    # Query the database for the search term
    cursor = conn.execute("SELECT * FROM toil_items WHERE description LIKE ?", ('%' + search_term + '%',))

    # Populate the treeview with the search results
    for row in cursor:
        treeview.insert('', 'end', values=row)

average_engineer_salary = 80000  # Default salary. It will be updated in the Preferences window.

# Function to update the money saved label
def update_money_labels():
    money_saved, money_pending = calculate_money_saved_and_pending(average_engineer_salary)
    money_saved_label.config(text=f'Money Saved: ${money_saved:.2f}')
    money_pending_label.config(text=f'Potential Savings: ${money_pending:.2f}')

    # Call this function again after 1000 ms (1 second)
    root.after(1000, update_money_labels)

# Create label for displaying money saved with larger, bold font
money_saved_label = Label(root, fg='green', bg=color_scheme["bg"], font=('Arial', 14, 'bold'))
money_saved_label.place(relx=1, y=0, anchor='ne')

# Create label for displaying potential savings with smaller, regular font
money_pending_label = Label(root, fg='black', bg=color_scheme["bg"], font=('Arial', 12))
money_pending_label.place(relx=1, y=30, anchor='ne')

update_money_labels()

# Search bar
search_frame = Frame(root, bd=2, padx=15, pady=10, bg=color_scheme["bg"])
search_frame.pack(padx=15, pady=15)
search_label = Label(search_frame, text="Search:", bg=color_scheme["bg"], fg=color_scheme["fg"])
search_label.grid(row=0, column=0, sticky='e')
search_entry = Entry(search_frame, bg=color_scheme["fieldbg"], fg=color_scheme["fg"],
                     insertbackground=color_scheme["fg"])
search_entry.grid(row=0, column=1, sticky='we')
search_button = Button(search_frame, text="Search", command=search_items, bg=color_scheme["bg"], fg=color_scheme["fg"],
                       activebackground=color_scheme["selectbg"], activeforeground=color_scheme["selectfg"])
search_button.grid(row=0, column=2, sticky='we')

# Bind the search function to the 'Control + f' shortcut
root.bind('<Control-f>', search_items)

# Toil inputs frame
inputs_frame = Frame(root, bd=2, padx=15, pady=10, bg=color_scheme["bg"])
inputs_frame.pack(padx=15, pady=15)

# Toil description label and entry
toil_description_label = Label(inputs_frame, text="Toil Description:", bg=color_scheme["bg"], fg=color_scheme["fg"])
toil_description_label.grid(row=0, column=0, sticky='e')
toil_description_entry = Entry(inputs_frame, bg=color_scheme["fieldbg"], fg=color_scheme["fg"],
                               insertbackground=color_scheme["fg"])
toil_description_entry.grid(row=0, column=1, sticky='we')

# Toil duration label and entry
toil_duration_label = Label(inputs_frame, text="Toil Duration:", bg=color_scheme["bg"], fg=color_scheme["fg"])
toil_duration_label.grid(row=1, column=0, sticky='e')
toil_duration_entry = Entry(inputs_frame, bg=color_scheme["fieldbg"], fg=color_scheme["fg"],
                            insertbackground=color_scheme["fg"])
toil_duration_entry.grid(row=1, column=1, sticky='we')

# Toil duration unit label and dropdown
toil_duration_unit_label = Label(inputs_frame, text="Duration Unit:", bg=color_scheme["bg"], fg=color_scheme["fg"])
toil_duration_unit_label.grid(row=1, column=2, padx=(10, 0), sticky='w')
toil_duration_unit = ttk.Combobox(inputs_frame, values=["Seconds", "Minutes", "Hours", "Days"],
                                  style="ComboboxStyle.TCombobox")
toil_duration_unit.set("Seconds")
toil_duration_unit.grid(row=1, column=3, sticky='we')

# Toil id label and entry
toil_id_label = Label(inputs_frame, text="Toil ID (for editing/removing):", bg=color_scheme["bg"],
                      fg=color_scheme["fg"])
toil_id_label.grid(row=2, column=0, sticky='e')
toil_id_entry = Entry(inputs_frame, bg=color_scheme["fieldbg"], fg=color_scheme["fg"],
                      insertbackground=color_scheme["fg"])
toil_id_entry.grid(row=2, column=1, sticky='we')

# Toil buttons
add_button = Button(inputs_frame, text="Add Toil", command=add_button_click, bg=color_scheme["bg"],
                    fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                    activeforeground=color_scheme["selectfg"])
add_button.grid(row=3, column=1, sticky='we')
remove_button = Button(inputs_frame, text="Remove Toil", command=remove_button_click, bg=color_scheme["bg"],
                       fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                       activeforeground=color_scheme["selectfg"])
remove_button.grid(row=3, column=2, sticky='we')
edit_button = Button(inputs_frame, text="Edit Toil", command=edit_button_click, bg=color_scheme["bg"],
                     fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                     activeforeground=color_scheme["selectfg"])
edit_button.grid(row=3, column=3, sticky='we')
save_button = Button(inputs_frame, text="Save Changes", command=save_button_click, bg=color_scheme["bg"],
                     fg=color_scheme["fg"], activebackground=color_scheme["selectbg"],
                     activeforeground=color_scheme["selectfg"])
save_button.grid(row=3, column=4, sticky='we')

# Toil treeview
treeview = ttk.Treeview(root)
treeview.pack(fill='x')
treeview['columns'] = ["id", "description", "duration", "eliminated"]
treeview.column("#0", width=0, stretch=NO)  # Hide the first column (tree column)

treeview.column("id", width=50)
treeview.column('description', width=300)
treeview.column('duration', width=200)
treeview.column('eliminated', width=100)
treeview.heading('id', text="ID")
treeview.heading('description', text='Description')
treeview.heading('duration', text='Duration (s)')
treeview.heading('eliminated', text='Eliminated')
treeview.pack(pady=20)

# Total toil label
total_toil_label = Label(root, text="", bg=color_scheme["bg"], fg=color_scheme["fg"])
total_toil_label.pack()

# Total toil duration unit dropdown
toil_total_duration_unit = ttk.Combobox(root, values=["Seconds", "Minutes", "Hours", "Days"], state="readonly",
                                        style="ComboboxStyle.TCombobox")
toil_total_duration_unit.set("Seconds")
toil_total_duration_unit.pack(pady=10)
toil_total_duration_unit.bind("<<ComboboxSelected>>", lambda _: update_total_toil())

# Add a checkbox for 'eliminated'
toil_eliminated_label = Label(inputs_frame, text="Eliminated:", bg=color_scheme["bg"], fg=color_scheme["fg"])
toil_eliminated_label.grid(row=4, column=0, sticky='e')
toil_eliminated_var = IntVar()
toil_eliminated_checkbox = Checkbutton(inputs_frame, variable=toil_eliminated_var, onvalue=1, offvalue=0,
                                       bg=color_scheme["bg"], fg=color_scheme["fg"])
toil_eliminated_checkbox.grid(row=4, column=1, sticky='w')

# Create a context menu
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Remove", command=remove_selected_items)

treeview.bind("<Button-3>", show_context_menu)  # Button-3 corresponds to the right-click event

# Update treeview and total toil initially
update_treeview()
update_total_toil()

root.mainloop()
