from flask import Flask, Response, request
from eventlet import wsgi
from routine.exchange import start_update_exchange_rate
from controller.token import token_cost
import eventlet

app = Flask(__name__)

@app.after_request
def append_headers(response):
    # add Access-Control-Allow-Origin header to every request
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Token'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/v1/token/cost', methods=['POST'])
def v1_token_cost():
    return token_cost()

@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        return Response(status=200)
    return None

if __name__ == '__main__':
    start_update_exchange_rate()
    server = wsgi.server(eventlet.listen(('', 8080)), app)