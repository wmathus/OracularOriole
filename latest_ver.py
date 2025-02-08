from flask import Flask, render_template, request, Response, jsonify
import mysql.connector
from config import DB_CONFIG
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import csv  
from flask import Response

app = Flask(__name__)

def get_db_connection():
    """Get a new database connection with error handling"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

@app.route("/")
def home():
    return render_template("index.html", search_results=None, manhattan_url=None)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_type = request.form.get("searchType")
        query = request.form.get("search_term", "").strip()
    else:
        search_type = request.args.get("searchType")
        query = request.args.get("search_term", "").strip()

    if not query:
        return render_template("index.html", search_results=None, manhattan_url=None)

    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)
        
        if search_type == "snp":
            cursor.execute("SELECT * FROM snps WHERE snp_id = %s", (query,))
        elif search_type == "gene":
            cursor.execute("SELECT * FROM snp_genome WHERE gene_id = %s", (query,))
        else:
            return render_template("index.html", search_results=None, manhattan_url=None)

        results = cursor.fetchall()
        
        manhattan_url = generate_manhattan_plot(results) if results else None
        
        return render_template("index.html",
                             search_results=results,
                             manhattan_url=manhattan_url)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("error.html", message="Database query failed")
    finally:
        if 'cursor' in locals(): cursor.close()
        if connection.is_connected(): connection.close()


# Add this route before the __main__ block
@app.route("/download_csv")
def download_csv():
    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM snps")
        results = cursor.fetchall()

        def generate():
            data = io.StringIO()
            writer = csv.writer(data)
            
            # Write header
            writer.writerow(['SNP_ID', 'Chromosome', 'Alternate_allele' , 'P_Value', 'Odds_ratio', 'source', 'link'])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # Write rows
            for row in results:
                writer.writerow([
                    row.get('snp_id', ''),
                    row.get('chromosome', ''),
                    row.get('alternate_allele', ''),
                    row.get('p_value', ''),
                    row.get('odds_ratio', ''),
                    row.get('source', ''),
                    row.get('link', ''),
                ])
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

        response = Response(
            generate(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=snps_data.csv'}
        )
        return response

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("error.html", message="Download failed")
    finally:
        if 'cursor' in locals(): cursor.close()
        if connection.is_connected(): connection.close()

def generate_manhattan_plot(results):
    try:
        if not results:
            return None

        # Extract multiple SNPs from results
        valid_data = []
        for row in results:
            try:
                chrom = str(row.get("chromosome", ""))
                pval = float(row.get("p_value", 1.0))
                valid_data.append((chrom, pval))
            except (ValueError, TypeError) as e:
                app.logger.error(f"Invalid data row: {row} - Error: {str(e)}")
                continue

        if not valid_data:
            return None

        chromosomes, p_values = zip(*valid_data)

        # Convert chromosomes to numeric indices
        unique_chrom = sorted(set(chromosomes), key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
        chrom_dict = {chrom: idx+1 for idx, chrom in enumerate(unique_chrom)}
        numeric_chrom = [chrom_dict[chrom] for chrom in chromosomes]

        # Create plot
        plt.figure(figsize=(12, 6))
        plt.scatter(numeric_chrom, -np.log10(p_values), 
                    c=numeric_chrom, cmap='viridis', alpha=0.6, edgecolors='w', linewidth=0.5)
        
        plt.axhline(y=-np.log10(5e-8), color='r', linestyle='--', linewidth=1)

        plt.colorbar(ticks=range(1, len(unique_chrom)+1), label='Chromosome', format=plt.FixedFormatter(unique_chrom))
        plt.xlabel('Chromosome')
        plt.ylabel('-log10(p-value)')
        plt.title('Manhattan Plot')
        plt.grid(True, alpha=0.3)

        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        
        return f"data:image/png;base64,{base64.b64encode(img_buffer.read()).decode('utf-8')}"

    except Exception as e:
        app.logger.error(f"Plot generation failed: {str(e)}")
        return None

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
