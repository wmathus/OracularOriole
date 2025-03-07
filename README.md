# T2D Oracle: A Web Tool for Type 2 Diabetes Genomics  

## Project Overview  
T2D Oracle is a web-based application designed to retrieve and analyze genetic variants associated with Type 2 Diabetes (T2D). It integrates SNP data with population genomics and functional annotations to explore genetic susceptibility, with a focus on South Asian populations.  

## Features  
- **SNP Lookup**: Search for T2D-associated SNPs by ID, genomic location, or mapped gene.  
- **Genomic Insights**: Displays SNP positions, association statistics, and mapped genes.  
- **Population Genetics**: Integrates selection summary statistics for South Asian populations.  
- **Functional Annotations**: Retrieves gene ontology terms for selected genes.  
- **Visualization**: Generates plots for genomic selection signals.  
- **Data Export**: Allows users to download summary statistics.  

## Project Structure  
T2D-Oracle/ ├── SQL_Data/ │ ├── readmesql.txt # Database connection details
│ ├── sql8762368.sql # Database schema
│ ├── flask_session/ # Session storage
│ ├── images/ # Image assets
│ ├── background.png
│ ├── oriole.png
│ ├── templates/ # HTML templates
│ ├── error.html # Error handling page
│ ├── gene_info.html # Gene information page
│ ├── index.html # Main UI page
│ ├── .gitignore # Git ignore file
├── README.md # Project documentation
├── config.py # Configuration settings
├── latest_ver.py # Main application logic
├── plotting_functions.py # Data visualization functions
├── pop_func.py # Population genetics calculations
├── requirements.txt # Python dependencies

## Installation & Setup  

### Clone the Repository  
```sh
git clone https://github.com/your-repo/T2D-Oracle.git
cd T2D-Oracle

### Ensure Python is installed, then run:
pip install -r requirements.txt


### Configure the Database
Connect to the MySQL database using the credentials in readmesql.txt, OR execute sql8762368.sql to set up the schema on local.

### Run the Application
python latest_ver.py
The web app will be available at http://192.168.0.49:8080

## Data Sources
####GWAS Catalog: EBI GWAS
####T2D Knowledge Portal: T2D Portal
####International Genome Samples Resource: IGSR

Contributors
Developed as part of the MSc Bioinformatics Software Development Group Project at Queen Mary University of London.
