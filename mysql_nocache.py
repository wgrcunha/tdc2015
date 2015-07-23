import MySQLdb
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/")
def hello():
    conn = MySQLdb.connect('localhost', 'imdb', 'imdb')
    conn.select_db('imdb')
    cursor = conn.cursor()

    cursor.execute('select * from title where production_year = 2015;')
    movies = []
    for line in cursor.fetchall():
        movies.append(line)

    response = make_response("Total of %s titles in 2015" % len(movies))

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5001)