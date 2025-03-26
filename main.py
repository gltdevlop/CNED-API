from flask import Flask, jsonify
from scrap_tools.scraper import scrape_data
from vars import *

app = Flask(__name__)

@app.route('/hws', methods=['GET'])
def scrape_endpoint():
    result = scrape_data(creds, 'data.txt')
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
