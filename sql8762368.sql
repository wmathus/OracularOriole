-- *********************************************************************
-- *          T2D_Genetics Database Schema & Testing Queries          *
-- *   This script creates a MySQL database to store SNP data for     *
-- *      Type 2 Diabetes (T2D) research, linking SNPs, genes,        *
-- *     populations, phenotypes, and selection statistics.           *
-- *                                                                 *
-- *   It includes schema creation, indexing for optimization,       *
-- *      testing queries, and sample data insertion.                 *
-- *********************************************************************

-- ====================================================================
-- 1. Drop the existing database if it exists, and create a new one
-- ====================================================================

CREATE DATABASE sql8762368 ;
USE sql8762368 ;

-- ====================================================================
-- 2. Table Definitions
-- ====================================================================

-- --------------------------------------------------------
-- SNPs Table: Stores information about Single Nucleotide Polymorphisms (SNPs)
-- --------------------------------------------------------
CREATE TABLE SNPs (
    snp_id VARCHAR(50) PRIMARY KEY,  -- Unique identifier for each SNP
    chromosome INT NOT NULL,         -- Chromosome number where SNP is located
    position INT NOT NULL,           -- Genomic position of the SNP
    reference_allele CHAR(1),        -- Reference allele
    effector_allele CHAR(1),         -- Effect allele (linked to disease risk)
    p_value FLOAT,                   -- P-value from statistical association studies
    odds_ratio FLOAT,                -- Odds ratio indicating disease risk
    source VARCHAR(255),             -- Source of the SNP data (e.g., GWAS)
    link VARCHAR(255),               -- Reference link to SNP study
    INDEX idx_snp_chromosome (chromosome, position)  -- Index for optimised SNP lookups
);

-- --------------------------------------------------------
-- Population Table: Stores information about different populations
-- --------------------------------------------------------
CREATE TABLE Population (
    pop_id INT PRIMARY KEY AUTO_INCREMENT,  -- Unique population ID (auto-increment meanign automatically do 1,2,3.. )
    pop_name VARCHAR(255) NOT NULL,         -- Name of the population group
    sample_size INT NOT NULL                -- Sample size of the population in the study
);

-- --------------------------------------------------------
-- Population_Allele Table: Stores allele frequencies within populations
-- --------------------------------------------------------
CREATE TABLE Population_Allele (
    pop_allele_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for the allele frequency record
    pop_id INT NOT NULL,  -- Foreign key linking to Population table
    allele_frequency DECIMAL(5,4) NOT NULL,  -- Frequency of a specific allele in a population
    FOREIGN KEY (pop_id) REFERENCES Population(pop_id) ON DELETE CASCADE
    -- If a population is deleted, all related allele frequency records will be deleted as well (hence ON DELETE CASCADE)
);

-- --------------------------------------------------------
-- SNP_Population Table: Many-to-Many relationship between SNPs and Population groups
-- --------------------------------------------------------
CREATE TABLE SNP_Population (
    snp_id VARCHAR(50), -- Foreign key linking to SNPs table
    pop_id INT,         -- Foreign key linking to Population table
    FOREIGN KEY (snp_id) REFERENCES SNPs(snp_id) ON DELETE CASCADE,
    -- If an SNP is deleted, all its population associations will also be deleted
    FOREIGN KEY (pop_id) REFERENCES Population(pop_id) ON DELETE CASCADE,
    -- If a population is deleted, all SNP associations with that population will be removed
    PRIMARY KEY (snp_id, pop_id),
    INDEX idx_snp_population (snp_id, pop_id) -- Optimised for searching SNPs by population
);

