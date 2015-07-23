import MySQLdb
import base64
import redis
import pickle
from flask import Flask, request, make_response

app = Flask(__name__)

def cached_query(query):
    r = redis.Redis(db=3)
    key = base64.b64encode(query)
    data = r.get(key)
    if data:
        return pickle.loads(data)
    else:
        conn = MySQLdb.connect('localhost', 'imdb', 'imdb')
        conn.select_db('imdb')
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        r.setex(key, pickle.dumps(data), 600)
        return data

@app.route("/")
def hello():
    movies = []
    for line in cached_query('select * from title where production_year = 2015;'):
        movies.append(line)

    response = make_response("Total of %s titles in 2015" % len(movies))

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5002)