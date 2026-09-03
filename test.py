import sqlite3
from flask import Flask, g, render_template

DATABASE = 'database.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Allows you to use column names like gpu['name'] in your HTML template
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    
    # Query your table
    sql = "SELECT * FROM gpus;"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    return render_template("home.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

