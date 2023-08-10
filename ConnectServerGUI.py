import mysql.connector
import tkinter as tk
from tkinter import messagebox
import csv

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
    show_columns_and_records_button.config(state=tk.NORMAL)
    # Enable the button for showing columns and records
    convert_to_csv_button.config(state=tk.NORMAL)#Enable CSV Button

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


def show_columns_and_records():
    selected_table = table_listbox.get(tk.ACTIVE)
    cursor = connection.cursor()

    # Show columns
    cursor.execute(f"DESCRIBE {selected_table}")
    columns = [column[0] for column in cursor.fetchall()]
    columns_text = "\n".join(columns)
    columns_label.config(text=f"Columns of {selected_table}:\n{columns_text}")

    # Show records
    cursor.execute(f"SELECT * FROM {selected_table}")
    records = cursor.fetchall()
    records_text = "\n".join([str(record) for record in records])
    records_label.config(text=f"Records of {selected_table}:\n{records_text}")

    cursor.close()



def convert_to_csv():
    selected_table = table_listbox.get(tk.ACTIVE)
    cursor = connection.cursor()

    # Show records
    cursor.execute(f"SELECT * FROM {selected_table}")
    records = cursor.fetchall()

    # Get column names
    cursor.execute(f"DESCRIBE {selected_table}")
    columns = [column[0] for column in cursor.fetchall()]

    # Save as CSV
    filename = f"{selected_table}.csv"
    with open(filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerows(records)

    cursor.close()
    messagebox.showinfo("Success", f"Table '{selected_table}' data converted to CSV: {filename}")




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
show_tables_button.pack(padx=10, pady=10, anchor='center')

table_listbox = tk.Listbox(root)
table_listbox.pack()

show_columns_and_records_button = tk.Button(root, text="Show Columns and Records", state=tk.DISABLED, command=show_columns_and_records)
show_columns_and_records_button.pack()

columns_label = tk.Label(root, text="Columns of selected table:\n")
columns_label.pack()

records_label = tk.Label(root, text="Records of selected table:\n")
records_label.pack()

convert_to_csv_button = tk.Button(root, text="Convert to CSV", state=tk.DISABLED, command=convert_to_csv)
convert_to_csv_button.pack()

# Insert Record Section
insert_button = tk.Button(root, text="Insert Record", state=tk.DISABLED, command=insert_record)
insert_button.pack()

# Run the GUI
root.mainloop()
