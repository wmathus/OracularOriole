from flask import Flask, render_template, request, Response, jsonify
import mysql.connector
from config import DB_CONFIG # Custom database config (e.g., host, user, password)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io # To keep in memory search (the past queries) We have to ask do we need to append search queries to sql and to then again backend to frontend!!
import base64 # This is needed for encoding the plot images in the website. Similarly if we want to import any image from google we'd need the URL to be in the frontend.  
import csv  
from flask import Response
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import send_from_directory

app = Flask(__name__)

def get_db_connection(): # Same as Aida's code only it returns an error if a connection isn't made. Better for future use.
    """Database connection with error handling"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err: # Displays the error type from MySql.
        print(f"Database connection error: {err}")
        return None

@app.route("/")
def home(): # Defines the home page where search hasn't been made. Nothing in the search results. No plot no results in the statistics section.
    return render_template("index.html", search_results=None, manhattan_url=None, population_map_url=None)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = ""  # Initialize query with a default value
    search_type = ""  # Initialize search_type with a default value
    population_type = ""
    if request.method == "POST":
        search_type = request.form.get("searchType")
        query = request.form.get("search_term", "").strip()
        population_type = request.form.get("population_type", "all")

    if not query:
        return render_template("index.html", search_results=None, manhattan_url=None, population_map_url=None)

    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
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

            # Fetch phenotype data for the given SNP
            cursor2 = connection.cursor(dictionary=True, buffered=True)
            cursor2.execute("""
                SELECT snp_id, phenotype_id
                FROM Phenotype_SNP
                WHERE snp_id = %s
            """, (query,))
            phenotype_results = cursor2.fetchall()
            cursor2.close()

        elif search_type == "gene":
            cursor.execute("""
                SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                FROM SNP_Gene
                JOIN SNPs ON SNP_Gene.snp_id = SNPs.snp_id
                JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                WHERE SNP_Gene.gene_id = %s
            """, (query,))
            results = cursor.fetchall()

            # Fetch phenotype data for the SNPs related to the gene
            snp_ids = [row["snp_id"] for row in results]
            if snp_ids:
                format_strings = ','.join(['%s'] * len(snp_ids))
                cursor2 = connection.cursor(dictionary=True, buffered=True)
                cursor2.execute(f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({format_strings})
                """, tuple(snp_ids))
                phenotype_results = cursor2.fetchall()
                cursor2.close()

        elif search_type == "chromosome":
            # Parse the query into chromosome and position range
            parts = query.split(":")
            chromosome = parts[0]
            
            if len(parts) == 1:
               start_pos, end_pos = None, None 
            else:
                position_part = parts[1] 
                # Handle position range
                
                if "-" in position_part:
        # Case: chromosome:start-end (e.g., "4:75576495-75576500")
                    position_parts = position_part.split("-")
                    if len(position_parts) == 2:
                        try:
                            start_pos = int(position_parts[0])
                            end_pos = int(position_parts[1])
                        except ValueError:
                            return render_template("error.html", message="Invalid position range. Expected format: 'chromosome:start-end'")
                else:
        # Case: chromosome:position (e.g., "4:75576495")
                    try:
                        start_pos = int(position_part)
                        end_pos = start_pos  # Treat single position as both start and end
                    except ValueError:
                        return render_template("error.html", message="Invalid position. Expected format: 'chromosome:position'")          

            # Fetch SNPs and genes based on the chromosome and position range
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
                # Fetch all SNPs and genes on the specified chromosome
                cursor.execute("""
                    SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
                    FROM SNPs
                    JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
                    JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
                    WHERE SNPs.chromosome = %s
                """, (chromosome,))
            results = cursor.fetchall()

            # Fetch phenotype data for the SNPs
            snp_ids = [row["snp_id"] for row in results]
            if snp_ids:
                format_strings = ','.join(['%s'] * len(snp_ids))
                cursor2 = connection.cursor(dictionary=True, buffered=True)
                cursor2.execute(f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({format_strings})
                """, tuple(snp_ids))
                phenotype_results = cursor2.fetchall()
                cursor2.close()

        if not results:
            error_message = "No results found for your query. Please try a different search term."
            return render_template("index.html",
                                   search_results=None,
                                   manhattan_url=None,
                                   phenotype_table_html=None,
                                   error_message=error_message)

        manhattan_url = generate_manhattan_plot(results) if results else None
        table_df = generate_phenotype_table(phenotype_results)
        population_results = fetch_population_results(query, search_type)
        phenotype_table_html = table_df.to_html(classes="table table-striped", index=False)
        filtered_population_results = filter_population_data(population_results, population_type)
        population_map_url = generate_population_plot()

        return render_template("index.html",
                               search_results=results,
                               manhattan_url=manhattan_url,
                               phenotype_table_html=phenotype_table_html,
                               population_results=filtered_population_results,
                               population_map_url=population_map_url,
                               error_message=None)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("error.html", message="Database query failed")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()

def fetch_population_results(query, search_type):
    """
    Fetches population results from the database based on the query and search type.

    Args:
        query (str): The search term (e.g., SNP ID, gene name, genomic location).
        search_type (str): The type of search ("snp", "gene", or "chromosome").

    Returns:
        list: List of dictionaries containing population data.
    """
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)

        if search_type == "snp":
            # Fetch population data for a specific SNP ID
            cursor.execute("""
                SELECT snp_id, pop_id, population_name, Ethnicity, sample_size, allele_frequency
                FROM Population
                WHERE snp_id = %s
            """, (query,))
        elif search_type == "gene":
            # Fetch population data for all SNPs associated with a gene
            cursor.execute("""
                SELECT p.snp_id, p.pop_id, p.population_name, p.Ethnicity, p.sample_size, p.allele_frequency
                FROM Population p
                JOIN SNP_Gene sg ON p.snp_id = sg.snp_id
                JOIN Gene_Functions gf ON sg.gene_id = gf.gene_id
                WHERE gf.gene_id = %s
            """, (query,))
        elif search_type == "chromosome":
            # Fetch population data for all SNPs in a specific genomic location
            cursor.execute("""
                SELECT p.snp_id, p.pop_id, p.population_name, p.Ethnicity, p.sample_size, p.allele_frequency
                FROM Population p
                JOIN SNPs s ON p.snp_id = s.snp_id
                WHERE s.chromosome = %s OR s.positions BETWEEN %s AND %s
            """, (query, query, query))  # Adjust the query for genomic location as needed
        else:
            return []  # Invalid search type

        population_results = cursor.fetchall()
        return population_results
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        if connection.is_connected(): connection.close()

def filter_population_data(population_results, population_type):
    """
    Filters population results based on the selected population type.

    Args:
        population_results (list): List of dictionaries containing population data.
        population_type (str): The selected population type (e.g., "tml", "bpb", "jpn", "brt", "all").

    Returns:
        list: Filtered list of population results.
    """
    if population_type == "all":
        return population_results  # Return all results if "all" is selected

    # Define a mapping of population types to population names
    population_mapping = {
        "slk": "South Asian",
        "bpb": "South Asian",
        "jpn": "East Asian",
    #    "brt": "European"
    }

    # Get the population name corresponding to the selected type
    population_name = population_mapping.get(population_type)

    if not population_name:
        return []  # Return an empty list if the population type is invalid

    # Filter the population results based on the population name
    filtered_results = [row for row in population_results if row.get("population_name") == population_name]

    return filtered_results     
   
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

@app.route("/download_csv") # Similar steps are taken as this needs to be defined as a new route. Why? Well, instead of this it is possible to do what Abi did with the initial template where he had to denote html.
def download_csv():
    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        def generate():
            data = io.StringIO()  # Creates an in-memory buffer (StringIO object) to store CSV data temporarily.
            writer = csv.writer(data) # Transform binary data to csv. Easy Peasy Lemon Squeeky.
            
            # Write header
            writer.writerow(['SNP_ID', 'Chromosome', 'Gene_Start' , 'Gene_End', 'P_Value', 'Odds_Ratio', 'Mapped Gene', 'Link'])
            yield data.getvalue() # Sends the row to the user. Remember this is a different route.
            data.seek(0) # reset and clear the buffer for the next row
            data.truncate(0)

            # Write rows from the results dictionary
            for row in results:
                writer.writerow([
                    row.get('snp_id', ''),
                    row.get('chromosome', ''),
                    row.get('gene_start', ''),
                    row.get('gene_end', ''),
                    row.get('p_value', ''),
                    row.get('odds_ratio', ''),
                    row.get('gene_id', ''),
                    row.get('link', ''),
                ])
                yield data.getvalue() # Writes each row 
                data.seek(0)
                data.truncate(0)

        response = Response(
            generate(), # This is the above function called.
            mimetype='text/csv', # Tells the browser what type of file it is.
            headers={'Content-Disposition': 'attachment; filename=snps_data.csv'} # Forces the browser to download the file with the name snps_data.csv
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
                gstart = float(row.get("gene_start", 1.0))
                gend = float(row.get("gene_end", 1.0))
                valid_data.append((chrom, gstart, gend, pval))
            except (ValueError, TypeError) as e:
                app.logger.error(f"Invalid data row: {row} - Error: {str(e)}")
                continue

        if not valid_data:
            return None

        # Create DataFrame from valid data
        valid_data = pd.DataFrame(valid_data, columns=["chromosome", "gstart", "gend", "p_value"])
        valid_data["midpoint"] = (valid_data["gstart"] + valid_data["gend"]) / 2    
        valid_data["-log10(p)"] = -np.log10(valid_data["p_value"])

        # Define colors for chromosomes
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "cyan", "magenta"]
        unique_chromosomes = valid_data["chromosome"].unique()
        chrom_color_map = {chrom: colors[i % len(colors)] for i, chrom in enumerate(unique_chromosomes)}

        # Create Manhattan plot
        plt.figure(figsize=(14, 8))
        for chrom in unique_chromosomes:
            subset = valid_data[valid_data["chromosome"] == chrom]
            plt.scatter(subset["midpoint"], subset["-log10(p)"], 
                        color=chrom_color_map[chrom], label=f"Chr {chrom}", alpha=0.6, edgecolors='w', linewidth=0.5)

        # Plot genome-wide significance line
        plt.axhline(y=-np.log10(5e-8), color='r', linestyle='--', linewidth=1, label="Genome-wide significance")

        # Add labels and grid
        plt.xlabel("Genomic Position")
        plt.ylabel("-log10(p-value)")
        plt.title("Manhattan Plot")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()  # Adjust layout to prevent overlap

        # Save plot to a buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)

        # Encode image to Base64 string
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        app.logger.error(f"Plot generation failed: {str(e)}")
        return None

def generate_phenotype_table(phenotype_results):
    try:
        if not phenotype_results:
            return pd.DataFrame(columns=["SNP ID", "Phenotype Name", "Phenotype Description"])

        # Convert the raw results to a Pandas DataFrame
        df = pd.DataFrame(phenotype_results)

        # Retrieve phenotype names and descriptions from the database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT phenotype_id, phenotype_name, phenotype_description 
                FROM Phenotype
            """)
            phenotype_info = cursor.fetchall()
            cursor.close()
            connection.close()

            phenotype_df = pd.DataFrame(phenotype_info)

            # Merge the phenotype information with the results
            df = df.merge(phenotype_df, on="phenotype_id", how="left")

            # Fill missing values for unknown phenotype names/descriptions
            df["phenotype_name"] = df["phenotype_name"].fillna("Unknown Phenotype")
            df["phenotype_description"] = df["phenotype_description"].fillna("No description available")

        else:
            df["phenotype_name"] = "Unknown Phenotype"
            df["phenotype_description"] = "No description available"

        # Keep only relevant columns for display
        df = df[["snp_id", "phenotype_name", "phenotype_description"]]
        df.rename(columns={"snp_id": "SNP ID", "phenotype_name": "Phenotype Name", "phenotype_description": "Phenotype Description"}, inplace=True)

        return df

    except Exception as e:
        print(f"Error generating phenotype table: {e}")
        return pd.DataFrame(columns=["SNP ID", "Phenotype Name", "Phenotype Description"])


    except Exception as e:
        print(f"Error generating phenotype table: {e}")
        return pd.DataFrame()
   



