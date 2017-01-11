suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
load(paste('data/', args[1], '/cluster.RData', sep = ''))
filename <- paste('data/', args[1], '/expression.csv', sep = '')
cutHeight <- commandArgs(TRUE)[2]

clust <- cutreeStatic(tree, cutHeight = as.integer(cutHeight), minSize = 10)
datExpr <- read.csv(filename, row.names = 1)
datExpr <- datExpr[clust == 1, ]
write.csv(datExpr, filename)
