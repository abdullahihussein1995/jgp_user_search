from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load Excel data at startup
data = pd.read_excel("JGP.xlsx")

@app.route("/")
def index():
    # Extract unique counties to pass to the frontend
    counties = data["County"].dropna().unique().tolist()
    return render_template("index.html", counties=counties)

@app.route("/search", methods=["POST"])
def search():
    try:
        filters = request.json
        county = filters.get("county", "").lower()
        id_number = filters.get("idNumber", "").strip()
        phone_number = filters.get("phoneNumber", "").strip()
        full_name = filters.get("fullName", "").lower()

        # Apply filters
        filtered_data = data
        if county:
            filtered_data = filtered_data[filtered_data["County"].str.lower() == county]
        if id_number:
            filtered_data = filtered_data[filtered_data["WHAT IS YOUR NATIONAL ID?"].astype(str).str.contains(id_number, na=False)]
        if phone_number:
            filtered_data = filtered_data[filtered_data["Phone Number"].astype(str).str.contains(phone_number, na=False)]
        if full_name:
            filtered_data = filtered_data[filtered_data["Full Name"].str.lower().str.contains(full_name, na=False)]

        # Ensure JSON serializability
        results = filtered_data.fillna("").to_dict(orient="records")  # Replace NaN with empty strings
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error as JSON

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
