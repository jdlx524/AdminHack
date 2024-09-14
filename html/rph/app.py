from flask import Flask, jsonify, request, render_template
from retrieve import retrieve

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    searchTerm = request.json['searchTerm']
    topN = request.json['topN']
    # Call your function to retrieve the data from your database or other source
    data = retrieve(searchTerm, "./rph/static/final_result_w_bert_cs.csv", topN)
    # Return the data as a JSON response to the frontend
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8001)