-- --------------------------------------------------------
-- Gene_Functions Table: Stores gene-related information
-- --------------------------------------------------------
CREATE TABLE Gene_Functions (
    gene_id VARCHAR(50) PRIMARY KEY, -- Unique identifier for each gene
    chromosome INT NOT NULL,         -- Chromosome number
    gene_start INT NOT NULL,         -- Start position of the gene
    gene_end INT NOT NULL,           -- End position of the gene
    gene_description TEXT,           -- Description of the gene function
    INDEX idx_gene_chromosome (chromosome, gene_start, gene_end) -- Optimised for searching genes by region
);

-- --------------------------------------------------------
-- Gene_GO Table: Stores Gene Ontology (GO) annotations
-- --------------------------------------------------------
CREATE TABLE Gene_GO (
    gene_id VARCHAR(50),  -- Foreign key referencing Gene_Functions table
    go_id VARCHAR(50),    -- Gene Ontology ID
    go_description TEXT,  -- Description of the GO annotation
    PRIMARY KEY (gene_id, go_id),
    FOREIGN KEY (gene_id) REFERENCES Gene_Functions(gene_id) ON DELETE CASCADE
    -- If a gene is deleted, all its Gene Ontology associations will also be removed
);

-- --------------------------------------------------------
-- SNP_Gene Table: Establishes relationships between SNPs and Genes
-- --------------------------------------------------------
CREATE TABLE SNP_Gene (
    snp_id VARCHAR(50),  -- Foreign key referencing SNPs
    gene_id VARCHAR(50), -- Foreign key referencing Gene_Functions
    PRIMARY KEY (snp_id, gene_id),
    FOREIGN KEY (snp_id) REFERENCES SNPs(snp_id) ON DELETE CASCADE,
    -- If an SNP is deleted, all its linked gene associations will also be deleted
    FOREIGN KEY (gene_id) REFERENCES Gene_Functions(gene_id) ON DELETE CASCADE
    -- If a gene is deleted, all its SNP associations will also be removed
);

-- ====================================================================
-- 3. Testing Queries: Verifying Integrity and Performance
-- ====================================================================

-- Verify Foreign Key Constraints Exist
SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME 
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = 'sql8762368' 
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Testing the SNP-Population Relationship for SNP Filtering
SELECT s.snp_id, p.pop_name, pa.allele_frequency
FROM SNPs s
JOIN SNP_Population sp ON s.snp_id = sp.snp_id
JOIN Population p ON sp.pop_id = p.pop_id
JOIN Population_Allele pa ON pa.pop_id = p.pop_id
WHERE s.snp_id = 'rs7903146';


-- Testing Population Comparison for Fst Values
EXPLAIN SELECT * FROM Fixation WHERE pop_id_1 = 6 AND pop_id_2 = 5 AND chromosome = 10;

-- Retrieve Genes Associated with an SNP
SELECT s.snp_id, g.gene_id, g.gene_description
FROM SNPs s
JOIN SNP_Gene sg ON s.snp_id = sg.snp_id
JOIN Gene_Functions g ON sg.gene_id = g.gene_id
WHERE s.snp_id = 'rs7903146';


-- Retrieve SNPs within a Gene’s Genomic Region
SELECT s.snp_id, g.gene_id, g.gene_start, g.gene_end, s.chromosome, s.position
FROM SNPs s
JOIN Gene_Functions g ON s.chromosome = g.chromosome
WHERE s.position BETWEEN g.gene_start AND g.gene_end
ORDER BY s.chromosome, s.position;

-- Testing Population Comparison for Fst Values
SELECT * FROM Fixation 
WHERE pop_id_1 = 6 
AND pop_id_2 = 5 
AND chromosome = 10;

-- Check Tajima’s D Values for a Specific Population
SELECT t.chromosome, t.pop_id, p.pop_name, t.bin_start, t.bin_end, t.tajimas_d
FROM TajimasD t
JOIN Population p ON t.pop_id = p.pop_id
WHERE t.chromosome = 10 AND t.pop_id = 6;

