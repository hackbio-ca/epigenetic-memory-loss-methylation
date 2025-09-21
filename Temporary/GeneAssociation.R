library(IlluminaHumanMethylation450kanno.ilmn12.hg19)
library(IlluminaHumanMethylationEPICanno.ilm10b4.hg19)
library(minfi)
library(readr)
library(dplyr)

# Load annotation
ann450k <- getAnnotation(IlluminaHumanMethylation450kanno.ilmn12.hg19)
ann850k <- getAnnotation(IlluminaHumanMethylationEPICanno.ilm10b4.hg19)

# Read CpG site lists
diseaseCpGSites <- read_csv("cpg_sites.csv")$`Site Name`
# Subset annotations
disease_genes <- ann850k[rownames(ann850k) %in% diseaseCpGSites, c("Name", "UCSC_RefGene_Name")]

# Convert to data frame if needed
disease_genes_df <- as.data.frame(disease_genes)

View(disease_genes_df)

# Save to CSV
write_csv(disease_genes_df, "disease_cpg_gene_map.csv")
