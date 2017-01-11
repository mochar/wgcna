suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
filename <- paste('data/', args[1], '/expression.csv', sep = '')

datExpr <- read.csv(filename, row.names = 1)
gsg <- goodSamplesGenes(datExpr, verbose = 0)
samples <- paste(rownames(datExpr)[!gsg$goodSamples], collapse = ',')
genes <- paste(colnames(datExpr)[!gsg$goodGenes], collapse = ',')
cat(paste(gsg$allOK, samples, genes, sep = '\t'))