# import csv
# import sqlite3
# from venv import create

# con = sqlite3.connect("ira.db")
# cursor = con.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# # query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# # cursor.execute(query)
# # con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()


# # testing module
# # app_name = "android studio"
# # cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# # results = cursor.fetchall()
# # print(results[0][0])

# #create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# #Specify the column indices you want to import (0-based index)
# #Example: Importing the 1st and 3rd columns
# # desired_columns_indices = [0, 18]

# # # Read data from CSV and insert into SQLite table for the desired columns
# # with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
# #     csvreader = csv.reader(csvfile)
# #     for row in csvreader:
# #         selected_data = [row[i] for i in desired_columns_indices]
# #         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # # Commit changes and close connection
# # con.commit()
# # con.close()

# # query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# # cursor.execute(query)
# # con.commit()

# # query = 'vartika'
# # query = query.strip().lower()

# # cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# # results = cursor.fetchall()
# # print(results[0][0])






import sqlite3
import os

# Connect (or create if not exists)
con = sqlite3.connect("ira.db")
cursor = con.cursor()

# ==============================
# Create Tables
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE,
    path VARCHAR(1000)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE,
    url VARCHAR(1000)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200),
    mobile_no VARCHAR(255),
    email VARCHAR(255) NULL
)""")

# ==============================
# Pre-fill Apps (adjust paths if needed)
# ==============================
apps = [
    ('notepad', r'C:\Windows\system32\notepad.exe'),
    ('calculator', r'C:\Windows\system32\calc.exe'),
    ('paint', r'C:\Windows\system32\mspaint.exe'),
    ('word', r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.exe'),
    ('excel', r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.exe'),
    ('powerpoint', r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.exe'),
    ('chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
    ('vs code', r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe'),
    ('file explorer', r'C:\Windows\explorer.exe'),  # Added File Explorer
]


for app in apps:
    try:
        cursor.execute("INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)", app)
    except Exception as e:
        print("Error inserting app:", e)

# ==============================
# Pre-fill Websites
# ==============================
websites = [
    ('chatgpt', 'https://chat.openai.com'),
    ('google', 'https://google.com'),
    ('youtube', 'https://youtube.com'),
    ('github', 'https://github.com'),
    ('stackoverflow', 'https://stackoverflow.com'),
    ('linkedin', 'https://linkedin.com'),
    ('facebook', 'https://facebook.com'),
    ('twitter', 'https://twitter.com'),
    ('instagram', 'https://instagram.com'),
    ('wikipedia', 'https://wikipedia.org'),
]

for site in websites:
    try:
        cursor.execute("INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)", site)
    except Exception as e:
        print("Error inserting site:", e)

# Save & Close
con.commit()


print("✅ Database initialized successfully with apps and websites.")

# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

#create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


#Specify the column indices you want to import (0-based index)
#Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'vartika'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

cursor.execute(
    "INSERT INTO contacts (name, mobile_no) VALUES (?, ?)",
    ("ds", "9451660562")
)
con.commit()
con.close()
