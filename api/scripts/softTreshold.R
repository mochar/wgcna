suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)

args <- commandArgs(TRUE)
filename <- paste('data/', args[1], '/expression.csv', sep = '')
tresholdsname <- paste('data/', args[1], '/tresholds.csv', sep = '')

datExpr <- read.csv(filename, row.names = 1)

powers <- c(c(1:10), seq(from = 12, to=20, by=2))
sft <- pickSoftThreshold(datExpr, powerVector = powers, verbose = 5,
                         corFnc = 'bicor')

tresholds <- data.frame(
    powers = powers, 
    scaleindep = -sign(sft$fitIndices[,3]) * sft$fitIndices[,2],
    meank = sft$fitIndices[,5])
    

write.csv(tresholds, tresholdsname, row.names = F)