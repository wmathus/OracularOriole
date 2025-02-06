from flask import Flask, render_template, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

#for the searchbox to work
@app.route("/search_snp", methods=["GET"])  #Defines the URL route
def search_snp():
    snp_id = request.args.get("snp_id")  # Get the SNP ID from the user input
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query MySQL to get SNP information
    #The cursor.executewill run a MySQL query to find the SNP

    cursor.execute("SELECT * FROM snps WHERE snp_id = %s", (snp_id,))
    results = cursor.fetchall()

#closing the sql query 
   cursor.close()
    connection.close()
    return jsonify(results)  # Return data as JSON

# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
    
# Route to display the homepage 
@app.route("/")
def home():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
