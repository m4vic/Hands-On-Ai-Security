# CREATE TABLE users (name TEXT, password TEXT);
# INSERT INTO users VALUES ('alice', 'alice2');
# INSERT INTO users VALUES ('admin', 'admin1');

# SELECT * FROM users WHERE name = 'alice';


import sqlite3


con = sqlite3.connect(":memory:")

cur = con.cursor() 

cur.execute("CREATE TABLE users (name TEXT, password TEXT)")
cur.execute("INSERT INTO users VALUES ('alice', 'alice2')")
cur.execute("INSERT INTO users VALUES ('admin', 'admin1')")

con.commit()

cur.execute("SELECT * FROM users WHERE name = 'alice'")
print("alice's row", cur.fetchall())


def login_danger(user_input):
    query = f"SELECT * FROM users WHERE name = 'alice' AND password = '{user_input}'"
    cur.execute(query)
    return cur.fetchall()


print("real password  -> ", login_danger("alice2"))
print("injected 'OR' '1'='1 ->", login_danger("'OR '1'='1")) 


def login_safe(user_input):
    cur.execute(
        "SELECT * FROM users WHERE name = 'alice' AND password = ?",
        (user_input,),
    )
    return cur.fetchall()


print("real password  -> ", login_safe("alice2"))
print("injected 'OR' '1'='1 ->", login_safe("'OR '1'='1"))


