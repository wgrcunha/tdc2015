import httpagentparser
import random
import redis
import os
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/")
def hello():
    conn = redis.Redis(db=1)

    # Check cookie
    uid = request.cookies.get("yourid", 0)

    if not uid or not conn.sismember('/set/uids', uid):

        # Generate Z from user-agent
        for key, value in httpagentparser.detect(request.user_agent.string).iteritems():
            redis_key = os.path.join('/zset', key)
            if value:
                conn.zadd(redis_key, value.get('name'), 1)

        # Generate a general counter
        conn.incr('/string/counter', 1)

        # Generate a ID for the current request
        uid = random.randrange(1, 1000000)
        while conn.sismember('/set/uids', uid):
            uid = random.randrange(100000)
        conn.sadd('/set/uids', uid)

        # Generate a response with a cookie
        response = make_response("Hello from #tdc2015, your uid is: %s" % uid)
        response.set_cookie('yourid', value=str(uid))

        # Increment visit
        conn.incr('/string/uids/%s' % uid, 1)

        # Set the values
        for k, v in request.headers:
            conn.hset('/hash/%s' % uid, k, v)

    else:
        conn.incr('/string/uids/%s' % uid, 1)
        response = make_response("Hello from #tdc2015, welcome back: %s, this is your hit number: %s" % (uid, conn.get('/string/uids/%s' % uid)))

    return response

if __name__ == "__main__":
    app.run(debug=True)