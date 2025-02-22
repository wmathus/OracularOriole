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
    return render_template("index.html", search_results=None, manhattan_url=None)

@app.route("/search", methods=["GET", "POST"]) # **The POST option is required so that we can save the query submission for further analysis. GET only displays the table.
def search():
    query = ""  # Initialize query with a default value; for gene info back to search function
    search_type = ""  # Initialize search_type with a default value; for gene info back to search function
    
    if request.method == "POST": # POST is often used to save username and password. The past queries are stored in the search bar. How it works for the frontend: (e.g., via an HTML <form> with method="POST")  
        search_type = request.form.get("searchType") # This bit is important because we need the plots for the pvalues to be drawn in the time of search submission (e.g., Manhattan plot, or other that you can think of). **We will use a similar structure for population stats. Keep that in mind pls.
        query = request.form.get("search_term", "").strip() # Strip = no unwanted spaces in the search pls >:( **A line can be added here for uppercase and lowercase queries. Nevermind SQL handles them. 
   

    if not query: # Defines the home page where search hasn't been made. Nothing in the search results. The route here is different therefore this line is still necessary.
        return render_template("index.html", search_results=None, manhattan_url=None)

    connection = get_db_connection()
    if not connection: # Redirect to error html frontpage, if there is and issue with MySql. Daddy will work on how that will look like later kitten whiskers.
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        if search_type == "snp":
            cursor.execute("""
            SELECT SNPs.snp_id, SNPs.chromosome, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
            FROM SNPs
            LEFT JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
            LEFT JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
            WHERE SNPs.snp_id = %s
            """, (query,))
         
         # Fetch raw phenotype data for the given SNP from your phenotype table
         
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
            
            # For phenotype data in the gene search, first extract the SNP IDs from the results
           # snp_results_temp = cursor.fetchall()
           # snp_ids = [row["snp_id"] for row in snp_results_temp]
            # Reset the cursor with the SNP results to be used later
            global results
            snp_results_temp = cursor.fetchall()
            print("Fetched SNP Results:", snp_results_temp)  # Debugging

            if not snp_results_temp:
                print("No SNP results found for the given query")
                return render_template("index.html", search_results=None, phenotype_table_html=None)

            snp_ids = [row["snp_id"] for row in snp_results_temp]
            results = snp_results_temp  # Store for later use
            print(results)

            if snp_ids:
                cursor2 = connection.cursor(dictionary=True, buffered=True)
                # Use IN clause to get phenotype data for all SNPs related to the gene
                format_strings = ','.join(['%s'] * len(snp_ids))
                phenotype_query = f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({format_strings})
                    """
                print("Phenotype Query:", phenotype_query)  # Print generated query
                print("Query Parameters:", tuple(snp_ids))
                cursor2.execute(phenotype_query, tuple(snp_ids))
                phenotype_results = cursor2.fetchall()
                cursor2.close()
                print("Phenotype Results:", phenotype_results)
            else:
                print("No SNPs found for the given query.")
                phenotype_results = []

            # Since we already fetched the results above, skip the default fetch later.
            cursor = None

        
        elif search_type == "chromosome":
            cursor.execute("""
            SELECT SNPs.snp_id, SNPs.p_value, SNPs.odds_ratio, SNPs.link, SNPs.chromosome, SNP_Gene.gene_id, Gene_Functions.gene_start, Gene_Functions.gene_end
            FROM SNPs
            JOIN SNP_Gene ON SNPs.snp_id = SNP_Gene.snp_id
            JOIN Gene_Functions ON SNP_Gene.gene_id = Gene_Functions.gene_id
            WHERE SNPs.chromosome = %s OR Gene_Functions.gene_start = %s OR Gene_Functions.gene_end = %s
            """, (query,query,query))
           
            # For phenotype data in chromosome search, extract SNP IDs first
            snp_results_temp = cursor.fetchall()
            snp_ids = [row["snp_id"] for row in snp_results_temp]
            results = snp_results_temp

            if snp_ids:
                cursor2 = connection.cursor(dictionary=True, buffered=True)
                format_strings = ','.join(['%s'] * len(snp_ids))
                phenotype_query = f"""
                    SELECT snp_id, phenotype_id
                    FROM Phenotype_SNP
                    WHERE snp_id IN ({format_strings})
                    """
                cursor2.execute(phenotype_query, tuple(snp_ids))
                phenotype_results = cursor2.fetchall()
                cursor2.close()
            else:
                phenotype_results = []
            cursor = None  # results already captured          
        
        #else:
         #   return render_template("index.html", search_results=None, manhattan_url=None) #Leaves the webpage blank, resets to home kinda.

       # else:
       #     return render_template("index.html", search_results=None, manhattan_url=None, phenotype_table_html=None)
        # To be able to use the results table in the download function. This globalizes the variable.
        # If we haven't already set results (for gene and chromosome, we set it already)
              
        if cursor is not None:
            results = cursor.fetchall()
            
        # If no valid search_type was found, return empty page
        if search_type not in ["snp", "gene", "chromosome"]:
            return render_template("index.html", search_results=None, manhattan_url=None, phenotype_table_html=None)

   
        manhattan_url = generate_manhattan_plot(results) if results else None # Calling the plot function, why this is called URL will be explained in the fumction below.
        # Generate phenotype pie chart URL from raw data (if available)
        # Generate the phenotype table DataFrame using your helper function
        table_df = generate_phenotype_table(phenotype_results)

        # Convert the DataFrame to an HTML table.
        # You can add Bootstrap classes (or your own) for styling.
        phenotype_table_html = table_df.to_html(classes="table table-striped", index=False)

        return render_template("index.html",
                       search_results=results,
                       manhattan_url=manhattan_url,
                       phenotype_table_html=phenotype_table_html)
        # ... you could include similar logic for other search types (e.g., gene, chromosome)
        
    except mysql.connector.Error as err: 
        print(f"Database error: {err}") # Displays the error type from MySql.
        return render_template("error.html", message="Database query failed")
    finally: # This ensures that resources are released and connections are closed.  
        if 'cursor' in locals() and cursor is not None: cursor.close() # Regardless of if the cursor is empty or full. The connection is closed. It might give an error if it is empty otherwvise.
        if connection.is_connected(): connection.close() # If the connection is already closed (e.g., due to an error), calling connection.close() again would raise an exception. Hence "is_connected". 
        # MySQL has a database connection limit, which is controlled by the "max_connections" system variable; this defines the maximum number of simultaneous client connections allowed to connect to the MySQL server, and the default value is usually around 151 connections depending on the MySQL version. 
        # Consider adding this if the function won't be necessarily continuosly used.

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

def generate_manhattan_plot(results): # Truth be told this can be replaced with any other statistics you come up with. Improvement point: Add this to the search route so that all queries can be compared with one another.
    try: # Not terribly important if you have a better idea, add whatever stats you see fit. Placeholder at the moment. Keep in mind io to temporarily play with the data here and base 64 need to be used to display the graph (Binary to URL).  
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
        valid_data = pd.DataFrame(valid_data, columns=["chromosome", "gstart", "gend", "p_value"])
        valid_data["midpoint"] = (valid_data["gstart"] + valid_data["gend"]) / 2    
        valid_data["-log10(p)"] = -np.log10(valid_data["p_value"])
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "cyan", "magenta"]
    # chromosomes, p_values = zip(*valid_data)# Plot each chromosome separately

        unique_chromosomes = valid_data["chromosome"].unique()
        chrom_color_map = {chrom: colors[i % len(colors)] for i, chrom in enumerate(unique_chromosomes)}

        # Create Manhattan plot
        plt.figure(figsize=(14, 8))
        for chrom in unique_chromosomes:
            subset = valid_data[valid_data["chromosome"] == chrom]
            plt.scatter(subset["midpoint"], subset["-log10(p)"], 
                        color=chrom_color_map[chrom], label=f"Chr {chrom}", alpha=0.6, edgecolors='w', linewidth=0.5)

        plt.axhline(y=-np.log10(5e-8), color='r', linestyle='--', linewidth=1, label="Genome-wide significance")
        # Convert chromosomes to numeric indices
       # unique_chrom = sorted(set(chromosomes), key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
       # chrom_dict = {chrom: idx+1 for idx, chrom in enumerate(unique_chrom)}
       # numeric_chrom = [chrom_dict[chrom] for chrom in chromosomes]

        # Create plot
        plt.figure(figsize=(14, 8))

        
        plt.axhline(y=-np.log10(5e-8), color='r', linestyle='--', linewidth=1)


        plt.xlabel("Genomic Position")
        plt.ylabel('-log10(p-value)') 
        plt.title('Manhattan Plot')
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.grid(True, alpha=0.3)

        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        
        return f"data:image/png;base64,{base64.b64encode(img_buffer.read()).decode('utf-8')}" # The URL

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

population_data = {
    "population_code": ["SAS"] * 60,
    "population_name": ["South Asian"] * 60,
    "Ethnicity": ["BPB"] * 6 + ["N/A"] * 20 + ["BPB?"] * 34,
    "snp_id": ["rs7903146", "rs10830963", "rs2972145", "rs7756992", "rs2191349", "rs9854769",
               "rs7531962", "rs12463719", "rs7432739", "rs7626079", "rs62366901", "rs74790763",
               "rs7765207", "rs73689877", "rs2980766", "rs62486442", "rs13257283", "rs2488597",
               "rs2114824", "rs10748694", "rs7123361", "rs9568861", "rs76141923", "rs28790585",
               "rs7261425", "rs2065703", "rs11708067", "rs9808924", "rs7766070", "rs10184004",
               "rs2203452", "rs1260326", "rs35142762", "rs12655753", "rs17036160", "rs13094957",
               "rs10916784", "rs61748094", "rs329122", "rs2714343", "rs6813195", "rs3775087",
               "rs13130845", "rs7629245", "rs3887925", "rs13066678", "rs935112", "rs76263492",
               "rs62259319", "rs1393202", "rs12746673", "rs59689207", "rs61818951", "rs7579323",
               "rs1012311", "rs10864859", "rs13387347", "rs16849467", "rs9873519", "rs1514895",
               ],
    "allele_freq": [0.75, 0.29, 0.54, 0.41, 0.11, 0.32, 0.28, 0.64, 0.60, 0.94, 0.39, 0.12, 0.48, 0.34, 0.92, 0.84, 0.47, 0.42, 0.69, 0.15, 0.01, 0.33, 0.71, 0.15, 0.782, 0.43, 0.266, 0.741, 0.757, 0.754, 0.857, 0.889, 0.881, 0.76, 0.559, 0.967, 0.383, 0.463, 0.618, 0.201, 0.702, 0.24, 0.549, 0.44, 0.882, 0.039, 0.412, 0.052, 0.147, 0.142, 0.044, 0.755, 0.402, 0.941, 0.403, 0.637, 0.286, 0.721, 0.297, 0.164],
    "sample_size": [22490] * 6 + [197391, 272634, 197391, 197391, 197080, 272634, 197391, 272634, 264876, 190682, 272634, 272634, 271738, 272634, 228651, 272634, 186208, 197391] * 3
}

# Create a DataFrame
df = pd.DataFrame(population_data)
def generate_population_plot(df):
    try:
        # Aggregate data by population
        aggregated_data = df.groupby('population_name').agg({
            'allele_freq': 'mean',
            'sample_size': 'sum'
        }).reset_index()

        # Map population names to coordinates (latitude and longitude)
        population_coords = {
            "South Asian": {"lat": 20.5937, "lon": 78.9629}
        }

        # Add coordinates to the DataFrame
        aggregated_data['lat'] = aggregated_data['population_name'].map(lambda x: population_coords[x]['lat'])
        aggregated_data['lon'] = aggregated_data['population_name'].map(lambda x: population_coords[x]['lon'])

        # Create the map using Plotly Express
        fig = px.scatter_geo(aggregated_data,
                             lat='lat',
                             lon='lon',
                             size='sample_size',
                             color='allele_freq',
                             hover_name='population_name',
                             projection="natural earth",
                             title='Worldwide Population Distribution')

        # Optionally show the map in a browser (can be commented out in production)
        # fig.show()

        # Save the map to a file. Here, we're saving to the "templates" folder so that Flask's render_template can find it.
       # fig.write_html("templates/map.html")
       # return True
        # Save the plot as a PNG image
        # Convert the plot to a base64-encoded image
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format="png")  # Use kaleido to save as PNG
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        img_url = f"data:image/png;base64,{img_base64}"
        print("Figure generated successfully!")
        return img_url  # Return the base64-encoded image URL

    except Exception as e:
        print(f"Error generating population plot: {e}")
        return None
# Define the route globally
@app.route("/population_map")
def population_map():
    # Generate the population plot and get the base64-encoded image URL
    population_map_url = generate_population_plot(df)
    if not population_map_url:
        return render_template("error.html", message="Failed to generate population map")

    # Pass the image URL to the template
    return render_template("index.html", population_map_url=population_map_url)

@app.route("/other_population_data")
def other_population_data():
    # Add the logic for this endpoint
    return render_template("None")

if __name__ == "__main__": # Debugging in the command prompt
    app.run(debug=True, host="0.0.0.0", port=8080)
