suppressMessages(library(WGCNA))
options(stringsAsFactors = FALSE)


args <- commandArgs(TRUE)
loadfile <- paste('data/', args[1], '/geneTree.RData', sep = '')
tomfile <- paste('data/', args[1], '/tom-colors.png', sep = '')
savefile <- paste('data/', args[1], '/colors.RData', sep = '')
minModuleSize <- as.integer(args[2])
deepSplit <- as.integer(args[3])

load(loadfile)

dynamicMods <- cutreeDynamic(dendro = geneTree, distM = dissTOM,
                            deepSplit = deepSplit, pamRespectsDendro = FALSE,
                            minClusterSize = minModuleSize)
colors <- labels2colors(dynamicMods)

png(tomfile, width = 12, height = 6, units = 'in', res = 100)
plotDendroAndColors(geneTree, colors, "Modules",
                    dendroLabels = FALSE, hang = 0.03,
                    addGuide = TRUE, guideHang = 0.05,
                    main = "Gene clustering on TOM-based dissimilarity")
dev.off()

save(colors, file=savefile)