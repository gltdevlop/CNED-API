from flask import Flask, jsonify, make_response
from scrap_tools.scraper import scrape_data, checking, checking_incor, checking_cor
from vars import *

app = Flask(__name__)

import json
from flask import Response

@app.route('/hws', methods=['GET'])
def scrape_endpoint():
    data = scrape_data(creds, 'data.txt')
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


@app.route('/checkall', methods=['GET'])
def check_endpoint():
    result = checking()
    json_data = json.dumps(result, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


@app.route('/check_cor', methods=['GET'])
def check_cor_endpoint():
    result = checking_cor()
    json_data = json.dumps(result, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


@app.route('/check_incor', methods=['GET'])
def check_incor_endpoint():
    result = checking_incor()
    json_data = json.dumps(result, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
