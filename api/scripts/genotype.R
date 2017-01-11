suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
load(paste('data/', args[1], '/colors.RData', sep = ''))
filename <- paste('data/', args[1], '/expression.csv', sep = '')
writename <- paste('data/', args[1], '/genotype-pvalues.csv', sep = '')
group <- as.factor(strsplit(args[2], ',')[[1]])

datExpr <- read.csv(filename, row.names = 1)

nGenes <- ncol(datExpr)
nSamples <- nrow(datExpr)
MEs0 <- moduleEigengenes(datExpr, colors)$eigengenes
MEs <- orderMEs(MEs0)

p.values <- sapply(colnames(MEs), function(col) kruskal.test(MEs[, col], group)$p.value)
p.values.adjusted <- p.adjust(p.values, 'fdr')
write.csv(data.frame(p.values.adjusted), writename)