-- Retrieve Phenotypes Associated with SNPs
SELECT ps.snp_id, ps.phenotype_id, p.phenotype_name, p.phenotype_description
FROM Phenotype_SNP ps
JOIN Phenotype p ON ps.phenotype_id = p.phenotype_id
WHERE ps.snp_id = 'rs7903146';

-- Count the Number of SNPs per Population
SELECT p.pop_name, COUNT(sp.snp_id) AS total_snps
FROM SNP_Population sp
JOIN Population p ON sp.pop_id = p.pop_id
GROUP BY p.pop_name
ORDER BY total_snps DESC;

-- Retrieve SNPs With the Highest Statistical Significance
SELECT snp_id, chromosome, position, p_value 
FROM SNPs 
WHERE p_value IS NOT NULL 
ORDER BY p_value ASC 
LIMIT 10;

-- Retrieve the Two Populations With the Highest Fixation Index (Fst)
SELECT f.pop_id_1, f.pop_id_2, p1.pop_name AS population_1, p2.pop_name AS population_2, MAX(f.fst) AS max_fst
FROM Fixation f
JOIN Population p1 ON f.pop_id_1 = p1.pop_id
JOIN Population p2 ON f.pop_id_2 = p2.pop_id
GROUP BY f.pop_id_1, f.pop_id_2
ORDER BY max_fst DESC
LIMIT 1;

--  Retrieve the Most Frequent Effector Allele
SELECT effector_allele, COUNT(*) AS allele_count 
FROM SNPs 
GROUP BY effector_allele 
ORDER BY allele_count DESC 
LIMIT 1;

--  Verify the Number of SNPs Per Chromosome
SELECT chromosome, COUNT(*) AS snp_count 
FROM SNPs 
GROUP BY chromosome 
ORDER BY snp_count DESC;

-- ====================================================================
-- 4. Sample Data Insertion
-- ====================================================================

-- --------------------------------------------------------
-- Insert sample SNPs
-- --------------------------------------------------------
INSERT INTO SNPs (snp_id, chromosome, position, p_value, effector_allele, reference_allele, odds_ratio, source, link) 
VALUES 
('rs1116357', 2, 57060276, 6.9E-10, 'G', 'A', 1.09, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs147538848', 12, 31313679, 7.8E-10, 'A', 'G', 1.11, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs1575972', 9, 22301093, 1.5E-9, 'T', 'T', 1.19, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs9309245', 2, 53169910, 1.3E-8, 'G', 'C', 1.1, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs67156297', 1, 154364240, 2E-8, 'A', 'G', 1.14, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs7107784', 11, 2193859, 2.1E-8, 'G', 'G', 1.14, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs67839313', 15, 40327523, 2.4E-8, 'C', 'T', 1.09, 'GWAS', 'https://www.nature.com/articles/ncomms10531#:~:text=A%20single%2Dnucleotide%20polymorphism%20in,2%20diabetes%20in%20Japanese%20populations.'),
('rs243021', 2, 60357684, 1.1E-3, 'A', 'G', 1.23, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/'),
('rs10010131', 4, 6291188, 5.6E-3, 'G', 'A', 1.24, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/'),
('rs4457053', 5, 77129124, 3.6E-3, 'G', 'G', 1.25, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/'),
('rs13266634', 8, 117172544, 3.9E-4, 'C', 'C', 1.32, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/'),
('rs13292136', 9, 79337213, 4.4E-3, 'C', 'C', 1.29, 'GWAS', 'https://pmc.ncbi.nlih.gov/articles/PMC4057178/'),
('rs10811661', 9, 22134095, 1.2E-3, 'T', 'T', 1.34, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/'),
('rs1531343', 12, 65781114, 8.8E-3, 'C', 'G', 1.23, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4057178/');

-- the data was lost due to my mistake in csv conversion so i added them by insert 

-- ====================================================================
-- 5. Backup Reminder
-- ====================================================================
-- Use: mysqldump -u root -p T2D_Genetics > T2D_Genetics_backup.sql
