# import
all_data = read.table('/cellar/users/ramarty/Data/kir/components/tcga/kir_four_random_read_counts.csv', sep = ',', row.names = 1, header = True)
capture_kits <- read.table('/cellar/users/ramarty/Data/kir/ref/sample.capture.kit', sep = '\t', header = T, row.names = 2)

library(liger)

# select capture kit in all_data
kits = capture_kits$KIT[capture_kits$SHORT_ID %in% row.names(all_data)]

nimb1 <- capture_kits$SHORT_ID[capture_kits$KIT == 'Nimblegen HGSC']
a <- all_data[nimb1]

nimb2 <- capture_kits$SHORT_ID[capture_kits$KIT == 'Nimblegen.SQEZ2']
b<-all_data[nimb2]

# use liger to join them
liger_object = createLiger(list(nimb1=a, nimb2=b))