from flask import Flask, jsonify

app = Flask(__name__)

def fuzzy_topsis():
    # dummy data (you can change later)
    alternatives = ["A1", "A2", "A3"]
    scores = [0.6, 0.8, 0.7]

    result = sorted(zip(alternatives, scores), key=lambda x: x[1], reverse=True)
    return result

@app.route('/')
def home():
    result = fuzzy_topsis()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)