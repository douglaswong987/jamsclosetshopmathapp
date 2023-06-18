import re
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    content = file.read().decode('utf-8')

    matches = re.findall(r"@([^\n]+)\n((?:.*?\$[\d.]+\n)+)", content)
    totals = {}

    for match in matches:
        name = match[0].strip()
        prices = re.findall(r"\$([\d.]+)", match[1])
        total = sum(float(price) for price in prices)
        totals[name] = total

    return render_template('results.html', totals=totals)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
