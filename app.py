from crypt import methods
from tabnanny import check
import plaid
from plaid.api import plaid_api
from flask import Flask, jsonify
import requests
import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:admin@cluster0.orjsd.mongodb.net/Stock-Act?retryWrites=true&w=majority')
db = client["Stock-Act"]
users = db["users"]



app = Flask(__name__)

# configuration = plaid.Configuration(
#     host=plaid.Environment.Sandbox,
#     api_key={
#         'clientId': '61f60b0a6862640013522b7d',
#         'secret': 'db81faacca77ffe422a201b1777dd2',
#     }
# )
#
# api_client = plaid.ApiClient(configuration)
# client = plaid_api.PlaidApi(api_client)

# ALPACA
BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': 'PKRRRDL0OBGCBIEBBERD',
           'APCA-API-SECRET-KEY': 'NwLG8uuMDBETc8fJrfLY0WvyefM94kuLUWbu9Rcq'}


@app.route('/getaccount', methods=['GET'])
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

@app.route('/checkuser/<string:user>/<string:pwd>', methods=['GET'])
def check_user(user, pwd=""):
    print("checking user")
    resp = users.find_one({"username": user})
    if resp and resp['password'] == pwd:
        return jsonify({'id': str(resp['_id']), 'username': resp['username']})
    return None

@app.route('/createuser/<string:user>/<string:pwd>', methods=['GET'])
def create_user(user, pwd):
    name = users.find_one({'username': user})
    print(name)
    if not name:
        users.insert_one({"username": user, "password": pwd, "track": 'untracked'})
        return json.loads('user added')
    return None


@app.route('/createorder/<string:symbol>/<int:qty>/<string:side>/<string:type>/<string:time_in_force>', methods=['GET'])
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


@app.route('/settrack/<string:user>/<string:politician>', methods=['GET'])
def set_track(user,politician):
    users.find_one_and_update({'user': user},{'track': politician})


@app.route('/getorders', methods=['GET'])
def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)


def hit_endpoint():
    url = "https://api.quiverquant.com/beta/live/housetrading"
    headers = {'accept': 'application/json',
               'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
               'Authorization': 'Token 591c8fca810b40d0893aa0276056760ed097e082'}
    r = requests.get(url, headers=headers)
    data = json.loads(r.content)

    return data


@app.route('/')
def index():
    return 'Welcome to the StockAct API'


@app.route('/listpoliticians', methods=['GET'])
def get_politician_names():
    data = hit_endpoint()
    names = []
    for trade in data:
        name = trade['Representative'].strip()
        if not name in names:
            names.append(name)
    # print(names)
    return jsonify(names)


@app.route('/politicians/<string:name>', methods=['GET'])
def get_politician_trades(name):
    data = hit_endpoint()
    trades = []

    for trade in data:
        if trade['Representative'].strip() == name:
            trades.append(trade)

    # print(trades)
    return jsonify(trades)


if __name__ == '__main__':
    # app.run(threaded=True, port=5000)
    with app.app_context():
    #     get_politician_names()
    #     get_politician_trades('Nancy Pelosi')
    # print(create_order('AAPL', 100, 'buy', 'market', 'gtc'))
    # create_user("testuser","testpass")
        # print(check_user('testuser','testpass'))
        try:
            print(create_user("user123","pass123"))
        except ValueError:
            pass
        # print(check_user("user123","pass123"))
        # print(set_track("user123","nancy"))
