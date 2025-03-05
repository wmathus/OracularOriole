# plotting_functions.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import seaborn as sns
import pandas as pd

# Function to plot Tajima's D by chromosome KEEP in, takes away the whole results SNPS. Doesn't do anything fancy!
# def plot_tajima_d_by_chromosome(chromosome, population, df):
#     filtered_df = df[(df["chromosome"] == chromosome) & (df["POPULATION"] == population)]
    
#     if filtered_df.empty:
#         print(f"No data found for chromosome {chromosome} and population {population}. Skipping plot.")
#         return None
    
#     gene_data = filtered_df[filtered_df["gene_id"].notna()]
    
#     distinct_colors = [
#         "#E6194B", "#3CB44B", "#FFE119", "#0082C8", "#F58231",
#         "#911EB4", "#46F0F0", "#F032E6", "#D2F53C", "#FABEBE",
#         "#008080", "#E6BEFF", "#AA6E28", "#800000", "#AAFFC3",
#         "#808000", "#FFD8B1", "#000080", "#808080", "#A9A9A9",
#         "#DC143C", "#20B2AA", "#9932CC", "#FF4500", "#2E8B57"
#     ]
    
#     num_genes = 25
#     unique_genes = gene_data["gene_id"].unique()
#     gene_color_map = {gene: color for gene, color in zip(unique_genes, distinct_colors)}
    
#     gene_stats = gene_data.groupby("gene_id").agg({"tajimas_d": ["mean", "std"]})
#     chromosome_stats = df.groupby("chromosome").agg({"tajimas_d": ["mean", "std"]})
    
#     gene_stats["tajimas_d", "std"] = gene_stats["tajimas_d", "std"].fillna(0)
#     chromosome_stats["tajimas_d", "std"] = chromosome_stats["tajimas_d", "std"].fillna(0)
    
#     plt.figure(figsize=(16, 8))
    
#     for gene, color in gene_color_map.items():
#         gene_subset = gene_data[gene_data["gene_id"] == gene]
#         plt.scatter(gene_subset["BIN_START_Mb"], gene_subset["tajimas_d"], 
#                     color=color, alpha=1, marker="x", label=f"Gene: {gene}")
    
#     plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
#     plt.xlabel("Genomic Position (Mb)")
#     plt.ylabel("Tajima's D")
#     plt.title(f"Manhattan Plot of Tajima's D Values (Chromosome {chromosome}, {population} Population)")
#     plt.legend(title="Gene Association", bbox_to_anchor=(1.05, 1), loc="upper left")
#     plt.grid(True, linestyle="--", alpha=0.75)
#     plt.tight_layout()
    
#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
#     plt.close()
#     img_buffer.seek(0)
    
#     img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
#     return f"data:image/png;base64,{img_base64}"


def plot_tajima_d_by_chromosome(chromosome, population, df, snp_df):
    """
    Generates a Manhattan plot of Tajima's D values for a given chromosome and population.
    Also overlays vertical lines at SNP positions and labels them at the bottom of the plot
    Also uses snp_df which is a conversion of user results to map SNPs to the plot.
    Will plot each gene in different colours, had to use varying shapes for some regions. e.g. with chr2 results

    Returns: Base64 encoded image.
    """
    filtered_df = df[(df["chromosome"] == chromosome) & (df["POPULATION"] == population)]
    
    if filtered_df.empty:
        print(f"No data found for chromosome {chromosome} and population {population}. Skipping plot.")
        return None
    
    gene_data = filtered_df[filtered_df["gene_id"].notna()]
    
    distinct_colors = [
        "#E6194B", "#3CB44B", "#FFE119", "#0082C8", "#F58231",
        "#911EB4", "#46F0F0", "#F032E6", "#D2F53C", "#FABEBE",
        "#008080", "#E6BEFF", "#AA6E28", "#800000", "#AAFFC3",
        "#808000", "#FFD8B1", "#000080", "#808080", "#A9A9A9",
        "#DC143C", "#20B2AA", "#9932CC", "#FF4500", "#2E8B57"
    ]
    
    unique_genes = gene_data["gene_id"].unique()
    gene_color_map = {gene: color for gene, color in zip(unique_genes, distinct_colors)}
    
    plt.figure(figsize=(16, 8))

    # Alternating marker shapes (Triangle-Up and Circle)
    markers = ["^", "o"]  # Triangle-up and Circle
    marker_map = {gene: markers[i % 2] for i, gene in enumerate(unique_genes)}

    # Plot Tajima's D data
    for gene, color in gene_color_map.items():
        gene_subset = gene_data[gene_data["gene_id"] == gene]
        plt.scatter(
            gene_subset["BIN_START_Mb"], gene_subset["tajimas_d"], 
            color=color, alpha=0.7, marker=marker_map[gene], 
            edgecolors="black", linewidths=0.8, s=50, label=f"Gene: {gene}", zorder=3)
    
    # Plot vertical lines for SNP locations and collect SNP labels
    snp_df_filtered = snp_df[snp_df["chromosome"] == chromosome]
    
    for _, row in snp_df_filtered.iterrows():
        plt.axvline(x=row["gene_start_mb"], color="red", linestyle="--", alpha=0.4, zorder=2)

    # Add SNP labels at the bottom
    for _, row in snp_df_filtered.iterrows():
        plt.text(
            row["gene_start_mb"], min(filtered_df["tajimas_d"]) - 0.2,  # Offset below lowest Tajima's D value
            row["snp_id"], fontsize=9, rotation=90, color="red", alpha=0.7,
            ha='right', va='top', zorder=2)

    # Final plot adjustments
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1, zorder=1)
    plt.xlabel("Genomic Position (Mb)")  # **X-axis is still Megabases**
    plt.ylabel("Tajima's D")
    plt.title(f"Manhattan Plot of Tajima's D Values (Chromosome {chromosome}, {population} Population)")
    plt.legend(title="Gene Association", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.75)
    plt.tight_layout()
    
    # Save and return image as Base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    img_buffer.seek(0)
    
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"




