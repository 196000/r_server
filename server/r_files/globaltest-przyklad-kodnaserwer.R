#
#   Przyk3ad u?ycia metody Globaltest do analizy pobudzenia szlaków sygna3owych 
#
#   metoda: globaltest (p. vignette("GlobalTest")   --> GlobalTest.pdf)
#

library(globaltest)
#vignette("GlobalTest")
library(org.Hs.eg.db)

gt.options(trim = TRUE)		# nie zg3aszaj b3edu jeoli pewne geny usuniete
					# z macierzy, a obecne w subsets



#
# zaczynamy analize pathway'ów od wczytania pliku z danymi
#

# datadir <- "C:/temp"
# datadir <- "F:/projekt/open_beta/media/server"
exprsFile <- file.path(datadir2, "data.csv")

em <- read.table(exprsFile,sep=";",header=FALSE,row.names=1,as.is=TRUE)
#head(em)
#dim(em)

# wczytaj target 
targetFile <- file.path(datadir2, "target.csv")
tv <- read.table(targetFile,sep=";",header=TRUE)


dataX <- t(em)	# globaltest wymaga genów jako kolumny
dataY <- as.factor(tv[,1])	# targetem bedzie zmienna disease 


#
#  wczytaj probe2entrez -- mapujemy oznaczenie genów (Agilent ProbeID) na
#                          standardowe identyfikatory Entrez
#
datadir <- "media/server"
mapFile <- file.path(datadir, "AgilentProbe2Entrez.csv")
#p2e <- read.table(mapFile,sep=";",header=TRUE,row.names=1,as.is=TRUE)
p2e <- read.table(mapFile,sep=";",header=TRUE,as.is=TRUE)

lista <- as.list(p2e[,2])
names(lista) <- p2e[,1]


#
# I gwóYdY programu -- wywy3ujemy metode Globaltest
#
res <- gtKEGG(dataY, dataX, probe2entrez = lista, annotation = "org.Hs.eg.db")

#
# wynik 1: lista najbardziej aktywnych pathway'ów
#
lista_PWs <- result(res)
sink("static/server/out.txt")
print(lista_PWs)	# to chcemy pokazaa na stronie
sink()

#
# wynik 2: wizualizacja najwa?niejszych genów w pathway'u 1 -- najbardziej aktywnym
#
#pdf <- "F:/projekt/open_beta/static/server/testowy.pdf"
pdf <- "static/server/testowy.pdf"
f <- features(res[1], pdf=pdf)	# wizualizacja dla 1-wszego pathway'a - chcemy zobaczya obrazek