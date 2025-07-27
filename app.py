from flask import Flask, render_template, request, redirect 
import sqlite3

app = Flask(__name__)

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


@app.route('/')
def index():
    return render_template('index.html')
    
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


if __name__ == '__main__':
    init_db()
    app.run(debug=True)