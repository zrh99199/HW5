from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

# The function will run on ('url')
@app.route('/')
def main():
    return render_template('main.html')

# The function will run on ('url/submit/'), the function will use POST and GET methods
@app.route('/submit/', methods=['POST', 'GET'])
def submit():

    # render the submit.html without any argument when there is no submitted form exists
    if request.method == 'GET':
        return render_template('submit.html')

    # else submit the message to the database
    else:
        try:
            message, handle = insert_message()
            return render_template('submit.html', submitted=True, message=message, handle=handle)

        except:
            return render_template('submit.html', error=True)

# The function will run on ('url/view/')
@app.route('/view/')
def view(): 
    return render_template('view.html', messages=random_messages(5))

def get_message_db():
    try:
        return g.message_db

    except:
        # create a sql database
        g.message_db = sqlite3.connect("messages_db.sqlite")

        # use cmd to create a table with three columns
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """

        # execute cmd by cursor
        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db


def insert_message():
    
    # save user's message input as variable 'message' and handle input as variable 'handle'
    message = request.form['message']
    handle = request.form['handle']

    # connect to the database and use cmd to save inputs
    conn = get_message_db()
    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ('{message}', '{handle}')
    """

    cursor = conn.cursor()
    cursor.execute(cmd)

    conn.commit()
    conn.close()

    return message, handle


def random_messages(n):

    # get n random message from our database
    conn = get_message_db()
    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """
    cursor = conn.cursor()
    cursor.execute(cmd)

    # use fetchall to save the random message as variable 'result'
    result = cursor.fetchall()
    conn.close()

    return result
