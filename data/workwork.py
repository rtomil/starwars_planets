def registration(cursor, username, password):
    cursor.execute("""INSERT INTO 'user' (username, password) VALUES %s, %s;""", username, password)
    return "done"

def validator(cursor, username):
    cursor.execute("""SELECT username FROM 'user' WHERE username = %s""", username)
    result = cursor.fetchall()
    return result
