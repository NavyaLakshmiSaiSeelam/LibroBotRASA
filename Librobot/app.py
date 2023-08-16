from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def create_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="project",
        password="project",
        database="library_db.sql"
    )
    return conn

@app.route('/books', methods=['POST'])
def insert_book():
    title = request.json['title']
    author = request.json['author']

    conn = create_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO books (title, author) VALUES (%s, %s)"
    values = (title, author)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(message='Book inserted successfully'), 200

@app.route('/books', methods=['GET'])
def get_all_books():
    conn = create_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM books"
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    book_list = []
    for book in books:
        book_dict = {
            'id': book[0],
            'title': book[1],
            'author': book[2]
        }
        book_list.append(book_dict)

    return jsonify(books=book_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
