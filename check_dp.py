import sqlite3

# 1. Connect to the database file
conn = sqlite3.connect('users.db')

# 2. Create a cursor object to execute SQL queries
cursor = conn.cursor()

# 3. Write a SQL SELECT query to get all rows from your user table
cursor.execute("SELECT * FROM users")  # 'users' කියන table එක ඔයාගේ user data තියෙන table name එක

# 4. Fetch all results from the query
rows = cursor.fetchall()

# 5. Print each row (each row is a user record)
for row in rows:
    print(row)

# 6. Close the connection
conn.close()
