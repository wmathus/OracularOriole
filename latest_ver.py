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
    if request.method == "POST": # POST is often used to save username and password. The past queries are stored in the search bar. How it works for the frontend: (e.g., via an HTML <form> with method="POST")  
        search_type = request.form.get("searchType") # This bit is important because we need the plots for the pvalues to be drawn in the time of search submission (e.g., Manhattan plot, or other that you can think of). **We will use a similar structure for population stats. Keep that in mind pls.
        query = request.form.get("search_term", "").strip() # Strip = no unwanted spaces in the search pls >:( **A line can be added here for uppercase and lowercase queries. 
    else: # In the html if the search method is GET do the same exact same thing.
        search_type = request.args.get("searchType") # Don't worry about this! It is in case i assigned get as the method in the frontend. Basically a safety net because the frontend is getting complicated. Also to get URLs. I might instead add routes to searched SNP_IDs
        query = request.args.get("search_term", "").strip() # Strip = no unwanted spaces in the search pls >:(

    if not query: # Defines the home page where search hasn't been made. Nothing in the search results. The route here is different therefore this line is still necessary.
        return render_template("index.html", search_results=None, manhattan_url=None)

    connection = get_db_connection()
    if not connection: # Redirect to error html frontpage, if there is and issue with MySql. Daddy will work on how that will look like later kitten whiskers.
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True) # By default, cursor() returns rows as tuples. When dictionary=True is passed, rows are returned as dictionaries where: Keys are the column names. Values are the corresponding row values.
        
        if search_type == "snp":
            cursor.execute("""
            SELECT snps.snp_id, snps.chromosome, snps.p_value, snps.link, snp_genome.gene_id
            FROM snps
            LEFT JOIN snp_genome ON snps.snp_id = snp_genome.snp_id
            WHERE snps.snp_id = %s
            """, (query,))# Defines which table is to be used. This is why the SQL structure is very important.
        
        elif search_type == "gene":
            cursor.execute("""
            SELECT snps.snp_id, snps.p_value, snps.link, snps.chromosome, snp_genome.gene_id 
            FROM snp_genome 
            JOIN snps ON snp_genome.snp_id = snps.snp_id
            WHERE snp_genome.gene_id = %s 
            """, (query,)) #Select will create a template for the table. FROM will take the information from that table. Join will join the two tables temporarily, and rows
        
        elif search_type == "chromosome": #This needs to be added to the frontend (I think)
            cursor.execute("""
             SELECT snps.snp_id, snps.p_value, snps.link, snp_genome.gene_id, snps.chromosome
             FROM snps
             JOIN snp_genome ON snps.snp_id = snp_genome.snp_id
             WHERE snps.chromosome = %s
             """, (query,))
                           
        
        else:
            return render_template("index.html", search_results=None, manhattan_url=None) #Leaves the webpage blank, resets to home kinda.

        results = cursor.fetchall() # Calling cursor dictionary from above.
        print (results)
        
        manhattan_url = generate_manhattan_plot(results) if results else None # Calling the plot function, why this is called URL will be explained in the fumction below.
        
        return render_template("index.html",
                             search_results=results,
                             manhattan_url=manhattan_url)

    except mysql.connector.Error as err: 
        print(f"Database error: {err}") # Displays the error type from MySql.
        return render_template("error.html", message="Database query failed")
    finally: # This ensures that resources are released and connections are closed.  
        if 'cursor' in locals(): cursor.close() # Regardless of if the cursor is empty or full. The connection is closed. It might give an error if it is empty otherwvise.
        if connection.is_connected(): connection.close() # If the connection is already closed (e.g., due to an error), calling connection.close() again would raise an exception. Hence "is_connected". 
        # MySQL has a database connection limit, which is controlled by the "max_connections" system variable; this defines the maximum number of simultaneous client connections allowed to connect to the MySQL server, and the default value is usually around 151 connections depending on the MySQL version. 
        # Consider adding this if the function won't be necessarily continuosly used.


@app.route("/download_csv") # Similar steps are taken as this needs to be defined as a new route. Why? Well, instead of this it is possible to do what Abi did with the initial template where he had to denote html.
def download_csv():
    connection = get_db_connection()
    if not connection:
        return render_template("error.html", message="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True) # This should be clearer as it is almost the same with the search method, only some packages needed to be imported.
        cursor.execute("SELECT * FROM snps")  # Note that the table name from the SQL is snps and the header row is in the same order as the order comes from the table.
        results = cursor.fetchall() # All rows are retrieved, rows are SNPs in this case. See mysql to use other tables for fumctions that retrieve gene function. After that has been mapped.

        def generate():
            data = io.StringIO()  # Creates an in-memory buffer (StringIO object) to store CSV data temporarily.
            writer = csv.writer(data) # Transform binary data to csv. Easy Peasy Lemon Squeeky.
            
            # Write header
            writer.writerow(['SNP_ID', 'Chromosome', 'Alternate_allele' , 'P_Value', 'Odds_ratio', 'source', 'link'])
            yield data.getvalue() # Sends the row to the user. Remember this is a different route.
            data.seek(0) # reset and clear the buffer for the next row
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

if __name__ == "__main__": # Debugging in the command prompt
    app.run(debug=True, host="0.0.0.0", port=8080)
