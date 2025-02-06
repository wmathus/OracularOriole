create database ff;
use ff;

CREATE TABLE Phenotype (
    phenotype_id VARCHAR(50) PRIMARY KEY, -- Unique identifier for phenotypes
    phenotype_name VARCHAR(100) NOT NULL, -- Name of the phenotype
    phenotype_description TEXT -- Description of the phenotype
);

CREATE TABLE SNPs (
    snp_id VARCHAR(50) PRIMARY KEY, -- Unique identifier for SNPs
    chromosome INT NOT NULL, -- Chromosome number
    alternate_allele VARCHAR(50), -- Alternate alleles
    p_value FLOAT NOT NULL, -- P-value for significance
    odds_ratio DECIMAL(10,3), -- Odds ratio
    source VARCHAR(50), -- Source of the SNP data
    link TEXT -- Reference link
);

CREATE TABLE Gene_Functions (
    gene_id VARCHAR(50) PRIMARY KEY, -- Unique identifier for genes
    gene_description TEXT, -- Description of the gene function
    gene_start BIGINT, -- Start position of the gene
    gene_end BIGINT, -- End position of the gene
    ontology TEXT -- Gene ontology
);

CREATE TABLE SNP_Genome (
    snp_id VARCHAR(50), -- Foreign key referencing SNPs
    gene_id VARCHAR(50), -- Foreign key referencing Gene_Functions
    PRIMARY KEY (snp_id, gene_id), -- Composite primary key
    CONSTRAINT fk_snp_genome_snp FOREIGN KEY (snp_id) REFERENCES SNPs(snp_id) ON DELETE CASCADE,
    CONSTRAINT fk_snp_genome_gene FOREIGN KEY (gene_id) REFERENCES Gene_Functions(gene_id) ON DELETE CASCADE
);


CREATE TABLE Phenotype_SNP (
    phenotype_id VARCHAR(50), -- Foreign key referencing Phenotype
    snp_id VARCHAR(50), -- Foreign key referencing SNPs
    PRIMARY KEY (phenotype_id, snp_id), -- Composite primary key
    CONSTRAINT fk_phenotype_snp_phenotype FOREIGN KEY (phenotype_id) REFERENCES Phenotype(phenotype_id) ON DELETE CASCADE,
    CONSTRAINT fk_phenotype_snp_snp FOREIGN KEY (snp_id) REFERENCES SNPs(snp_id) ON DELETE CASCADE
);

CREATE TABLE Population (
    pop_id VARCHAR(50) PRIMARY KEY, -- Unique identifier for populations
    region VARCHAR(100) NOT NULL, -- Region of the population
    allele_freq FLOAT -- Allele frequency
);

CREATE TABLE Selection_Statistics (
    snp_id VARCHAR(50), -- Foreign key referencing SNPs
    pop_id VARCHAR(50), -- Foreign key referencing Population
    fst_value FLOAT NOT NULL, -- Fixation index value
    ihs_value FLOAT NOT NULL, -- Integrated haplotype score
    PRIMARY KEY (snp_id, pop_id), -- Composite primary key
    CONSTRAINT fk_selection_statistics_snp FOREIGN KEY (snp_id) REFERENCES SNPs(snp_id) ON DELETE CASCADE,
    CONSTRAINT fk_selection_statistics_pop FOREIGN KEY (pop_id) REFERENCES Population(pop_id) ON DELETE CASCADE
);

INSERT INTO Phenotype (phenotype_id, phenotype_name, phenotype_description)
VALUES
    ('HBA1C', 'glycated hemoglobin', 'A diabetes marker that measures the amount of glucose attached to the red blood cell''s haemoglobin'),
    ('HDL', 'High-density lipoprotein', 'Lower HDL cholesterol levels are associated with greater T2D risk'),
    ('LDL', 'low-density lipoprotein', 'Higher LDL cholesterol levels are associated with greater T2D risk'),
    ('DR', 'diabetic retinopathy', 'An eye condition that causes damage to the retinal blood vessels due to chronically elevated blood sugar levels from diabetes'),
    ('BMI', 'body mass index', 'A value derived from the weight and height of a person');

INSERT INTO SNPs (snp_id, chromosome, alternate_allele, p_value, odds_ratio, source, link)
VALUES
    ('rs11187138-A', 10, 'C,G', 5e-10, 1.234, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9119587/'),
    ('rs35261542-A', 6, 'A', 5e-10, 1.259, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9119587/'),
    ('rs7903146-T', 10, 'G,T', 2e-17, 1.366, 'GWAS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9119587/'),
    ('rs10916784-G', 1, 'A,C,T', 3e-11, 1.03, 'GWAS', 'https://www.nature.com/articles/s41588-022-01000-8');

INSERT INTO Gene_Functions (gene_id, gene_description, gene_start, gene_end, ontology)
VALUES
    ('HHEX', 'hematopoietically expressed homeobox', 92689955, 92695647, NULL),
    ('Y_RNA', 'Y RNA', 133337728, 133337824, NULL),
    ('CDKAL1', 'transcription factor 7 like 2', 112950247, 113167678, NULL),
    ('LINC01141', 'long intergenic non-protein coding RNA 1141', 20360579, 20439489, NULL),
    ('MACF1', 'microtubule actin crosslinking factor 1', 39081316, 39487177, NULL);

INSERT INTO SNP_Genome (snp_id, gene_id)
VALUES
    ('rs11187138-A', 'HHEX'),
    ('rs11187138-A', 'Y_RNA'),
    ('rs35261542-A', 'CDKAL1'),
    ('rs7903146-T', 'LINC01141'),
    ('rs10916784-G', 'MACF1');
    
    
INSERT INTO Phenotype_SNP (phenotype_id, snp_id)
VALUES
    ('HBA1C', 'rs11187138-A'),
    ('HBA1C', 'rs35261542-A'),
    ('DR', 'rs7903146-T'),
    ('HBA1C', 'rs10916784-G');
    
INSERT INTO Population (pop_id, region, allele_freq)
VALUES
    ('pakistani', 'south asian', 2.5);
    
INSERT INTO Selection_Statistics (snp_id, pop_id, fst_value, ihs_value)
VALUES
    ('rs11187138-A', 'pakistani', 0.24, 2.56),
    ('rs35261542-A', 'pakistani', 0.19, 1.98),
    ('rs7903146-T', 'pakistani', 0.31, 2.85),
    ('rs10916784-G', 'pakistani', 0.21, 2.10);
    
SELECT * FROM Phenotype;
SELECT * FROM SNPs;
SELECT * FROM Gene_Functions;
SELECT * FROM SNP_Genome;
SELECT * FROM Phenotype_SNP;
SELECT * FROM Population;
SELECT * FROM Selection_Statistics;




