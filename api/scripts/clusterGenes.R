suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
expressionfile <- paste('data/', args[1], '/expression.csv', sep = '')
tomfile <- paste('data/', args[1], '/tom.png', sep = '')
genetreefile <- paste('data/', args[1], '/geneTree.RData', sep = '')
softPower <- as.integer(args[2])

datExpr <- read.csv(expressionfile, row.names = 1)

adjacency <- adjacency(datExpr, power = softPower, type = 'signed', corFnc = 'bicor')
TOM <- TOMsimilarity(adjacency, TOMType = 'signed')
dissTOM <- 1 - TOM

geneTree <- hclust(as.dist(dissTOM), method = 'average')
png(tomfile, width = 12, height = 6, units = 'in', res = 100)
plot(geneTree, xlab="", sub="", main = "Gene clustering on TOM-based dissimilarity",
     labels = FALSE, hang = 0.04)
dev.off()

save(geneTree, dissTOM, file=genetreefile)