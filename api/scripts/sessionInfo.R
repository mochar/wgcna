suppressMessages(library(WGCNA))

args <- commandArgs(TRUE)
filename <- paste('data/', args[1], '/sessionInfo.txt', sep = '')

sink(filename)
sessionInfo()
sink()