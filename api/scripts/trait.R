suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
load(paste('data/', args[1], '/colors.RData', sep = ''))
filename <- paste('data/', args[1], '/expression.csv', sep = '')
writename <- paste('data/', args[1], '/pvalues.csv', sep = '')
group <- as.factor(strsplit(args[2], ',')[[1]])

datExpr <- read.csv(filename, row.names = 1)

nGenes <- ncol(datExpr)
nSamples <- nrow(datExpr)
MEs0 <- moduleEigengenes(datExpr, colors)$eigengenes
MEs <- orderMEs(MEs0)

p.values <- sapply(colnames(MEs), function(col) kruskal.test(MEs[, col], group)$p.value)
p.values.adjusted <- p.adjust(p.values, 'fdr')
significant <- colnames(MEs)[p.values.adjusted < 0.05]

MEnames <- paste(names(p.values.adjusted), collapse = ',')
MEvalues <- paste(p.values.adjusted, collapse = ',')
cat(paste(MEnames, MEvalues, sep = '\t'))

combinations <- combn(levels(group), 2)
p.values.samples <- sapply(colnames(MEs), function(col) {
  eigengene <- MEs[, col]
  p.values <- apply(combinations, 2, function(combination) {
    group1_eigengene <- eigengene[which(group == combination[1])]
    group2_eigengene <- eigengene[which(group == combination[2])]
    return(wilcox.test(group1_eigengene, group2_eigengene)$p.value)
  })
  return(p.values)
})

write.csv(p.values.samples, writename, row.names = F)
