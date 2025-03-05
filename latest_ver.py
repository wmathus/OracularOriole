from flask import Flask, render_template, request, Response, jsonify
from config import DB_CONFIG # Custom database config (e.g., host, user, password)
import mysql.connector
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
from pop_func import fetch_population_id, generate_population_df, generate_population_plot
from flask import session, redirect, url_for
import seaborn as sns
from plotting_functions import plot_tajima_d_by_chromosome, plot_fst_heatmap, plot_tajima_d_all_chromosomes, plot_tajima_d_histogram
from flask_session import Session

app = Flask(__name__)
app.secret_key = "oriole"
# Configure server-side session storage
# Configure session to use filesystem (store session data on the server)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False  # Optional: session expires on browser close
app.config["SESSION_FILE_DIR"] = "./flask_session"  # Folder to store session files

Session(app)

def get_db_connection(): # Same as Aida's code only it returns an error if a connection isn't made. Better for future use.
    """Database connection with error handling"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err: # Displays the error type from MySql.
        print(f"Database connection error: {err}")
        return None


@app.route('/')
def home():
    # Retrieve sidebar state from session (default to False if not set)
    sidebar_hidden = session.get('sidebar_hidden', False)
    
    return render_template("index.html", 
                           search_results=None, 
                           manhattan_url=None, 
                           population_map_url=None,
                           chromosome=None, 
                           sidebar_hidden=sidebar_hidden) 


@app.route('/hide_sidebar')
def hide_sidebar():
    session['sidebar_hidden'] = True  # Set sidebar as hidden
    return redirect(url_for('home'))

@app.route('/show_sidebar')
def show_sidebar():
    session['sidebar_hidden'] = False  # Reset sidebar visibility
    return redirect(url_for('home'))

@app.route("/search", methods=["GET", "POST"])
def search():
    query = ""  # Initialize query with a default value
    search_type = ""  # Initialize search_type with a default value
    population = ""
    if request.method == "POST":
        search_type = request.form.get("searchType")
        query = request.form.get("search_term", "").strip()
        population = request.args.get("population")

    if not query:
        return render_template("index.html", search_results=None, manhattan_url=None, population_map_url=None, population_type=None, chromosome=None)

    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        global results
        results = []
        phenotype_results = []
        session["results"] = results 
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
            return render_template("index.html", search_results=None, pop_results=None, error_message="No results found.")

        chromosome = results[0]["chromosome"]
        
        # Fetch population results
        population_results = fetch_population_id(query, search_type)

        # Filter and append population names
        

        # Generate DataFrame with allele frequencies, sample sizes, SNP IDs, and population names
        pop_results = generate_population_df(population_results)
        population_map_url = generate_population_plot(pop_results)
        # Convert phenotype results to HTML table
        phenotype_table_html = pd.DataFrame(phenotype_results).to_html(classes="table table-striped", index=False)
        session["pop_results"] = pop_results
        session["population_map_url"] = population_map_url
        session["results"] = results 
        
        session["population_map_url"] = population_map_url
        session["phenotype_table_html"] = phenotype_table_html
        
        chr_taj = list(range(1, 15)) + [15, 20]
        if chromosome not in chr_taj:
            return render_template("index.html", search_results=results, population_map_url=population_map_url, error_message=f"No Tajima's D data found for Chromosome {chromosome}.", chromosome=chromosome, selected_population=population)


        # Render template with results
        return render_template(
            "index.html",
            search_results=results,
            selected_population=population,
            chromosome=chromosome,
            sidebar_hidden=True,
            phenotype_table_html=phenotype_table_html,
            pop_results=pop_results,
            population_map_url=population_map_url,
            error_message=None
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("index.html", search_results=None, pop_results=None, error_message="Database query failed.")
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
        SELECT Gene_Functions.gene_id, Gene_Functions.gene_description, Gene_Functions.gene_start, Gene_Functions.gene_end, SNP_Gene.snp_id, Gene_GO.go_id, Gene_GO.go_description
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
   

def fetch_fst_data():
    """Fetches FST data from MySQL and returns it as a DataFrame."""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Fixation")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        if not rows:
            print("No FST data found.")
            return None
        
        # Convert fetched data into Pandas DataFrame
        df = pd.DataFrame(rows)
        return df

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    
def fetch_tajimas_d_data():
    pop_id_to_population = {
    6: "BEB",
    7: "PJL",
    2: "STU",  # Might be SLK
}
    """
    Fetch Tajima's D data from the MySQL database and return it as a pandas DataFrame.
    """
    connection = get_db_connection()
    #query = "SELECT * FROM all_tajimas"
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        

        # Query to get all Tajima's D data from the "all_tajimas" table
        cursor.execute("""SELECT * FROM TajimasD""")
        rows = cursor.fetchall()

        # # Print the fetched rows to debug
        # print("Fetched rows:", rows)
        # If no data found, return None
        if not rows:
            return None
        
        for row in rows:
            pop_id = row.get("pop_id")
            if pop_id in pop_id_to_population:
                row["POPULATION"] = pop_id_to_population[pop_id]
            else:
                row["POPULATION"] = "Unknown"  # Default value for unknown pop_ids
        # Convert the result into a pandas DataFrame
            if "bin_start" in row:
                row["BIN_START_Mb"] = row["bin_start"] / 1_000_000  # Convert bp to Mb
        df = pd.DataFrame(rows)
        print (df)
        return df

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if 'cursor' in locals() and cursor is not None: cursor.close()
        if connection.is_connected(): connection.close()

def process_results_for_plotting():
    """
    Extracts relevant information from the global `results` variable,
    converts it into a DataFrame, and transforms gene start positions into megabases.
    This is later used to try and plot the lines per SNP in the individual Taj manhattan plot.
    Can be removed if we find another way to annotate the SNP's present in plots!

    Returns:
        pd.DataFrame: Processed DataFrame with required columns.
    """
    if not results:
        print("No results found to process.")
        return pd.DataFrame()  # Return an empty DataFrame if results are empty

    processed_data = [
        {"snp_id": entry["snp_id"], "chromosome": entry["chromosome"], "gene_id": entry["gene_id"], "gene_start_mb": entry["gene_start"] / 1_000_000, 
         "gene_end_mb": entry["gene_end"] / 1_000_000}
        for entry in results
    ]

    # Convert dictionaries to DataFrame
    df_processed = pd.DataFrame(processed_data)

    return df_processed

@app.route("/search/tajima_d_by_chromosome", methods=["GET"])
def tajima_d_by_chromosome_route():
    chromosome = request.args.get("chromosome")  
    population = request.args.get("population")  

    if not chromosome or not population:
        return render_template("error.html", message="Please provide both chromosome and population.")

    df = fetch_tajimas_d_data()
    filtered_df = df[(df["chromosome"].astype(str) == str(chromosome)) & (df["POPULATION"] == population)]

    if filtered_df.empty:
        return render_template("error.html", message="No data found for the specified chromosome and population.")

    img_url = plot_tajima_d_by_chromosome(chromosome, population, filtered_df)
    tajima_histogram_url = plot_tajima_d_histogram(population, df)
    df_fst = fetch_fst_data()

    # Generate image URLs
    tajima_all_chromosomes_url = plot_tajima_d_all_chromosomes(population, df)
    tajima_histogram_url = plot_tajima_d_histogram(population, df)
    fst_heatmap_url = plot_fst_heatmap(df_fst)


    if not img_url:
        return render_template("error.html", message="Failed to generate the plot.")

    # Store session variables
    session["chromosome"] = chromosome
    session["population"] = population
    session["histogram_url"] = tajima_histogram_url
    session["tajima_all_chromosomes_url"] = tajima_all_chromosomes_url  
    session["fst_heatmap_url"] = fst_heatmap_url

    results = session.get("results", [])

    # Render template with results
    return render_template(
        "index.html",
        search_results=results,
        selected_population=population,
        chromosome=chromosome,
        tajima_all_chromosomes_url=session.get("tajima_all_chromosomes_url"),
        histogram_url=session.get("histogram_url"),
        fst_heatmap_url=session.get("fst_heatmap_url"),
        manhattan_url=img_url,
        population_map_url=session.get("population_map_url"),  # Ensure this variable is stored in session
        sidebar_hidden=True,
        phenotype_table_html=session.get("phenotype_table_html", ""),
        pop_results=session.get("pop_results", []),
        error_message=None
    )

@app.route("/download/tajima_d_by_chromosome", methods=["GET"])
def download_taj_by_chromosome():
    chromosome = request.args.get("chromosome")
    population = request.args.get("population")

    if not chromosome or not population:
        return "Chromosome and population are required.", 400

    df = fetch_tajimas_d_data()
    filtered_df = df[(df["chromosome"] == int(chromosome)) & (df["POPULATION"] == population)]

    # Calculate gene and chromosome stats, filling N/A with 0
    gene_stats = filtered_df.groupby("gene_id").agg({"tajimas_d": ["mean", "std"]})
    chromosome_stats = filtered_df.groupby("chromosome").agg({"tajimas_d": ["mean", "std"]})
    gene_stats["tajimas_d", "std"] = gene_stats["tajimas_d", "std"].fillna(0)
    chromosome_stats["tajimas_d", "std"] = chromosome_stats["tajimas_d", "std"].fillna(0)

    # Convert both gene_stats and chromosome_stats to CSV format
    output = io.StringIO()  # Create an in-memory text stream
    writer = csv.writer(output)

    # Write headers for gene stats
    writer.writerow(['gene_id', 'mean_tajimas_d', 'std_tajimas_d'])
    for index, row in gene_stats.iterrows():
        writer.writerow([index, row[('tajimas_d', 'mean')], row[('tajimas_d', 'std')]])

    writer.writerow([])  # Blank row to separate the two tables

    # Write headers for chromosome stats
    writer.writerow(['chromosome', 'mean_tajimas_d', 'std_tajimas_d'])
    for index, row in chromosome_stats.iterrows():
        writer.writerow([index, row[('tajimas_d', 'mean')], row[('tajimas_d', 'std')]])

    # Set the file pointer to the start of the file
    output.seek(0)

    # Send the generated CSV as a response to download
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={population}_tajima_by_chromosome_{chromosome}_stats.csv"}
    )


@app.route("/tajima_d_all_chromosomes/<population>")
def tajima_d_all_chromosomes_route(population):
    df_tajima = fetch_tajimas_d_data()
    df_fst = fetch_fst_data()

    # Generate image URLs
    tajima_all_chromosomes_url = plot_tajima_d_all_chromosomes(population, df_tajima)
    tajima_histogram_url = plot_tajima_d_histogram(population, df_tajima)
    fst_heatmap_url = plot_fst_heatmap(df_fst)

    # Store URLs in session to retain data across requests
    session["tajima_all_chromosomes_url"] = tajima_all_chromosomes_url
    session["histogram_url"] = tajima_histogram_url
    session["fst_heatmap_url"] = fst_heatmap_url
    session["population"] = population

    return render_template("index.html", 
                           manhattan_url=session.get("manhattan_url"),
                           histogram_url=session.get("histogram_url"),
                           fst_heatmap_url=session.get("fst_heatmap_url"),
                           tajima_all_chromosomes_url=session.get("tajima_all_chromosomes_url"),
                           population=population)



if __name__ == "__main__": # Debugging in the command prompt
    app.run(debug=True, host="0.0.0.0", port=8080)



if __name__ == "__main__": # Debugging in the command prompt
    app.run(debug=True, host="0.0.0.0", port=8080)
