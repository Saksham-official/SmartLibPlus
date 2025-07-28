from flask import Flask, render_template, request, redirect 
import sqlite3

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html')  # This is your SmartLib homepage

@app.route('/forgot')
def forgot_password():
    return render_template('forgot.html')  # This will show the forgot password page

@app.route('/future')
def future_extensions():
    return render_template('future.html')


def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS BOOKS (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL
                        )
                   ''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded credentials for now
        if username == 'admin' and password == '12345':
            return redirect('/home')  # ✅ go to LMS dashboard
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

    
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        return redirect('/books')
    return render_template('add_book.html')

@app.route('/books')
def view_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('view_books.html', books=books)

@app.route('/delete/<int:id>')
def delete_books(id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/books')

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                       ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
        conn.close()
    return render_template('search_books.html', results=results)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
