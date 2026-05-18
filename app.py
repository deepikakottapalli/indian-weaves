from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",
        database="indian_weaves"
    )
    return conn

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Weaves page
@app.route('/weaves')
def weaves():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weaves")
    all_weaves = cursor.fetchall()
    conn.close()
    return render_template('weaves.html', weaves=all_weaves)

# Single weave detail page
@app.route('/weave/<int:id>')
def weave_detail(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weaves WHERE id = %s", (id,))
    weave = cursor.fetchone()
    conn.close()
    return render_template('weave_detail.html', weave=weave)

# Festivals page
@app.route('/festivals')
def festivals():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM festivals")
    all_festivals = cursor.fetchall()
    conn.close()
    return render_template('festivals.html', festivals=all_festivals)

# Explore by Region page
@app.route('/regions')
def regions():
    return render_template('regions.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Search
@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    search_term = '%' + query + '%'
    cursor.execute(
        "SELECT * FROM weaves WHERE name LIKE %s OR state LIKE %s OR region LIKE %s GROUP BY id",
        (search_term, search_term, search_term)
    )
    results = cursor.fetchall()
    conn.close()
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True) 