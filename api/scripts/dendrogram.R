options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
load(paste('data/', args[1], '/cluster.RData', sep = ''))
filename <- paste('data/', args[1], '/sample-clustering.png', sep = '')
cutHeight <- commandArgs(TRUE)[2]

png(filename, width = 12, height = 9, units = 'in', res = 100)
par(cex = 0.6)
par(mar = c(0, 4, 2, 0))
plot(tree, main = '', sub = '', xlab = '', cex.lab = 1.5, cex.axis = 1.5, cex.main = 2)
abline(h = as.integer(cutHeight), col = 'red')
dev.off()