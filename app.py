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
    return render_template("index.html") #render_template use to connect 

# Route to handle SNP & Gene Name search # should add the other searches 
@app.route("/search", methods=["GET"])
def search():
    search_type = request.args.get("snp_id")
    query = request.args.get("query").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search_type == "snp":
        cursor.execute("SELECT * FROM SNPs WHERE snp_id = %s", (query,))
    elif search_type == "gene":
        cursor.execute("SELECT * FROM SNPs WHERE gene_name = %s", (query,))
    else:
        return render_template("index.html", table=None) #what it got from the sql send it to the front 
#closing the pantery door 
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    # Generate the table witht the rtrived data 
    table = ""
    if results:
        table += "<table border='1'><tr><th>SNP ID</th><th>Gene</th><th>P-Value</th><th>Source</th></tr>"
        for row in results:
            table += f"<tr><td>{row['snp_id']}</td><td>{row.get('gene_name', 'N/A')}</td><td>{row['p_value']}</td>"
            table += f"<td><a href='{row.get('link', '#')}' target='_blank'>Source</a></td></tr>"
        table += "</table>"

    return render_template("index.html", table=table)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

