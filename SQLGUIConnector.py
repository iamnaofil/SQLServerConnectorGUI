import mysql.connector
import tkinter as tk
from tkinter import messagebox


def connect_to_server():
    global connection
    try:
        connection = mysql.connector.connect(
            user=username_var.get(),
            password=password_var.get(),
            host=host_var.get(),
            port=int(port_var.get())
        )

        if connection.is_connected():
            status_label.config(text="Connected to the server",fg='blue')
            database_button.config(state=tk.NORMAL)

    except mysql.connector.Error as e:
        messagebox.showerror("Error", str(e))

def show_databases():
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    database_listbox.delete(0, tk.END)
    for db in databases:
        database_listbox.insert(tk.END, db[0])
    cursor.close()

def select_database(event):
    selected_database = database_listbox.get(tk.ACTIVE)
    connected_database_label.config(text="Connected Database: " + selected_database, fg='purple')
    use_database_button.config(state=tk.NORMAL)
    show_tables_button.config(state=tk.NORMAL)

def use_selected_database():
    selected_database = database_listbox.get(tk.ACTIVE)
    connection.database = selected_database
    messagebox.showinfo("Success", f"Using database: {selected_database}")

def show_tables():
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_listbox.delete(0, tk.END)
    for table in tables:
        table_listbox.insert(tk.END, table[0])
    cursor.close()

def insert_record():
    cursor = connection.cursor()
    insert_query = "INSERT INTO Student (id, name, class) VALUES (%s, %s, %s)"
    record_to_insert = (3, "Ansari Khalid", "B.Sc.")
    cursor.execute(insert_query, record_to_insert)
    connection.commit()
    messagebox.showinfo("Success", "Record inserted successfully")
    cursor.close()

# GUI initialization
root = tk.Tk()
root.title("MySQL GUI")
root.geometry("600x1000")


# Server Connection Section
# Server Connection Section
connection_frame = tk.Frame(root)
connection_frame.pack(padx=10, pady=10, anchor='w')

connect_label = tk.Label(connection_frame, text="Server Connection:")
connect_label.pack(side='top', anchor='w')

username_label = tk.Label(connection_frame, text="Username:")
username_label.pack(side='top', anchor='w')
username_var = tk.StringVar()
username_entry = tk.Entry(connection_frame, textvariable=username_var)
username_entry.pack(side='top', anchor='w')

password_label = tk.Label(connection_frame, text="Password:")
password_label.pack(side='top', anchor='w')
password_var = tk.StringVar()
password_entry = tk.Entry(connection_frame, textvariable=password_var, show='*')
password_entry.pack(side='top', anchor='w')

host_label = tk.Label(connection_frame, text="Host:")
host_label.pack(side='top', anchor='w')
host_var = tk.StringVar()
host_entry = tk.Entry(connection_frame, textvariable=host_var)
host_entry.pack(side='top', anchor='w')

port_label = tk.Label(connection_frame, text="Port:")
port_label.pack(side='top', anchor='w')
port_var = tk.StringVar()
port_entry = tk.Entry(connection_frame, textvariable=port_var)
port_entry.pack(side='top', anchor='w')
connect_button = tk.Button(root, text="Connect to Server",fg='black', command=connect_to_server)
connect_button.pack(padx=10,pady=10,anchor='w')

status_label = tk.Label(root, text="Not connected")
status_label.pack(side='left')

# Databases Section
database_button = tk.Button(root, text="Show Databases", state=tk.DISABLED, command=show_databases)
database_button.pack(padx=10,pady=10,anchor='center')

database_listbox = tk.Listbox(root)
database_listbox.pack()
database_listbox.bind("<<ListboxSelect>>", select_database)

connected_database_label = tk.Label(root, text="Connected Database: None")
connected_database_label.pack()

use_database_button = tk.Button(root, text="Use Selected Database", state=tk.DISABLED, command=use_selected_database)
use_database_button.pack()

# Tables Section
show_tables_button = tk.Button(root, text="Show Tables", state=tk.DISABLED, command=show_tables)
show_tables_button.pack()

table_listbox = tk.Listbox(root)
table_listbox.pack()

# Insert Record Section
insert_button = tk.Button(root, text="Insert Record", state=tk.DISABLED, command=insert_record)
insert_button.pack()

# Run the GUI
root.mainloop()
