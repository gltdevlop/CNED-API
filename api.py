from flask import Flask, jsonify
from scrap_tools.scraper import scrape_data, checking, checking_incor, checking_cor
from vars import *

app = Flask(__name__)

@app.route('/hws', methods=['GET'])
def scrape_endpoint():
    result = scrape_data(creds, 'data.txt')
    return jsonify(result)

@app.route('/checkall', methods=['GET'])
def check_endpoint():
    result = checking()
    return jsonify(result)

@app.route('/check_cor', methods=['GET'])
def check_cor_endpoint():
    result = checking_cor()
    return jsonify(result)


@app.route('/check_incor', methods=['GET'])
def check_incor_endpoint():
    result = checking_incor()
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
