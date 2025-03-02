
from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import plotly.express as px
import io
import base64
from config import DB_CONFIG 
app = Flask(__name__)

def get_db_connection(): # Same as Aida's code only it returns an error if a connection isn't made. Better for future use.
    """Database connection with error handling"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err: # Displays the error type from MySql.
        print(f"Database connection error: {err}")
        return None
    
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("search_term", "").strip()
    search_type = request.form.get("searchType", "")
    population_type = request.form.get("population_type", "all")

    if not query:
        return render_template("pop.html", search_results=None, manhattan_url=None, population_map_url=None)

    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)
        results = []
        phenotype_results = []

        if search_type == "snp":
            cursor.execute("""
                SELECT SNPs.snp_id, SNPs.chromosome, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                FROM SNPs
                LEFT JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
                LEFT JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                WHERE SNPs.snp_id = %s
            """, (query,))
            results = cursor.fetchall()

            cursor.execute("""
                SELECT snp_id, phenotype_id
                FROM Phenotype_SNP
                WHERE snp_id = %s
            """, (query,))
            phenotype_results = cursor.fetchall()

        elif search_type == "gene":
            cursor.execute("""
                SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                FROM SNP_Gene
                JOIN SNPs ON SNP_Gene.snp_id = SNPs.snp_id
                JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                WHERE SNP_Gene.gene_id = %s
            """, (query,))
            results = cursor.fetchall()

            snp_ids = [row["snp_id"] for row in results]
            if snp_ids:
                cursor.execute(f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({','.join(['%s'] * len(snp_ids))})
                """, tuple(snp_ids))
                phenotype_results = cursor.fetchall()

        elif search_type == "chromosome":
            parts = query.split(":")
            chromosome = parts[0]
            start_pos, end_pos = None, None

            if len(parts) > 1:
                position_part = parts[1]
                if "-" in position_part:
                    start_pos, end_pos = map(int, position_part.split("-"))
                else:
                    start_pos = end_pos = int(position_part)

            if start_pos is not None and end_pos is not None:
                cursor.execute("""
                    SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                    FROM SNPs
                    JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
                    JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                    WHERE SNPs.chromosome = %s
                    AND (Gene_Functions.gene_start BETWEEN %s AND %s
                    OR Gene_Functions.gene_end BETWEEN %s AND %s
                    OR (Gene_Functions.gene_start <= %s AND Gene_Functions.gene_end >= %s))
                """, (chromosome, start_pos, end_pos, start_pos, end_pos, start_pos, end_pos))
            else:
                cursor.execute("""
                    SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                    FROM SNPs
                    JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
                    JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                    WHERE SNPs.chromosome = %s
                """, (chromosome,))
            results = cursor.fetchall()

            snp_ids = [row["snp_id"] for row in results]
            if snp_ids:
                cursor.execute(f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({','.join(['%s'] * len(snp_ids))})
                """, tuple(snp_ids))
                phenotype_results = cursor.fetchall()

        if not results:
            return render_template("pop.html", search_results=None, error_message="No results found.")


        phenotype_table_html = pd.DataFrame(phenotype_results).to_html(classes="table table-striped", index=False)
        population_results = fetch_population_results(query, search_type)
        filtered_population_results = filter_population_data(population_results, population_type)
        population_map_url = generate_population_plot(filtered_population_results)

        return render_template("pop.html",
                               search_results=results,
                               phenotype_table_html=phenotype_table_html,
                               population_results=filtered_population_results,
                               population_map_url=population_map_url)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("error.html", message="Database query failed")
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
@app.route('/gene/<gene_id>')
def gene_info(gene_id):
    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch gene information from the database
        cursor.execute("""
        SELECT Gene_Functions.gene_id, Gene_Functions.gene_description, Gene_Functions.ensembl_id, Gene_Functions.gene_start, Gene_Functions.gene_end, SNP_Gene.snp_id, Gene_GO.go_id, Gene_GO.go_description
        FROM Gene_Functions
        LEFT JOIN SNP_Gene ON Gene_Functions.gene_id = SNP_Gene.gene_id LEFT JOIN Gene_GO ON Gene_Functions.gene_id = Gene_GO.gene_id
        WHERE Gene_Functions.gene_id = %s
        """, (gene_id,))

        rows = cursor.fetchall()
        # Process the first row (if it exists)
        if rows:
            gene_info = rows[0]  # Get the first row
            print("Gene info is:", gene_info)
        else:
            print("No gene found with ID:", gene_id)

        return render_template('gene_info.html', gene_info=gene_info)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("error.html", message="Database query failed")
    finally:
        if 'cursor' in locals(): cursor.close()
        if connection.is_connected(): connection.close()

def fetch_population_results(query, search_type):
    """Fetches population data based on the query and search type."""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        if search_type == "snp":
            cursor.execute("""
                SELECT snp_id, pop_id, population_name, Ethnicity, sample_size, allele_frequency
                FROM Population
                WHERE snp_id = %s
            """, (query,))
        elif search_type == "gene":
            cursor.execute("""
                SELECT p.snp_id, p.pop_id, p.population_name, p.Ethnicity, p.sample_size, p.allele_frequency
                FROM Population p
                JOIN SNP_Gene sg ON p.snp_id = sg.snp_id
                JOIN Gene_Functions gf ON sg.gene_id = gf.gene_id
                WHERE gf.gene_id = %s
            """, (query,))
        elif search_type == "chromosome":
            cursor.execute("""
                SELECT p.snp_id, p.pop_id, p.population_name, p.Ethnicity, p.sample_size, p.allele_frequency
                FROM Population p
                JOIN SNPs s ON p.snp_id = s.snp_id
                WHERE s.chromosome = %s
            """, (query,))
        else:
            return []
        
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

def filter_population_data(population_results, population_type):
    """Filters population data based on the selected population type."""
    if population_type == "all":
        return population_results

    population_mapping = {
        "slk": "South Asian",
        "bpb": "South Asian",
        "jpn": "East Asian",
        # Add more mappings as needed
    }

    population_name = population_mapping.get(population_type)
    if population_type == population_name:
        return [row for row in population_results if row.get("population_name") == population_name]
    
    else:
        return[]
    

def generate_population_plot(population_data):
    """Generates a Plotly map for population data."""
    if not population_data:
        return None

    df = pd.DataFrame(population_data)
    population_coords = {
        "BPB": {"lat": 20.5937, "lon": 78.9629}, # Bangladesh
        "SLK": {"lat": 7.8731, "lon": 80.7718}, # Sri lankan
        "JPN": {"lat": 36.2048, "lon": 138.2529} # Japanese
    }

    df["lat"] = df["population_name"].map(lambda x: population_coords.get(x, {}).get("lat"))
    df["lon"] = df["population_name"].map(lambda x: population_coords.get(x, {}).get("lon"))
    df = df.dropna(subset=["lat", "lon"])

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        scope="asia",
        size="sample_size",
        color="allele_frequency",
        hover_name="population_name",
        projection="natural earth",
        title="Population Distribution in Asia"
    )

    img_buffer = io.BytesIO()
    fig.write_image(img_buffer, format="png")
    img_buffer.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img_buffer.read()).decode('utf-8')}"
@app.route("/population_map", methods=["GET"])

def population_map():
    print("Accessed /population_map route")  # Debugging log

    population_data = fetch_population_results()

    # Generate the population map
    population_map_url = generate_population_plot(population_data)

    if not population_map_url:
        print("No population map generated!")
        return render_template("error.html", message="Failed to generate population map")

    print("Population map generated successfully, rendering template.")
    return render_template("pop.html", population_map_url=population_map_url)
if __name__ == "__main__":
    app.run(debug=True)