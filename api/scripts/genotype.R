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

m <- data.frame(t(p.values.samples))
colnames(m) <- apply(combinations, 2, function(c) paste(c[1], 'vs', c[2]))
m$significance <- p.values.adjusted

write.csv(m, writename)