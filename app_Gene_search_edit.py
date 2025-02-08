from flask import Flask, render_template, request, jsonify
import mysql.connector
import sys
from config import DB_CONFIG
import matplotlib  #to make graphs 
matplotlib.use("Agg")  # Fix GUI issue on macOS
import matplotlib.pyplot as plt
#io use it to create a temporary buffer (BytesIO object)
#where we store the Matplotlib-generated graph without saving it as an actual file
import io # to manage in-memory file-like objects      
#base64 used for encoding binary data into a text format
#we encode the graph as a Base64 string, which allows to embed it directly into HTML as an <img> tag
import base64

app = Flask(__name__)

# Function to connect to MySQL through the config key
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Route to display the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle SNP & Gene Name search add more for future if we want 
@app.route("/search", methods=["GET"])
def search():
    search_type = request.args.get("snp_type")  # Fix the form input name
    query = request.args.get("query", "").strip()  # Prevent NoneType error

    if not query:
        return render_template("index.html", table=None, graph_url=None)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Ensuring correct table names
    if search_type == "snp":
        cursor.execute("SELECT * FROM snps WHERE snp_id = %s", (query,))
    elif search_type == "gene":
        cursor.execute("""
            SELECT snps.snp_id, snps.p_value, snps.link, snp_genome.gene_id
            FROM snp_genome
            JOIN snps ON snp_genome.snp_id = snps.snp_id
            WHERE snp_genome.gene_id = %s
        """, (query,))
    else:
        return render_template("index.html", table=None, graph_url=None)

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    # Generate the table
    table = None  # Default to None if no results
    if results:
        table = "<table border='1'><tr><th>SNP ID</th><th>Gene</th><th>P-Value</th><th>Source</th></tr>"
        for row in results:
            table += f"<tr><td>{row['snp_id']}</td><td>{row['gene_id']}</td><td>{row['p_value']}</td>"
            table += f"<td><a href='{row.get('link', '#')}' target='_blank'>Source</a></td></tr>"
        table += "</table>"

    # Generate P-value graph as an example
    graph_url = None
    if results:
        # Extract SNP IDs and P-values
        snp_ids = [row['snp_id'] for row in results]
        p_values = [row['p_value'] for row in results]

        if snp_ids and p_values:
            plt.figure(figsize=(10, 6))
            plt.bar(snp_ids, p_values, color='skyblue')
            plt.xlabel('SNP IDs')
            plt.ylabel('P-Values')
            plt.title('SNP P-Values Visualization')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the graph to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()

            # Encode the graph as a Base64 string
            graph_url = "data:image/png;base64," + base64.b64encode(img.read()).decode('utf-8')

    return render_template("index.html", table=table, graph_url=graph_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
