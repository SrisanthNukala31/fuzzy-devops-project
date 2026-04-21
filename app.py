from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def fuzzy_topsis():
    # Example decision matrix (alternatives x criteria)
    matrix = np.array([
        [7, 9, 9],
        [8, 7, 8],
        [7, 8, 7]
    ])

    weights = np.array([0.3, 0.4, 0.3])

    # Step 1: Normalize
    norm = matrix / np.sqrt((matrix**2).sum(axis=0))

    # Step 2: Weighted matrix
    weighted = norm * weights

    # Step 3: Ideal & negative ideal
    ideal = weighted.max(axis=0)
    negative = weighted.min(axis=0)

    # Step 4: Distance
    d_pos = np.sqrt(((weighted - ideal)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted - negative)**2).sum(axis=1))

    # Step 5: Closeness
    score = d_neg / (d_pos + d_neg)

    # Ranking
    alternatives = ["A1", "A2", "A3"]
    result = sorted(zip(alternatives, score), key=lambda x: x[1], reverse=True)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)