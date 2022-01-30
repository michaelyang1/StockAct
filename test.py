from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)


def hit_endpoint():
    url = "https://api.quiverquant.com/beta/live/housetrading"
    headers = {'accept': 'application/json',
               'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
               'Authorization': 'Token 591c8fca810b40d0893aa0276056760ed097e082'}
    r = requests.get(url, headers=headers)
    data = json.loads(r.content)

    for d in data[:100]:
        print(d)
    return data


@app.route('/')
def index():
    return 'Welcome to the StockAct API'


@app.route('/politicians/<string:name>', methods=['GET'])
def get_politician_trades(name):
    data = hit_endpoint()
    trades = []

    for trade in data:
        if trade['Representative'].strip() == name:
            trades.append(trade)

    print(trades)
    return jsonify(trades)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    # with app.app_context():
    #     get_politician_trades('Nancy Pelosi')
