import mysql.connector
import pandas as pd
import plotly.express as px
import io
import base64
from flask import Flask
from config import DB_CONFIG
app = Flask(__name__)

def get_db_connection(): # Same as Aida's code only it returns an error if a connection isn't made. Better for future use.
    """Database connection with error handling"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err: # Displays the error type from MySql.
        print(f"Database connection error: {err}")
        return None

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


def generate_population_df(population_results):
    """Generates a DataFrame with allele frequencies and sample sizes."""
    if not population_results:
        print("🔴 No population results! Returning empty DataFrame.")
        return pd.DataFrame()

    connection = get_db_connection()
    if not connection:
        return pd.DataFrame()

    try:
        cursor = connection.cursor(dictionary=True)

        # Extract unique population IDs
        pop_ids = [str(row["pop_id"]) for row in population_results]
        pop_ids_str = ",".join(pop_ids)

        # Fetch allele frequencies and sample sizes for all populations
        cursor.execute(f"""
            SELECT sp.snp_id, pa.pop_id, pa.allele_frequency, p.pop_name, p.sample_size
            FROM Population_Allele pa
            JOIN Population p ON pa.pop_id = p.pop_id
            JOIN SNP_Population sp ON pa.pop_id = sp.pop_id
            WHERE pa.pop_id IN ({pop_ids_str})
        """)

        df = pd.DataFrame(cursor.fetchall())
        print(f"🟢 Population DataFrame: {df}")  # Debugging

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
        print("Error: population_df is empty.")
        return None

    print("Population DataFrame:")
    print(population_df)

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
