from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

# -----------------------------
# Step 1: Define Challenges
# -----------------------------
challenges = [
    "Data Heterogeneity",
    "Data Integration",
    "Error & Inconsistent Data",
    "Misspelling in Data Entry",
    "Missing/Invalid Data",
    "Traceability",
    "Data Harmonization",
    "Visualization",
    "Data Aggregation",
    "Data Provenance",
    "Storage Logs",
    "Real-time Analysis",
    "New Visualization Techniques"
]

# -----------------------------
# Step 2: Define Criteria
# -----------------------------
criteria = [
    "Project Administration",
    "Coordination",
    "Software Methodology",
    "Human Resource",
    "Technology"
]

# -----------------------------
# Step 3: Fuzzy Scale
# -----------------------------
fuzzy_scale = {
    "Low": (1, 2, 3),
    "Medium": (3, 5, 7),
    "High": (7, 9, 9)
}

# -----------------------------
# Step 4: Decision Matrix (Linguistic)
# (You can tweak values if needed)
# -----------------------------
linguistic_matrix = [
    ["High","Medium","High","Medium","High"],
    ["Medium","Medium","High","Medium","High"],
    ["High","High","Medium","Medium","High"],
    ["Low","Medium","Medium","Low","Medium"],
    ["High","High","High","Medium","High"],
    ["Medium","High","Medium","Medium","Medium"],
    ["Medium","Medium","Medium","Medium","High"],
    ["High","High","High","Medium","High"],
    ["Medium","Medium","Medium","Medium","Medium"],
    ["Medium","Medium","Medium","Medium","Medium"],
    ["Low","Medium","Medium","Low","Medium"],
    ["High","High","High","High","High"],
    ["Medium","High","High","Medium","High"]
]

# -----------------------------
# Step 5: Convert to Numeric (Defuzzify)
# -----------------------------
def defuzzify(triple):
    return sum(triple) / 3

matrix = np.array([
    [defuzzify(fuzzy_scale[val]) for val in row]
    for row in linguistic_matrix
])

# -----------------------------
# Step 6: Weights
# -----------------------------
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# -----------------------------
# Step 7: TOPSIS
# -----------------------------
def topsis(matrix, weights):
    # Normalize
    norm = matrix / np.sqrt((matrix**2).sum(axis=0))
    
    # Weighted matrix
    weighted = norm * weights
    
    # Ideal best & worst
    ideal_best = np.max(weighted, axis=0)
    ideal_worst = np.min(weighted, axis=0)
    
    # Distance
    dist_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))
    
    # Score
    scores = dist_worst / (dist_best + dist_worst)
    
    return scores

# -----------------------------
# Step 8: Route
# -----------------------------
@app.route('/')
def get_ranking():
    scores = topsis(matrix, weights)
    
    ranking = sorted(
        zip(challenges, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return jsonify(ranking)

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)