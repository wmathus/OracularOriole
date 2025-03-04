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
    # Retrieve form data
    query = request.form.get("search_term", "").strip()
    search_type = request.form.get("searchType", "")
    population_type = request.form.get("population_type", "all")

    if not query:
        return render_template("pop.html", search_results=None, pop_results=None, error_message="Please enter a search term.")

    connection = get_db_connection()
    if not connection:
        return render_template("pop.html", search_results=None, pop_results=None, error_message="Database connection failed.")

    try:
        cursor = connection.cursor(dictionary=True)
        global results
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
            return render_template("pop.html", search_results=None, pop_results=None, error_message="No results found.")

        # Fetch population results
        population_results = fetch_population_id(query, search_type)

        # Filter and append population names
        filtered_results = filter_population_data(population_results, population_type)

        # Generate DataFrame with allele frequencies, sample sizes, SNP IDs, and population names
        pop_results = generate_population_df(filtered_results)
        population_map_url = generate_population_plot(pop_results)
        # Convert phenotype results to HTML table
        phenotype_table_html = pd.DataFrame(phenotype_results).to_html(classes="table table-striped", index=False)

        # Render template with results
        return render_template(
            "pop.html",
            search_results=results,
            sidebar_hidden=True,
            phenotype_table_html=phenotype_table_html,
            pop_results=pop_results,
            population_map_url=population_map_url,
            error_message=None
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("pop.html", search_results=None, pop_results=None, error_message="Database query failed.")
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

import pandas as pd
import mysql.connector

def fetch_population_id(query, search_type):
    """Fetches population data based on the query and search type."""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        if search_type == "snp":
            cursor.execute("""
                SELECT snp_id, pop_id
                FROM SNP_Population
                WHERE snp_id = %s
            """, (query,))
        elif search_type == "gene":
            cursor.execute("""
                SELECT sp.snp_id, sp.pop_id
                FROM SNP_Population sp
                JOIN SNP_Gene sg ON sp.snp_id = sg.snp_id          
                JOIN Gene_Functions gf ON sg.gene_id = gf.gene_id
                WHERE gf.gene_id = %s
            """, (query,))
        elif search_type == "chromosome":
            cursor.execute("""
                SELECT sp.snp_id, sp.pop_id
                FROM SNP_Population sp
                JOIN SNPs s ON sp.snp_id = s.snp_id
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
    """Filters population data based on the selected population type and appends population names."""
    if not population_results:
        return []

    # Define population mapping
    population_mapping = {
        "1": "British Pakistani and Bangladeshi",
        "2": "Sri Lankan Tamil",
        "3": "South Asian1",
        "4": "South Asian2",
        "5": "Japanese from Tokyo, Japan",
        "6": "Bengali from Bangladesh",
        "7": "Punjabi from Lahore, Pakistan",
    }

    # Filter results if a specific population type is selected
    if population_type != "all":
        filtered_results = [row for row in population_results if str(row.get("pop_id")) == population_type]
    else:
        filtered_results = population_results

    # Append population names to the results
    for row in filtered_results:
        pop_id = str(row.get("pop_id"))
        row["population_name"] = population_mapping.get(pop_id, "Unknown Population")

    return filtered_results


def generate_population_df(filtered_results):
    """Generates a DataFrame with allele frequencies and sample sizes for the filtered population data."""
    if not filtered_results:
        return pd.DataFrame()

    connection = get_db_connection()
    if not connection:
        return pd.DataFrame()

    try:
        cursor = connection.cursor(dictionary=True)

        # Extract unique population IDs from filtered_results
        pop_ids = [str(row["pop_id"]) for row in filtered_results]
        pop_ids_str = ",".join(pop_ids)

        # Fetch allele frequencies and sample sizes for the selected populations
        cursor.execute(f"""
            SELECT sp.snp_id, pa.pop_id, pa.allele_frequency, p.pop_name, p.sample_size
            FROM Population_Allele pa
            JOIN Population p ON pa.pop_id = p.pop_id
            JOIN SNP_Population sp ON pa.pop_id = sp.pop_id
            WHERE pa.pop_id IN ({pop_ids_str})
        """)

        # Convert results to a DataFrame
        df = pd.DataFrame(cursor.fetchall())
        return df

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def generate_population_plot(population_df):
    """
    Generates a Plotly map for population data, including allele frequencies and sample sizes.

    Args:
        population_df (list of dict or pd.DataFrame): Population data with columns:
            - pop_id: Population ID
            - population_name: Population name
            - allele_frequency: Allele frequency
            - sample_size: Sample size

    Returns:
        str: Base64-encoded PNG image of the Plotly map.
    """
    if population_df.empty:
        return None

    # Convert input data to DataFrame
    df = pd.DataFrame(population_df)

    # Define population coordinates
    population_coords = {
        "1": {"lat": 51.5074, "lon": -0.1278},  # British Pakistani and Bangladeshi (UK)
        "2": {"lat": 7.8731, "lon": 80.7718},   # Sri Lankan Tamil (Sri Lanka)
        "3": {"lat": 20.5937, "lon": 78.9629},  # South Asian1 (India, general South Asia)
        "4": {"lat": 20.5937, "lon": 78.9629},  # South Asian2 (India, general South Asia)
        "5": {"lat": 36.2048, "lon": 138.2529}, # Japanese from Tokyo, Japan
        "6": {"lat": 23.6850, "lon": 90.3563},  # Bengali from Bangladesh
        "7": {"lat": 31.5204, "lon": 74.3587},  # Punjabi from Lahore, Pakistan
    }

    # Map coordinates to the DataFrame
    df["lat"] = df["pop_id"].astype(str).map(lambda x: population_coords.get(x, {}).get("lat"))
    df["lon"] = df["pop_id"].astype(str).map(lambda x: population_coords.get(x, {}).get("lon"))

    # Drop rows with missing coordinates
    df = df.dropna(subset=["lat", "lon"])

    # Generate Plotly map
    try:
        fig = px.scatter_geo(
            df,
            lat="lat",
            lon="lon",
            scope="world",
            size="sample_size",
            color="allele_frequency",
            hover_name="pop_name",
            projection="natural earth",
            title="Population Distribution in Asia"
        )

        # Save plot as base64-encoded image
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format="png")
        img_buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(img_buffer.read()).decode('utf-8')}"
    except Exception as e:
        print(f"Error generating plot: {e}")
        return None


if __name__ == "__main__":
    app.run(debug=True)