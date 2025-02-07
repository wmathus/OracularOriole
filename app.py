from flask import Flask, render_template, request, jsonify
import mysql.connector
import sys
from config import DB_CONFIG

app = Flask(__name__)

# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Route to display the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle SNP & Gene Name search
@app.route("/search", methods=["GET"])
def search():
    print("🔍 Received Search Request:", request.args.get("snp_type"), request.args.get("query"), file=sys.stderr)

    search_type = request.args.get("snp_type")
    query = request.args.get("query").strip()  # Remove extra spaces

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search_type == "snp":
        cursor.execute("SELECT * FROM snps WHERE snp_id = %s", (query,))
    elif search_type == "gene":
        cursor.execute("SELECT * FROM snps WHERE gene_name = %s", (query,))
    else:
        return jsonify([])

    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