def plot_fst_heatmap(df):
    """
    Generates an FST heatmap from the given DataFrame.
    Assumes columns: ['chromosome', 'comparison', 'fst']
    Returns image as a Base64 string.
    """
    if df is None or df.empty:
        print("Error: No valid FST data provided for heatmap generation.")
        return None

    # Pivot table for heatmap
    heatmap_data = df.pivot_table(index="chromosome", columns="comparison", values="fst", aggfunc="mean")

    # Fill NaN values with 0 (to handle missing comparisons)
    heatmap_data_filled = heatmap_data.fillna(0)

    # Replace negative FST values with 0 using NumPy's clip()
    heatmap_data_filled = heatmap_data_filled.clip(lower=0)

    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data_filled, annot=True, cmap="coolwarm", fmt=".3f", linewidths=0.5)
    plt.title("Pairwise FST Heatmap (Mean per Chromosome)")
    plt.xlabel("Population Comparison")
    plt.ylabel("Chromosome")

    # Save the plot to an in-memory buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", dpi=300, bbox_inches="tight")
    plt.close()
    img_buffer.seek(0)

    # Convert image to Base64 for frontend display
    img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"



# Function to plot Tajima's D values across all chromosomes for a population
def plot_tajima_d_all_chromosomes(population, df):
    """
    Generates a Manhattan plot of Tajima's D values for all chromosome in a population.
    Returns image of the plot. Colour coded by chromosome
    """
    filtered_df = df[df["POPULATION"] == population]
    
    if filtered_df.empty:
        print(f"No data found for population {population}. Skipping plot.")
        return None
    
    plt.figure(figsize=(16, 8))
    
    unique_chromosomes = sorted(filtered_df["chromosome"].unique())
    cumulative_positions = {}
    cumulative_offset = 0
    
    for chromosome in unique_chromosomes:
        chromosome_data = filtered_df[filtered_df["chromosome"] == chromosome]
        x_positions = chromosome_data["BIN_START_Mb"] + cumulative_offset
        plt.scatter(x_positions, chromosome_data["tajimas_d"], 
                    label=f"Chromosome {chromosome}", alpha=1, marker="x")
        
        cumulative_positions[chromosome] = cumulative_offset + (chromosome_data["BIN_START_Mb"].max() / 2)
        cumulative_offset += chromosome_data["BIN_START_Mb"].max() + 10
    
    plt.xlabel("Chromosome")
    plt.ylabel("Tajima's D")
    plt.title(f"Manhattan Plot of Tajima's D Values ({population} Population)")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xticks(
        ticks=[cumulative_positions[chromosome] for chromosome in unique_chromosomes],
        labels=[f"Chr {chromosome}" for chromosome in unique_chromosomes],
        rotation=45)
    plt.legend(title="Chromosome", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.75)
    plt.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    img_buffer.seek(0)
    
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

# Function for the histogram plotting (Tajima's D)
def plot_tajima_d_histogram(population, df):
    filtered_df = df[df["POPULATION"] == population]
    
    if filtered_df.empty:
        print(f"No data found for population {population}. Skipping plot.")
        return None
    
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_df["tajimas_d"], color='blue', alpha=0.7, edgecolor='black', zorder=2, bins=30)
    plt.xlabel("Tajima's D")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Tajima's D Values ({population} Population)")
    plt.grid(True, linestyle="--", alpha=0.75, zorder=0.5)
    plt.axvline(0, color="black", linestyle="--", linewidth=1.5, zorder=3)
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    img_buffer.seek(0)
    
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


# def results_conversion():
#     filtered_results = [{'snp_id': entry['snp_id'], 'chromosome': entry['chromosome'], 'gene_id': entry['gene_id'], 'gene_start': entry['gene_start'], 'gene_end': entry['gene_end']} 
#                         for entry in results]
#     print(filtered_results)