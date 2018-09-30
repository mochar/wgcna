suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
filename <- paste(args[1], '/expression.csv', sep = '')
writename <- paste(args[1], '/pvalues.csv', sep = '')
group <- as.factor(strsplit(args[2], ',')[[1]])

datExpr <- read.csv(filename, row.names = 1)
modules <- read.csv(paste(args[1], '/modules.csv', sep = ''), row.names = 1)$modules
MEs <- read.csv(paste(args[1], '/eigengenes.csv', sep = ''), row.names = 1)

p.values <- sapply(colnames(MEs), function(col) kruskal.test(MEs[, col], group)$p.value)
p.values.adjusted <- p.adjust(p.values, 'fdr')

combinations <- combn(levels(group), 2)
nCombinations <- ncol(combinations)
p.values.samples <- sapply(seq(1, ncol(MEs)), function(index) {
  module <- names(MEs)[index]
  eigengene <- MEs[, index]
  p.value <- p.values.adjusted[module]
  if (p.value > 0.05) {
    return(rep(NA, nCombinations))
  }
  p.values <- apply(combinations, 2, function(combination) {
    group1_eigengene <- eigengene[which(group == combination[1])]
    group2_eigengene <- eigengene[which(group == combination[2])]
    return(wilcox.test(group1_eigengene, group2_eigengene)$p.value)
  })
  return(p.values)
})
p.values.samples <- p.adjust(unlist(as.list(p.values.samples)), 'fdr')
p.values.samples <- matrix(p.values.samples, ncol=length(MEs), nrow=nCombinations)

m <- data.frame(t(p.values.samples))
    
colnames(m) <- apply(combinations, 2, function(c) paste(c[1], 'vs', c[2]))
rownames(m) <- names(MEs)

m$significance <- p.values.adjusted

write.csv(m, writename)
