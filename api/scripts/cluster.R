options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
filename <- paste('data/', args[1], '/expression.csv', sep = '')
savefile <- paste('data/', args[1], '/cluster.RData', sep = '')

datExpr <- read.csv(filename, row.names = 1)
tree <- hclust(dist(datExpr), method = 'average')
save(tree, file=savefile)