def generate_population_plot():

    connection = get_db_connection()
    
    if not connection: # Redirect to error html frontpage, if there is and issue with MySql. Daddy will work on how that will look like later kitten whiskers.
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Population")  
        population_data = cursor.fetchall()
        cursor.close()
        connection.close()

        # Debug: Check data
        print(f" Retrieved {len(population_data)} rows from database.")

        if not population_data:
            print("No population data found in database!")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(population_data)
        print(f" DataFrame created: {df.head()}")  # Print first few rows

        # Define coordinates for populations
        population_coords = {
            "South Asian": {"lat": 20.5937, "lon": 78.9629},
            "Sri Lankan": {"lat": 7.8731, "lon": 80.7718},
            "Japanese": {"lat": 36.2048, "lon": 138.2529}
        }

        # Add coordinates to the DataFrame
        df["lat"] = df["population_name"].map(lambda x: population_coords.get(x, {}).get("lat", None))
        df["lon"] = df["population_name"].map(lambda x: population_coords.get(x, {}).get("lon", None))

        # Debug: Check if lat/lon were added
        print(f" Updated DataFrame with lat/lon: {df.head()}")

        # Ensure no NaN values in lat/lon
        df = df.dropna(subset=["lat", "lon"])

        # Generate the map
        fig = px.scatter_geo(
            df,
            lat="lat",
            lon="lon",
            size="sample_size",
            color="allele_frequency",
            hover_name="population_name",
            projection="natural earth",
            title="Population Distribution in Asia"
        )

        # Convert figure to image
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format="png")  
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
        img_url = f"data:image/png;base64,{img_base64}"

        print(" Plot generated successfully!")
        return img_url  

    except Exception as e:
        print(f" Error generating population plot: {e}")
        return None

@app.route("/population_map", methods=["GET"])
def population_map():
    print(" Accessed /population_map route")  # Debugging log

    population_map_url = generate_population_plot()

    if not population_map_url:
        print("No population map generated!")
        return render_template("error.html", message="Failed to generate population map")

    print("Population map generated successfully, rendering template.")
    return render_template("index.html", population_map_url=population_map_url)




if __name__ == "__main__": # Debugging in the command prompt
    app.run(debug=True, host="0.0.0.0", port=8080)
